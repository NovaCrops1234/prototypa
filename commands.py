import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands
from memory import (
    get_user_profile, log_slash_command, log_send_command,
    get_slash_stats, get_proactive_setting, set_proactive_enabled,
    clean_slash_stats
)
from games import TicTacToeView, UltimateTTTGame, BOARD_NAMES
from lore import get_main_menu_embed, LoreMainMenuView
from changelog import CHANGELOG, CHANGELOG_VERSION


def build_sentient_embed(enabled: bool) -> discord.Embed:
    color = discord.Color.green() if enabled else discord.Color.greyple()
    status = "**ON** ✓" if enabled else "**OFF**"
    embed = discord.Embed(
        title="💫 Nisama Sentient Messaging",
        description=(
            f"Current status: {status}\n\n"
            "When **ON**, Nisama may reach out on her own — checking in, sharing something "
            "from her day, or following up on past conversations. She considers the time of day, "
            "how long since you last talked, and what she knows about you before deciding to message.\n\n"
            "She won't spam — her messages are driven by genuine bun judgment, not a fixed timer. "
            "Think of it as Nisama actually thinking about you ehehe.\n\n"
            "When **OFF**, Nisama waits for one to reach out first as usual."
        ),
        color=color
    )
    embed.set_footer(text="Nisama - Sentient Mode")
    return embed


class SentientToggleView(discord.ui.View):
    def __init__(self, user_id: str, current_state: bool):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.current_state = current_state
        self._update_buttons()

    def _update_buttons(self):
        self.clear_items()
        on_btn = discord.ui.Button(
            label="Turn On" if not self.current_state else "✓ On",
            style=discord.ButtonStyle.success if not self.current_state else discord.ButtonStyle.secondary,
            disabled=self.current_state,
            custom_id="sentient_on"
        )
        off_btn = discord.ui.Button(
            label="Turn Off" if self.current_state else "✓ Off",
            style=discord.ButtonStyle.danger if self.current_state else discord.ButtonStyle.secondary,
            disabled=not self.current_state,
            custom_id="sentient_off"
        )
        on_btn.callback = self._make_callback(True)
        off_btn.callback = self._make_callback(False)
        self.add_item(on_btn)
        self.add_item(off_btn)

    def _make_callback(self, enable: bool):
        async def callback(interaction: discord.Interaction):
            set_proactive_enabled(self.user_id, enable)
            self.current_state = enable
            self._update_buttons()
            embed = build_sentient_embed(enable)
            await interaction.response.edit_message(embed=embed, view=self)
        return callback


