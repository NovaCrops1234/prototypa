import os
import asyncio
import discord
import psycopg2
from google import genai
from google.genai import types
from dotenv import load_dotenv
from persona import SYSTEM_PROMPT
from changelog import CHANGELOG_VERSION, CHANGELOG
from memory import (
    init_db, get_history, save_message, clear_history,
    save_global_fact, get_global_memory,
    save_user_profile, get_user_profile,
    get_active_users, has_broadcast_sent, mark_broadcast_sent
)

load_dotenv()
init_db()

# Config
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Extraction prompt for Global Memory
EXTRACT_PROMPT = """
You are a memory extraction assistant for an android named Nisama.
Given a user message, extract any notable facts worth remembering about this person.

IMPORTANT RULES:
- Only extract a name if the user EXPLICITLY states their own name in the message itself.
  Example of valid: "I am Craexy-sama", "my name is Mike", "call me J-san"
  Example of NOT valid: user just says "hi", "hello", "how are you" — extract nothing
- Do not use the Username field as a fact. That is just a system identifier, not a self-introduction.
- Notable facts include: explicitly stated name, what they are currently doing, their role/job,
  their location, their relationships, their plans, or anything personally significant they share.

Reply ONLY with a JSON array of short fact strings. Maximum 3 facts.
If nothing notable, reply with empty array: []

Examples:
Input: "I am Craexy-sama, working on stuff for Tevah today"
Output: ["Introduced themselves as Craexy-sama", "Working on something for Tevah"]

Input: "hi" or "hello" or "how are you"
Output: []

Input: "yeah I'm good"
Output: []

Input: "Just got back from Hant City ruins, doing some scouting for J-san"
Output: ["Recently visited Hant City ruins", "Doing scouting work for J-san"]
"""


# Main
async def extract_and_save_facts(user_id: str, discord_name: str, message: str):
    profile = get_user_profile(user_id)
    known_as = profile["known_as"] if profile and profile["known_as"] else None

    try:
        response = client_ai.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[types.Content(
                role="user",
                parts=[types.Part(text=f"Known as (if introduced): {known_as or 'unknown'}\nMessage: {message}")]
            )],
            config=types.GenerateContentConfig(
                system_instruction=EXTRACT_PROMPT,
                max_output_tokens=200,
                temperature=0.1
            )
        )
        import json
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        facts = json.loads(raw.strip())

        for fact in facts:
            is_introduction = (
                "introduced" in fact.lower() or
                "known as" in fact.lower() or
                "calls himself" in fact.lower() or
                "calls herself" in fact.lower()
            )

            if is_introduction:
                if not known_as:
                    extracted_name = fact.split("as")[-1].strip().strip('"').strip("'")
                    save_user_profile(user_id, discord_name, known_as=extracted_name)
                continue

            if fact:
                save_global_fact(user_id, known_as or "unknown one", fact)

    except Exception as e:
        print(f"Fact extraction error (non-critical): {e}")


def build_gemini_contents(history: list) -> list:
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )
    return contents


def build_global_context(current_user_id: str) -> str:
    all_facts = get_global_memory(limit=30)
    active = get_active_users(minutes=10)

    lines = []

    if active:
        lines.append("Users Nisama is currently or recently talking to (last 10 minutes):")
        for a in active:
            lines.append(f"- {a['name']}: {a['fact'] or 'no details yet'}")
        lines.append("")

    if all_facts:
        lines.append("Nisama's shared memory — things Nisama knows about people:")
        for f in all_facts:
            name = f["name"] or "unknown one"
            lines.append(f"- {name}: {f['fact']}")

    return "\n".join(lines) if lines else ""


async def broadcast_changelog():
    con = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = con.cursor()
    cur.execute("SELECT DISTINCT user_id FROM history")
    user_ids = [r[0] for r in cur.fetchall()]
    cur.close()
    con.close()

    for uid in user_ids:
        try:
            user = await bot.fetch_user(int(uid))
            await user.send(CHANGELOG)
            print(f"Sent changelog to {uid}")
        except Exception as e:
            print(f"Could not send to {uid}: {e}")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user} (ID: {bot.user.id})")
    print("Listening for DMs only.")

    if not has_broadcast_sent(CHANGELOG_VERSION):
        await broadcast_changelog()
        mark_broadcast_sent(CHANGELOG_VERSION)
        print(f"Changelog {CHANGELOG_VERSION} broadcast done.")
    else:
        print(f"Changelog {CHANGELOG_VERSION} already sent, skipping.")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    user_id = str(message.author.id)
    discord_display_name = message.author.display_name
    user_text = message.content.strip()

    if user_text.lower() in ["clear memory"]:
        clear_history(user_id)
        await message.channel.send("Nisama has cleared the memory here. It is like meeting again for the first time.")
        return

    if not user_text:
        return

    # Save Discord name silently to DB only — Nisama never sees this
    save_user_profile(user_id, discord_display_name)

    # Pass user_id only, no display name leaked to extraction
    asyncio.create_task(extract_and_save_facts(user_id, discord_display_name, user_text))

    # Get this user's personal history
    history = get_history(user_id)
    save_message(user_id, "user", user_text)

    # Build global context of what Nisama knows about everyone
    global_context = build_global_context(user_id)

    # Inject user profile so Nisama always knows who she's talking to
    profile = get_user_profile(user_id)
    full_system = SYSTEM_PROMPT
    if profile and profile["known_as"]:
        # Only tell Nisama the name if the user has actually introduced themselves
        full_system += f"\n\nNisama is currently speaking with: {profile['known_as']}. Always address this person as {profile['known_as']}."
    else:
        # User hasn't introduced themselves yet — Nisama should use "one"
        full_system += f"\n\nNisama does not know this person's name yet. Refer to them as 'one' until they introduce themselves."
    if global_context:
        full_system += f"\n\n{global_context}"

    error_occurred = False
    async with message.channel.typing():
        try:
            contents = build_gemini_contents(history)
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=user_text)]
                )
            )

            response = client_ai.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=full_system,
                    max_output_tokens=1024,
                    temperature=0.85
                )
            )
            reply = response.text

        except Exception as e:
            print(f"Gemini error: {e}")
            reply = "Nisama currently AFK, please try again later."
            error_occurred = True

    if not error_occurred:
        save_message(user_id, "assistant", reply)

    if len(reply) > 2000:
        reply = reply[:1997] + "..."

    await message.channel.send(reply)


bot.run(os.getenv("DISCORD_TOKEN"))