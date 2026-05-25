import os
import asyncio
import discord
from google import genai
from google.genai import types
from dotenv import load_dotenv
from persona import SYSTEM_PROMPT
from memory import (
    init_db, get_history, save_message, clear_history,
    save_global_fact, get_global_memory,
    save_user_profile, get_user_profile
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
async def extract_and_save_facts(user_id: str, username: str, message: str):
    """Extract notable facts from a message and save to global memory."""
    try:
        response = client_ai.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[types.Content(
                role="user",
                parts=[types.Part(text=f"Username: {username}\nMessage: {message}")]
            )],
            config=types.GenerateContentConfig(
                system_instruction=EXTRACT_PROMPT,
                max_output_tokens=200,
                temperature=0.1
            )
        )
        import json
        raw = response.text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        facts = json.loads(raw.strip())
        for fact in facts:
            if fact:
                save_global_fact(user_id, username, fact)

        # If someone introduces a custom name, save it to their profile
        for fact in facts:
            if "introduced" in fact.lower() or "known as" in fact.lower() or "calls himself" in fact.lower() or "calls herself" in fact.lower():
                save_user_profile(user_id, username, known_as=fact.split("as")[-1].strip().strip('"').strip("'"))

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
    """Build a summary of what Nisama knows about everyone."""
    all_facts = get_global_memory(limit=30)
    if not all_facts:
        return ""
    
    lines = ["Nisama's shared memory — things Nisama knows about people:"]
    for f in all_facts:
        name = f["name"] or "Unknown one"
        lines.append(f"- {name}: {f['fact']}")
    
    return "\n".join(lines)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    user_id = str(message.author.id)
    username = message.author.display_name
    user_text = message.content.strip()

    if user_text.lower() in ["clear memory"]:
        clear_history(user_id)
        await message.channel.send("Nisama has cleared the memory here. It is like meeting again for the first time.")
        return

    if not user_text:
        return

    # Always save/update basic profile from Discord display name
    save_user_profile(user_id, username)

    # Extract facts in background — doesn't block Nisama's reply
    asyncio.create_task(extract_and_save_facts(user_id, username, user_text))

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

    save_message(user_id, "assistant", reply)

    if len(reply) > 2000:
        reply = reply[:1997] + "..."

    await message.channel.send(reply)


bot.run(os.getenv("DISCORD_TOKEN"))