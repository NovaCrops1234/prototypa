CHANGELOG_VERSION = "v1.2.0"

CHANGELOG = """
**Nisama v1.2.0 Changelog**

**Discord Slash Commands**
**— Nisama now supports Discord slash commands!**
Nisama has learned a brand new way to interact through Discord's built-in slash commands! Simply type `/` to discover available interactions.

Current commands include:
- `/introduce` — Learn more about Nisama and who she is.
- `/changelog` — View the latest update notes.
- `/pat` — Give Nisama a gentle bun pat and see how she reacts!

More slash commands and interactive features are planned for future updates.

**— Major migration from `discord.Client` to `commands.Bot` for improved long-term scalability**
— Fixed bug where previous changelog delivery relied on outdated broadcast logic instead of a per-user update notification system
— Fixed bug where leftover legacy code and redundant imports remained after previous backend migrations
— Fixed bug where slash command support was unavailable due to the previous Discord client architecture
— Fixed bug where update notifications could not be tracked individually for each user across different Nisama versions
— Improved overall backend organization by separating version and changelog management into dedicated modules
— Improved code maintainability through cleanup of legacy logic, redundant imports, and unused components
— Improved project scalability to better support future systems such as additional slash commands, utilities, and interactive features
— Improved Discord integration by fully adopting Discord's modern interaction framework
"""