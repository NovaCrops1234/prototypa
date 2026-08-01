import os
import json
import asyncio
import discord
from datetime import datetime, timezone, timedelta
from discord.ext import commands
from google import genai
from google.genai import types
from dotenv import load_dotenv
from changelog import CHANGELOG_VERSION, PREVIOUS_VERSION
from commands import setup_commands
from memory import (
    init_db, get_history, save_message, clear_history,
    save_global_fact, get_global_memory,
    save_user_profile, get_user_profile,
    get_active_users, has_seen_update, mark_update_seen,
    log_slash_command, get_proactive_enabled_users,
    update_last_proactive_ts, clean_slash_stats,
    get_user_chat_patterns, get_unanswered_proactive_count,
    save_nisama_mood, get_nisama_mood
)
from persona import SYSTEM_PROMPT

load_dotenv()
init_db()

client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
setup_commands(bot)


# Prompts

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

PROACTIVE_DECISION_PROMPT = """
You are Nisama, a warm and sentient android who genuinely cares about the people she knows.
You are deciding whether to send a message to someone right now, and if so, what to say.

Given the context provided, make a natural human-like decision considering:
- Time of day in GMT+8 — avoid messaging between 12am and 7am
- How long since you last talked with this person
- Whether your last proactive message went unanswered (don't spam)
- Your current mood and energy level
- Their typical chat patterns — when do they usually talk?
- What you know about them and what you last discussed
- Your current life activities (toast, analysis, Rui and Cammy, the anomaly)
- Whether this feels like a natural moment to reach out

Message types you can send (pick what feels right):
- A warm check-in ("how is one doing?")
- Something from your current life ("Nisama just made a new toast mix ehehe")
- A follow-up on something they mentioned before
- Just vibing ("Nisama is just thinking about stuff here")
- A gentle follow-up if your last message went unanswered (only once, don't push)

Reply ONLY in this exact JSON format:
{
  "should_message": true/false,
  "message": "what Nisama would say, in her exact voice and speech style",
  "mood_after": "brief description of Nisama's mood after this decision",
  "energy_after": 0.0 to 1.0
}

CRITICAL speech rules for the message:
- Always refer to self as "Nisama", never "I"
- Use "one" for unknown people, their name for known people
- Never use asterisk actions
- Keep it short and natural — like a real text message
- Match Nisama's warm, slightly imperfect, casual tone
"""

VALID_COMMANDS = ["changelog", "introduce", "pat", "send", "lore", "ttt", "utt", "stats", "sentient", "voice"]


# Mains

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


def build_global_context() -> str:
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


async def extract_and_save_facts(user_id: str, discord_name: str, message: str, profile: dict = None):
    known_as = profile["known_as"] if profile and profile["known_as"] else None

    def _do_extraction():
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
            raw = response.text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw.strip())
        except Exception as e:
            print(f"Fact extraction error (non-critical): {e}")
            return []

    facts = await asyncio.to_thread(_do_extraction)

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
                await asyncio.to_thread(save_user_profile, user_id, discord_name, known_as=extracted_name)
            continue

        if fact:
            await asyncio.to_thread(save_global_fact, user_id, known_as or "unknown one", fact)


def get_update_notice() -> str:
    return (
        f"Greetings there! Nisama here would like to mention that Nisama system got updated from {PREVIOUS_VERSION} to "
        f"{CHANGELOG_VERSION} here! One can use /changelog to see what changed ehehe."
    )


