CHANGELOG_VERSION = "v1.2.4"
PREVIOUS_VERSION = "v1.2.3"

CHANGELOG = """
**Nisama v1.2.4 Changelog**

**More Discord Slash Commands**
**— Added `/voice` slash command as the first step toward future voice interaction support, with automatic voice channel idle detection to prepare for auto-disconnect behavior.**
Development has officially started toward making Nisama feel much more alive. While the full feature won't be available until v1.3, this update introduces the foundation for the so called sentient conversations which would allow Nisama to naturally reach out on her own instead of always waiting for someone else to start the conversation, which is pretty insane.

Another foundation also implemented on the voice interactions. While voice conversations themselves are still planned for a later update, the groundwork is now being built so Nisama can eventually join voice channels and unleash the joyful message to all.

— Updated Nisama's current-life lore with recent events surrounding New Hant City
— Added backend foundation for Nisama's upcoming proactive conversation system planned for v1.3
— Improved update notifications by automatically removing them after a short period to reduce chat clutter
— Fixed bug where newly created databases required manual SQL setup before Nisama could function correctly
— Fixed bug where missing database tables could cause startup errors during profile and memory operations
— Fixed bug where `/stats` continued displaying deprecated slash commands after they had been removed
— Fixed bug where TTT and UTT used reversed victory colors for player and Nisama wins
— Fixed bug where the initial `/voice` implementation could not establish voice connections due to missing voice dependencies
"""