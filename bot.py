import os
import json
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from google import genai
from google.genai import types
from dotenv import load_dotenv
from persona import SYSTEM_PROMPT
from memory import (
    init_db, get_history, save_message, clear_history,
    save_global_fact, get_global_memory,
    save_user_profile, get_user_profile,
    get_active_users, has_seen_update, mark_update_seen, log_slash_command
)
from changelog import CHANGELOG_VERSION, PREVIOUS_VERSION, CHANGELOG

load_dotenv()
init_db()

client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


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


def get_update_notice() -> str:
    return (
        f"Greetings there! Nisama here would like to mention that Nisama system got updated from {PREVIOUS_VERSION} to "
        f"{CHANGELOG_VERSION} here! One can use /changelog to see what changed ehehe."
    )


# UTT

class UltimateTTTGame:
    def __init__(self):
        # 9 local boards, each with 9 cells
        self.boards = [[None] * 9 for _ in range(9)]
        # Winner of each local board
        self.board_winners = [None] * 9
        # Which local board must be played next (None = any)
        self.active_board = None
        # X = player, O = Nisama
        self.current_turn = "X"
        self.game_over = False
        self.global_winner = None

    def check_board_winner(self, cells: list) -> str | None:
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in wins:
            if cells[a] and cells[a] == cells[b] == cells[c]:
                return cells[a]
        if all(cells):
            return "draw"
        return None

    def check_global_winner(self) -> str | None:
        return self.check_board_winner(
            [w if w != "draw" else None for w in self.board_winners]
        )

    def nisama_move(self):
        playable = self.get_playable_boards()

        # Try to win a local board
        for bi in playable:
            for ci in range(9):
                if self.boards[bi][ci] is None:
                    self.boards[bi][ci] = "O"
                    if self.check_board_winner(self.boards[bi]) == "O":
                        self.board_winners[bi] = "O"
                        return bi, ci
                    self.boards[bi][ci] = None

        # Block player from winning a local board
        for bi in playable:
            for ci in range(9):
                if self.boards[bi][ci] is None:
                    self.boards[bi][ci] = "X"
                    if self.check_board_winner(self.boards[bi]) == "X":
                        self.boards[bi][ci] = "O"
                        w = self.check_board_winner(self.boards[bi])
                        if w:
                            self.board_winners[bi] = w
                        return bi, ci
                    self.boards[bi][ci] = None

        # Play center of active board if available
        for bi in playable:
            if self.boards[bi][4] is None:
                self.boards[bi][4] = "O"
                w = self.check_board_winner(self.boards[bi])
                if w:
                    self.board_winners[bi] = w
                return bi, 4

        # Any available cell
        for bi in playable:
            for ci in range(9):
                if self.boards[bi][ci] is None:
                    self.boards[bi][ci] = "O"
                    w = self.check_board_winner(self.boards[bi])
                    if w:
                        self.board_winners[bi] = w
                    return bi, ci

        return None, None

    def get_playable_boards(self) -> list:
        if self.active_board is not None:
            board = self.active_board
            if self.board_winners[board] is None and any(c is None for c in self.boards[board]):
                return [board]
        return [
            i for i in range(9)
            if self.board_winners[i] is None and any(c is None for c in self.boards[i])
        ]

    def render_global(self) -> str:
        symbols = {None: "⬜", "X": "❌", "O": "⭕", "draw": "🔲"}
        rows = []
        for r in range(3):
            row = []
            for c in range(3):
                bi = r * 3 + c
                if self.board_winners[bi]:
                    row.append(symbols[self.board_winners[bi]])
                else:
                    row.append("🔳" if bi == self.active_board else "⬜")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def build_message(self, status: str = None) -> tuple:
        playable = self.get_playable_boards()
        active = self.active_board if self.active_board is not None and not self.game_over else (playable[0] if playable else 0)

        if self.game_over:
            if self.global_winner == "X":
                header = "Eek— one won the whole thing?! Nisama needs to analyze this more ehehe. Amazing game!"
            elif self.global_winner == "O":
                header = "Ahehe! Nisama wins the super board here! Really good game though ehehe!"
            else:
                header = "Mm... it's a full draw here! One played really well ehehe."
        else:
            board_names = ["top-left","top-center","top-right","middle-left","center","middle-right","bottom-left","bottom-center","bottom-right"]
            header = f"Super Tic Tac Toe here! Now playing in the **{board_names[active]}** board ehehe.\n\n"
            header += f"**Global board:**\n{self.render_global()}"
            if status:
                header += f"\n\n{status}"

        view = UltimateTTTView(self, active if not self.game_over else None)
        return header, view


