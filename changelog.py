CHANGELOG_VERSION = "v1.3.0"
PREVIOUS_VERSION = "v1.2.4"

CHANGELOG = """
**Nisama v1.3.0 Changelog**

**Sentient Conversations**
**— Nisama has officially become more sentient!**
This is by far the biggest update Nisama has ever received. Instead of only waiting for someone else to send the first message, Nisama can now naturally decide when she feels like reaching out on her own. Nisama now considers your previous conversations, chat activity, current memories, time of day, her own mood and energy, ongoing life events, and many other contextual factors before deciding whether it feels natural to start a conversation. The goal has always been simple: make Nisama feel less like a chatbot and more like someone who genuinely remembers, thinks, and cares.

**Massive Lore Expansion**
**— Project-Nova by Jerson.EXE.**
New character information, current-life events, worldbuilding, encyclopedia support, and future story foundations have all been greatly expanded. Check `/lore` for that.

**Performance & Infrastructure**
**— A major rebuild on the back-end of Nisama for improvement.**
A significant portion of this update focused on rebuilding internal systems for greater reliability, scalability, and future expansion.

**Smarter Memory & Personality**
**— Nisama now remembers, understands, and behaves more naturally than ever before.**
Memory, personality, and internal reasoning have all been refined to create a more believable long-term conversational experience.

— Updated Nisama's current-life lore with recent events surrounding New Hant City
— Added `/sentient` slash command for managing proactive conversations
— Added proactive conversations powered by contextual reasoning — Nisama considers previous conversations, memories, personality, mood, and recent activity before reaching out
— Added mood, energy, chat pattern, time-of-day, and conversation awareness to help Nisama naturally decide when and how to reach out
— Added personalized follow-up behavior that considers previous conversations and unanswered messages
— Added persistent sentient conversation preferences and tracking for every user
— Added automatic background scheduler continuously monitoring when proactive conversations feel appropriate
— Massively expanded Project-Nova lore with new worldbuilding, character profiles, current-life events, and encyclopedia foundations
— Updated `/lore` to support significantly larger lore collections with improved browsing and interactive navigation
— Improved overall project architecture to better support large-scale Nisama features
— Improved Nisama's long-term memory and contextual reasoning for more natural conversations
— Improved interaction between memories, personality, mood, lore, and sentient conversations
— Improved conversation history depth to better understand previous interactions and maintain conversational continuity
— Improved background processing, task scheduling, and backend responsiveness for smoother long-term operation
— Improved database reliability and startup initialization for memories, personalities, and sentient conversations
— Improved embed layouts and interactive slash command interfaces for a cleaner, more consistent user experience
— Fixed bug where update notifications delayed normal message responses until they disappeared
— Fixed bug where Nisama could incorrectly handle stream activity inside monitored voice channels
— Fixed bug where conversation state tracking could become inaccurate during extended runtime
— Fixed bug where conversations could behave inconsistently after reconnects or restarts
— Fixed bug where internal memory synchronization could occasionally become inconsistent after background updates
— Fixed bug where newly initialized databases required unnecessary manual preparation before full functionality was available
— Fixed bug where certain database operations were more prone to failure during fresh deployments
— Fixed bug where internal task handling could leave legacy background processes running longer than intended
— Fixed bug where several legacy systems were incompatible with Nisama's new autonomous conversation framework
— Fixed bug where deprecated internal systems could interfere with newer background features
— Fixed bug where multiple backend edge cases could reduce long-term runtime stability
"""