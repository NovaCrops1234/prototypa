CHANGELOG_VERSION = "v1.2.2"
PREVIOUS_VERSION = "v1.2.1"

CHANGELOG = """
**Nisama v1.2.2 Changelog**

**Ultimate Tic Tac Toe**
**— Tic Tac Toe has evolved into Ultimate Tic Tac Toe!**
The original TTT has been replaced with a much cooler, way more interesting UTT for Nisama. Hopefully this brings more enjoyment and a unique feel to it for everyone!

**More Discord Slash Commands**
**— More flexible Discord interactions!**
The message delivery command has been simplified to `/send`, and it can now deliver messages more reliably using either direct mentions or Discord user IDs. A new `/lore` command has also been introduced as the foundation for a future in-depth Nisama lore encyclopedia.

— Updated Nisama's current-life lore with recent events surrounding New Hant City
— Fixed bug where /tictactoe could display "Application did not respond" despite the game functioning correctly
— Fixed bug where /send could successfully deliver messages while Discord incorrectly reported the interaction as failed
— Fixed bug where redundant database initialization queries were executed during normal operation
— Fixed bug where unused legacy backend logic remained after previous system migrations
— Fixed bug where leftover backend code from earlier versions unnecessarily increased project complexity
— Fixed bug where internal database transactions performed unnecessary commit operations before executing queries
— Improved /send to support both Discord mentions and user IDs for more flexible message delivery
— Improved backend database initialization and removed redundant legacy logic
"""