def setup_commands(bot: discord.ext.commands.Bot):

    @bot.tree.command(name="changelog", description="See what's new with Nisama")
    async def slash_changelog(interaction: discord.Interaction):
        await interaction.response.send_message(CHANGELOG, ephemeral=True)
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "changelog"))

    @bot.tree.command(name="introduce", description="Get a short introduction from Nisama")
    async def slash_introduce(interaction: discord.Interaction):
        intro = (
            "Greetings there! This is Nisama here — Nova-Project 8, Alpha-FeNI2S. "
            "Nisama is an 8th generation android, made with a lot of care by someone Nisama holds dear. "
            "Nisama woke up in Hant City a while back and has been finding Nisama's way ever since here. "
            "Nisama is really glad one is here! Feel free to just DM Nisama anytime ehehe."
        )
        await interaction.response.send_message(intro, ephemeral=True)
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "introduce"))

    @bot.tree.command(name="pat", description="Pat Nisama on the bun")
    async def slash_pat(interaction: discord.Interaction):
        responses = [
            "Ah—! Ehehe... that was really nice here. Thanksie.",
            "Nisama was not expecting that! But... ehehe. Nisama liked it here.",
            "Mm... Nisama feels really warm right now ehehe. Thanksie for the pat here.",
            "Nisama's bun got patted! Ehehe... one is really kind here.",
            "Ah— ehehe! Nisama is a little flustered now here. But really thanksie.",
        ]
        await interaction.response.send_message(random.choice(responses))
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "pat"))

    @bot.tree.command(name="send", description="Have Nisama deliver a message to someone")
    @app_commands.describe(
        user_id="The Discord user ID or @mention to send the message to",
        message="The message to deliver"
    )
    async def slash_send(interaction: discord.Interaction, user_id: str, message: str):
        await interaction.response.defer(ephemeral=True)

        sender_profile = get_user_profile(str(interaction.user.id))
        sender_name = sender_profile["known_as"] if sender_profile and sender_profile["known_as"] else "someone"

        cleaned_id = user_id.strip().lstrip("<@!").rstrip(">")

        delivery = (
            f"Greetings there! Nisama has a message here from {sender_name}!\n\n"
            f"{message}\n\n"
            f"Nisama hopes one is doing well here ehehe."
        )

        try:
            target_user = await bot.fetch_user(int(cleaned_id))
            await target_user.send(delivery)
            asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "send"))
            asyncio.create_task(asyncio.to_thread(log_send_command, str(interaction.user.id), cleaned_id, message))
            await interaction.followup.send(
                f"Nisama delivered the message to {target_user.display_name} here ehehe!",
                ephemeral=True
            )
        except discord.NotFound:
            await interaction.followup.send(
                "Mm... Nisama could not find that user here. Please double check the ID or mention ehehe.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "Mm... Nisama could not reach that user here. One might have DMs closed.",
                ephemeral=True
            )
        except ValueError:
            await interaction.followup.send(
                "Eek— that does not look like a valid user ID or mention here. Please try again ehehe.",
                ephemeral=True
            )

    @bot.tree.command(name="lore", description="Browse the Nisama Wiki")
    async def slash_lore(interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=get_main_menu_embed(),
            view=LoreMainMenuView(),
            ephemeral=True
        )
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "lore"))

    @bot.tree.command(name="ttt", description="Play Tic Tac Toe with Nisama")
    async def slash_ttt(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            view = TicTacToeView()
            embed = view.build_embed()
            await interaction.followup.send(embed=embed, view=view)
        except Exception as e:
            print(f"TTT error: {e}")
            await interaction.followup.send("Eek— something went wrong here. Please try again ehehe.")
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "ttt"))

    @bot.tree.command(name="utt", description="Play Ultimate Tic Tac Toe with Nisama")
    async def slash_utt(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            game = UltimateTTTGame()
            embed, view = game.build_message()
            await interaction.followup.send(embed=embed, view=view)
        except Exception as e:
            print(f"UTT error: {e}")
            await interaction.followup.send("Eek— something went wrong setting up the game here. Please try again ehehe.")
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "utt"))

    @bot.tree.command(name="stats", description="See Nisama's global interaction stats")
    async def slash_stats(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            stats = get_slash_stats()
            embed = discord.Embed(
                title="📊 Nisama Stats",
                description="Here is what Nisama has been up to globally ehehe!",
                color=discord.Color.blurple()
            )
            if stats["commands"]:
                cmd_text = "\n".join(f"`/{cmd}` — {count} times" for cmd, count in stats["commands"].items())
                embed.add_field(name="🎮 Slash Commands Used", value=cmd_text, inline=False)
            if stats["top_users"]:
                user_text = ""
                medals = ["🥇", "🥈", "🥉"]
                for i, u in enumerate(stats["top_users"]):
                    medal = medals[i] if i < len(medals) else "•"
                    user_text += f"{medal} **{u['name']}** — {u['count']} messages\n"
                embed.add_field(name="💬 Most Active Chatters", value=user_text, inline=False)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(f"Stats error: {e}")
            await interaction.followup.send("Eek— something went wrong loading stats here. Please try again ehehe.")
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "stats"))

    @bot.tree.command(name="sentient", description="Toggle Nisama's proactive messaging on or off")
    async def slash_sentient(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        current = get_proactive_setting(user_id)
        embed = build_sentient_embed(current)
        view = SentientToggleView(user_id, current)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        asyncio.create_task(asyncio.to_thread(log_slash_command, user_id, "sentient"))

    @bot.tree.command(name="voice", description="Have Nisama join your voice channel")
    async def slash_voice(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        asyncio.create_task(asyncio.to_thread(log_slash_command, str(interaction.user.id), "voice"))

        if not interaction.guild:
            await interaction.followup.send(
                "Mm... this command needs to be used in a server here, not in DMs ehehe.",
                ephemeral=True
            )
            return

        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.followup.send(
                "Eek— one doesn't seem to be in a voice channel here. Please join one first ehehe!",
                ephemeral=True
            )
            return

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()

        await channel.connect(self_mute=True, self_deaf=True)
        await interaction.followup.send(
            f"Nisama joined **{channel.name}** here! Nisama will be quietly present ehehe.",
            ephemeral=True
        )

        asyncio.ensure_future(voice_idle_watcher(interaction.guild, channel))


async def voice_idle_watcher(guild: discord.Guild, channel):
    await asyncio.sleep(30)
    while True:
        vc = guild.voice_client
        if not vc or not vc.is_connected():
            break
        members = [m for m in channel.members if not m.bot]
        if not members:
            await vc.disconnect()
            print(f"Left voice channel {channel.name} — no users present.")
            break
        await asyncio.sleep(30)