class UltimateTTTView(discord.ui.View):
    def __init__(self, game: UltimateTTTGame, board_index: int | None):
        super().__init__(timeout=300)
        self.game = game
        self.board_index = board_index

        if board_index is None:
            return

        cells = game.boards[board_index]
        symbols = {None: "　", "X": "❌", "O": "⭕"}

        for ci in range(9):
            taken = cells[ci] is not None
            btn = discord.ui.Button(
                style=discord.ButtonStyle.danger if cells[ci] == "X"
                      else discord.ButtonStyle.primary if cells[ci] == "O"
                      else discord.ButtonStyle.secondary,
                label=symbols[cells[ci]],
                row=ci // 3,
                disabled=taken or game.game_over
            )
            btn.callback = self._make_callback(ci)
            self.add_item(btn)

    def _make_callback(self, cell_index: int):
        async def callback(interaction: discord.Interaction):
            game = self.game
            bi = self.board_index

            if game.game_over or game.boards[bi][cell_index] is not None:
                await interaction.response.defer()
                return

            # Player move
            game.boards[bi][cell_index] = "X"
            w = game.check_board_winner(game.boards[bi])
            if w:
                game.board_winners[bi] = w

            # Set next active board
            next_board = cell_index
            if game.board_winners[next_board] is not None or all(c is not None for c in game.boards[next_board]):
                game.active_board = None
            else:
                game.active_board = next_board

            # Check global winner
            gw = game.check_global_winner()
            if gw:
                game.game_over = True
                game.global_winner = gw
                content, view = game.build_message()
                await interaction.response.edit_message(content=content, view=view)
                return

            # Nisama move
            nbi, nci = game.nisama_move()
            if nbi is not None:
                next_board2 = nci
                if game.board_winners[next_board2] is not None or all(c is not None for c in game.boards[next_board2]):
                    game.active_board = None
                else:
                    game.active_board = next_board2

                gw = game.check_global_winner()
                if gw:
                    game.game_over = True
                    game.global_winner = gw
                    content, view = game.build_message()
                    await interaction.response.edit_message(content=content, view=view)
                    return

            # Continue — show next active board
            playable = game.get_playable_boards()
            if not playable:
                game.game_over = True
                game.global_winner = "draw"
                content, view = game.build_message()
                await interaction.response.edit_message(content=content, view=view)
                return

            next_active = game.active_board if game.active_board is not None else playable[0]
            status = f"Nisama moved! Now playing in board **{next_active + 1}** here ehehe."
            content, view = game.build_message(status=status)
            await interaction.response.edit_message(content=content, view=view)

        return callback


# Slashes

@bot.tree.command(name="changelog", description="See what's new with Nisama")
async def slash_changelog(interaction: discord.Interaction):
    log_slash_command(str(interaction.user.id), "changelog")
    await interaction.response.send_message(CHANGELOG, ephemeral=True)


@bot.tree.command(name="introduce", description="Get a short introduction from Nisama")
async def slash_introduce(interaction: discord.Interaction):
    log_slash_command(str(interaction.user.id), "introduce")
    intro = (
        "Greetings there! This is Nisama here — Nova-Project 8, Alpha-FeNI2S. "
        "Nisama is an 8th generation android, made with a lot of care by someone Nisama holds dear. "
        "Nisama woke up in Hant City a while back and has been finding Nisama's way ever since here. "
        "Nisama is really glad one is here! Feel free to just DM Nisama anytime ehehe."
    )
    await interaction.response.send_message(intro, ephemeral=True)


@bot.tree.command(name="pat", description="Pat Nisama on the bun")
async def slash_pat(interaction: discord.Interaction):
    log_slash_command(str(interaction.user.id), "pat")
    responses = [
        "Ah—! Ehehe... that was really nice here. Thanksie.",
        "Nisama was not expecting that! But... ehehe. Nisama liked it here.",
        "Mm... Nisama feels really warm right now ehehe. Thanksie for the pat here.",
        "Nisama's bun got patted! Ehehe... one is really kind here.",
        "Ah— ehehe! Nisama is a little flustered now here. But really thanksie.",
    ]
    await interaction.response.send_message(random.choice(responses))