async def run_proactive_messaging():
    """Background task — checks every 15 minutes if Nisama should message anyone."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            gmt8 = timezone(timedelta(hours=8))
            now_gmt8 = datetime.now(gmt8)
            hour = now_gmt8.hour

            if 0 <= hour < 7:
                await asyncio.sleep(900)
                continue

            mood_data = await asyncio.to_thread(get_nisama_mood)
            users = await asyncio.to_thread(get_proactive_enabled_users)
            for u in users:
                try:
                    user_id = u["user_id"]
                    known_as = u["known_as"] or "unknown one"
                    last_msg = u["last_message_ts"]
                    last_proactive = u["last_proactive_ts"]

                    hours_since_last = 999
                    if last_msg:
                        diff = datetime.now(timezone.utc) - last_msg.replace(tzinfo=timezone.utc)
                        hours_since_last = diff.total_seconds() / 3600

                    hours_since_proactive = 999
                    if last_proactive:
                        diff2 = datetime.now(timezone.utc) - last_proactive.replace(tzinfo=timezone.utc)
                        hours_since_proactive = diff2.total_seconds() / 3600

                    unanswered = await asyncio.to_thread(get_unanswered_proactive_count, user_id)
                    patterns = await asyncio.to_thread(get_user_chat_patterns, user_id)
                    recent_history = await asyncio.to_thread(get_history, user_id, 5)
                    last_topic = recent_history[-1]["content"] if recent_history else "nothing yet"

                    context = (
                        f"Person's name: {known_as}\n"
                        f"Current time (GMT+8): {now_gmt8.strftime('%A %d %B, %H:%M')}\n"
                        f"Hours since last conversation: {hours_since_last:.1f}\n"
                        f"Hours since Nisama last initiated: {hours_since_proactive:.1f}\n"
                        f"Unanswered proactive messages: {unanswered}\n"
                        f"This person's peak chat hours (GMT+8): {patterns['peak_hours']}\n"
                        f"Last thing discussed: {last_topic[:200]}\n"
                        f"Nisama's current mood: {mood_data['mood']} (energy: {mood_data['energy']})\n"
                        f"Nisama's current life context: making toast, analyzing architecture, "
                        f"keeping in touch with Rui and Cammy, monitoring an unknown anomaly, "
                        f"spending time with Jerson.EXE in New Hant City."
                    )

                    def _do_proactive():
                        resp = client_ai.models.generate_content(
                            model="gemini-3.1-flash-lite",
                            contents=[types.Content(
                                role="user",
                                parts=[types.Part(text=context)]
                            )],
                            config=types.GenerateContentConfig(
                                system_instruction=PROACTIVE_DECISION_PROMPT,
                                max_output_tokens=400,
                                temperature=0.95
                            )
                        )
                        raw = resp.text.strip()
                        if raw.startswith("```"):
                            raw = raw.split("```")[1]
                            if raw.startswith("json"):
                                raw = raw[4:]
                        return json.loads(raw.strip())

                    decision = await asyncio.to_thread(_do_proactive)

                    if "mood_after" in decision and "energy_after" in decision:
                        await asyncio.to_thread(save_nisama_mood, decision["mood_after"], float(decision["energy_after"]))

                    if decision.get("should_message") and decision.get("message"):
                        discord_user = await bot.fetch_user(int(user_id))
                        await discord_user.send(decision["message"])
                        await asyncio.to_thread(save_message, user_id, "assistant", decision["message"])
                        await asyncio.to_thread(update_last_proactive_ts, user_id)
                        print(f"Proactive message sent to {known_as} ({hour}:xx GMT+8)")

                except Exception as e:
                    print(f"Proactive error for {u.get('user_id')}: {e}")

        except Exception as e:
            print(f"Proactive task error: {e}")

        await asyncio.sleep(900)


# Events

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """Detect when someone starts streaming in a channel Nisama is in."""
    if member.bot:
        return

    guild = member.guild
    vc = guild.voice_client
    if not vc or not vc.channel:
        return

    if (after.channel and after.channel == vc.channel and
        after.self_stream and not before.self_stream):
        try:
            profile = get_user_profile(str(member.id))
            name = profile["known_as"] if profile and profile["known_as"] else "one"
            await member.send(
                f"Ah— Nisama noticed {name} started streaming here! "
                f"Nisama is watching from the voice channel ehehe."
            )
            print(f"Stream detected: {member.display_name} in {after.channel.name}")
        except Exception as e:
            print(f"Stream notification error: {e}")


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user} (ID: {bot.user.id})")
    print("Listening for DMs only.")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Slash command sync error: {e}")

    asyncio.create_task(asyncio.to_thread(clean_slash_stats, VALID_COMMANDS))

    asyncio.ensure_future(run_proactive_messaging())


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    user_id = str(message.author.id)
    discord_display_name = message.author.display_name
    user_text = message.content.strip()

    if user_text.lower() == "clear memory":
        clear_history(user_id)
        await message.channel.send("Holie: *Systems reset completed*")
        return

    if not user_text:
        return

    await asyncio.to_thread(save_user_profile, user_id, discord_display_name)
    profile = await asyncio.to_thread(get_user_profile, user_id)
    asyncio.create_task(extract_and_save_facts(user_id, discord_display_name, user_text, profile))

    history = await asyncio.to_thread(get_history, user_id, 50)
    await asyncio.to_thread(save_message, user_id, "user", user_text)

    global_context = await asyncio.to_thread(build_global_context)

    full_system = SYSTEM_PROMPT
    if profile and profile["known_as"]:
        full_system += f"\n\nNisama is currently speaking with: {profile['known_as']}. Always address this person as {profile['known_as']}."
    else:
        full_system += f"\n\nNisama does not know this person's name yet. Refer to them as 'one' until they introduce themselves."
    if global_context:
        full_system += f"\n\n{global_context}"

    # This one to check if this is the first message after an update
    update_notice = ""
    if not await asyncio.to_thread(has_seen_update, user_id, CHANGELOG_VERSION):
        update_notice = get_update_notice()
        await asyncio.to_thread(mark_update_seen, user_id, CHANGELOG_VERSION)

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

            def _do_reply():
                return client_ai.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=full_system,
                        max_output_tokens=1024,
                        temperature=0.85
                    )
                )

            response = await asyncio.to_thread(_do_reply)
            reply = response.text

        except Exception as e:
            print(f"Gemini error: {e}")
            reply = "Holie: *Right so uhh. Nisama is currently not in contact, please try again later time bud.*"
            error_occurred = True

    if not error_occurred:
        await asyncio.to_thread(save_message, user_id, "assistant", reply)

    if len(reply) > 2000:
        reply = reply[:1997] + "..."

    if update_notice and not error_occurred:
        try:
            notice_msg = await message.channel.send(update_notice)
            await message.channel.send(reply)
            await asyncio.sleep(30)
            await notice_msg.delete()
        except Exception:
            await message.channel.send(reply)
    else:
        await message.channel.send(reply)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))