CHANGELOG_VERSION = "v1.2.3"
PREVIOUS_VERSION = "v1.2.2"

CHANGELOG = """
**Nisama v1.2.3 Changelog**

**Better Games & Global Statistics**
**— Better TTT and UTT experience with Nisama!**
The last rendition of UTT with Nisama wasn't the best experience at all, so time was spent improving it to be cleaner than before. Neither fully satisfied nor unsatisfied with the current one — it's better than the last, and a further improved version may come in the near future. The original TTT has also been added back for convenience. A big update toward Nisama's behaviour is being prepared for v1.3, so stay tuned!

**More Discord Slash Commands**
**— Added `/stats` slash command to view global slash command usage and Nisama's most active friend :)**
Shows the stats of Nisama's usage activity — pretty neat if one is curious about what's been going on!

— Updated Nisama's current-life lore with recent events surrounding New Hant City
— Highly improved both TTT and UTT with cleaner embed-based interfaces
— Renamed `/tictactoe` to `/utt` for clearer game selection
— Added paginated UTT move history with persistent match logs
— Improved UTT board clarity with clearer active board indicators and overall gameplay flow
— Fixed bug where `/send` interactions were not recorded in the database
— Fixed bug where `/send` could fail when targeting users through Discord mentions
— Fixed bug where UTT matches did not preserve move history after gameplay progressed
— Fixed bug where UTT board progression could become difficult to follow during matches
— Fixed bug where `/lore` still used the older synchronous logging method instead of the newer asynchronous logging system
"""