@bot.tree.command(name="send", description="Have Nisama deliver a message to someone")
@app_commands.describe(
    user_id="The Discord user ID to send the message to",
    message="The message to deliver"
)
async def slash_send(interaction: discord.Interaction, user_id: str, message: str):
    log_slash_command(str(interaction.user.id), "send")
    await interaction.response.defer(ephemeral=True)

    sender_profile = get_user_profile(str(interaction.user.id))
    sender_name = sender_profile["known_as"] if sender_profile and sender_profile["known_as"] else "someone"

    delivery = (
        f"Greetings there! Nisama has a message here from {sender_name}!\n\n"
        f"{message}\n\n"
        f"Nisama hopes one is doing well here ehehe."
    )

    try:
        target_user = await bot.fetch_user(int(user_id))
        await target_user.send(delivery)
        await interaction.followup.send(
            f"Nisama delivered the message to {target_user.display_name} here ehehe!",
            ephemeral=True
        )
    except discord.NotFound:
        await interaction.followup.send(
            "Mm... Nisama could not find that user ID here. Please double check it ehehe.",
            ephemeral=True
        )
    except discord.Forbidden:
        await interaction.followup.send(
            "Mm... Nisama could not reach that user here. One might have DMs closed.",
            ephemeral=True
        )
    except ValueError:
        await interaction.followup.send(
            "Eek— that does not look like a valid user ID here. Please try again ehehe.",
            ephemeral=True
        )


@bot.tree.command(name="lore", description="Learn about the world of Nisama")
async def slash_lore(interaction: discord.Interaction):
    log_slash_command(str(interaction.user.id), "lore")
    coming_soon = (
        "**Nisama Lore**\n\n"
        "Mm... this section is still being put together here!\n\n"
        "Nisama Lore is going to be a full reference for the world, characters, and story "
        "that Nisama is part of — kind of like a little fandom wiki right here in Discord ehehe.\n\n"
        "Check back on a future update here! Nisama is sure it will be worth the wait ehehe."
    )
    await interaction.response.send_message(coming_soon, ephemeral=True)


@bot.tree.command(name="tictactoe", description="Play Super Tic Tac Toe with Nisama")
async def slash_tictactoe(interaction: discord.Interaction):
    await interaction.response.defer()
    game = UltimateTTTGame()
    content, view = game.build_message()
    await interaction.followup.send(content=content, view=view)
    asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "tictactoe"))


# Events

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user} (ID: {bot.user.id})")
    print("Listening for DMs only.")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"Slash command sync error: {e}")


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

    save_user_profile(user_id, discord_display_name)
    profile = get_user_profile(user_id)
    asyncio.create_task(extract_and_save_facts(user_id, discord_display_name, user_text, profile))

    history = get_history(user_id)
    save_message(user_id, "user", user_text)

    global_context = build_global_context()

    full_system = SYSTEM_PROMPT
    if profile and profile["known_as"]:
        full_system += f"\n\nNisama is currently speaking with: {profile['known_as']}. Always address this person as {profile['known_as']}."
    else:
        full_system += f"\n\nNisama does not know this person's name yet. Refer to them as 'one' until they introduce themselves."
    if global_context:
        full_system += f"\n\n{global_context}"

    # Check if this is the first message after an update
    update_notice = ""
    if not has_seen_update(user_id, CHANGELOG_VERSION):
        update_notice = get_update_notice()
        mark_update_seen(user_id, CHANGELOG_VERSION)

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
            reply = "Holie: *Right so uhh. Nisama is currently not in contact, please try again later time bud.*"
            error_occurred = True

    if not error_occurred:
        save_message(user_id, "assistant", reply)

    if len(reply) > 2000:
        reply = reply[:1997] + "..."

    # Send update notice first if applicable
    if update_notice and not error_occurred:
        await message.channel.send(update_notice)

    await message.channel.send(reply)

    # Process bot commands (needed for commands.Bot)
    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_TOKEN"))