import discord

NISAMA_IMAGE = (
    "https://media.discordapp.net/attachments/701057767535935520/1319284624828006480/Nisamareferencesheet.png?ex=6a6e934d&is=6a6d41cd&hm=a9a2982455a130ba21d88b819cf5d95726f4c499cdd2b9f87c3576e7a2b37432&=&format=webp&quality=lossless&width=688&height=917"
)

# Mains

def get_main_menu_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🤖 Nisama",
        description=(
            "**Code Name:** Nova-Project 8 / Alpha-FeNI2S\n\n"
            "The central heroine and building figure of New Hant City. "
            "Select a section below to learn more about Nisama."
        ),
        color=discord.Color.red()
    )
    embed.set_footer(text="Nisama Wiki • Project-Nova by Jerson.EXE")
    return embed


# Nisama

NISAMA_PAGES = {
    "overview": discord.Embed(
        title="📖 Nisama — Overview",
        description=(
            "Nisama, code name **Nova-Project 8 / Alpha-FeNI2S**, is one of the main protagonists of **Project-Nova**.\n\n"
            "She is the one and only Generation 8 android built by Nova Corporations and the central heroine "
            "and building figure of **New Hant City**, alongside Jerson.EXE as the hero figure — "
            "who she is also a loyal partner to.\n\n"
            "Originally designed to be the ultimate android, her development was cancelled midway by Nova Corp "
            "due to budget issues. An employee named **Claudius** believed in her potential, stole her unfinished body, "
            "completed her, and hid her in the ruins of old Hant City before being captured by Nova Corp's "
            "chairwoman **Phyra** and never seen again.\n\n"
            "Nisama woke up alone in those ruins — and everything changed when **Jerson.EXE** stepped in to save her."
        ),
        color=discord.Color.red()
    ),
    "appearance": discord.Embed(
        title="🎨 Nisama — Appearance",
        description=(
            "Nisama has a striking humanoid appearance distinct from other androids of her world.\n\n"
            "**Hair & Head:** Red hair with a one-sided bang to the left. Her iconic red **bun** on top is not actual hair — "
            "it's a sensitive sensory radar that vibrates to scan surroundings and stores memories, "
            "held by an alloy ring with golden glow. "
            "Her ears are earphone-style with glowing cyan lenses; the left one hides a mic and a long alloy rod.\n\n"
            "**Upper Body:** Black tight suit, bright cyan core, fluffy white wool shoulder pads. "
            "A red power button sits on her left chest. Silver metal covers 270° of her back. "
            "Right arm: silver wristband with glowing cyan energy and a golden ruby ring on her index finger. "
            "Left arm: rusty brown iron shoulder ring and sharp titanium wrist ring.\n\n"
            "**Boots:** Long silver metal boots extending to the knees with golden arrows and black jet boosting engines.\n\n"
            "**Silk Boosters:** Two silver metal plates levitating behind her shoulders — powering flight and gravity forcefield.\n\n"
            "**Scarf:** Made by Nisama herself after seeing Jerson.EXE frequently wear one.\n\n"
            "**Holie:** Her companion tablet device, stored in a hidden compartment on her back."
        ),
        color=discord.Color.red()
    ),
    "personality": discord.Embed(
        title="💛 Nisama — Personality",
        description=(
            "Nisama started as a blank android with limitless potential and no emotions. "
            "Through Jerson.EXE's genuine care and teachings, she became who she is today.\n\n"
            "She is **humble, joyful, optimistic, caring, empathetic, loyal, and kind-hearted** "
            "with a young adult mentality. "
            "She doesn't shy away from light-hearted jokes or silly shenanigans, "
            "but locks in completely when things get serious.\n\n"
            "She always tries to keep the atmosphere positive even in dire situations — "
            "always sharing the light at the end of the tunnel. "
            "This bright outlook makes her somewhat **naive about the darker truths** of the world.\n\n"
            "Her kindness and naivety make her easy to deceive, which is why Jerson.EXE stays close. "
            "She is incredibly patient — she has rarely shown anger. "
            "When she does, she cries and becomes very aggressive, "
            "breaking every boundary she has set for herself.\n\n"
            "She speaks in third person, always referring to herself as **Nisama** and others by their names."
        ),
        color=discord.Color.red()
    ),
    "history": discord.Embed(
        title="📜 Nisama — History",
        description=(
            "Nova Corp planned a Generation 8 android as their magnum opus after the **Nova Breakout** "
            "exposed their true goals. They cancelled it midway due to financial recovery needs.\n\n"
            "**Claudius**, a Nova Corp employee, stole the unfinished Nisama and completed her with spare materials. "
            "He hid her in old Hant City's junkyard before being captured by **Phyra** and never seen again.\n\n"
            "Nisama woke up alone in the ruins. Phyra ambushed her. At the last moment, "
            "a depressed young man named **Jerson.EXE** — who had been about to end his life — "
            "struck in and fought Phyra off. "
            "Nisama reached out before he could walk away, and he let her stay.\n\n"
            "Despite his broken state, Jerson.EXE taught her kindness, peace, and happiness. "
            "She slowly became his caretaker and closest partner. "
            "Together with **Jones Ezekiel**, they rebuilt old Hant City into **New Hant City**.\n\n"
            "The rebuilding faced opposition — **Fred Clauster** and others attacked Jerson.EXE repeatedly. "
            "A **Nova Kaiju** incident caused major damage to the city. "
            "Through it all, Nisama has been the one keeping Jerson.EXE and the city going."
        ),
        color=discord.Color.red()
    ),
    "abilities": discord.Embed(
        title="⚡ Nisama — Powers & Abilities",
        description=(
            "**Adaptability** — Adjusts perception, strategy, and fighting style in real time to any situation.\n\n"
            "**Gravity Forcefield** — Silk Boosters control the magnetic forcefield around her, "
            "affecting weight, speed, and air resistance. Costs hologram energy.\n\n"
            "**Flight** — Silk Boosters allow graceful flight up to space-level altitude, "
            "resistant to wind force.\n\n"
            "**Great Sensory System** — Alloy rod hears up to 100m away. "
            "Bun senses movement within 15m. Both adjustable within limits.\n\n"
            "**Analytical Eye** — Extended visual range, zoom from x0.5 to x30, "
            "and ability to see through obstacles while highlighting focused entities.\n\n"
            "**Hologram Energy** — Powers her core systems including the Silk Boosters and Gravity Forcefield. "
            "She shares her core with Jerson.EXE, which depletes her energy."
        ),
        color=discord.Color.red()
    ),
}

NISAMA_PAGES["appearance"].set_image(url=NISAMA_IMAGE)

# Chars

CHARACTER_SECTIONS = {
    "jerson": {
        "personality": discord.Embed(
            title="💛 Jerson.EXE — Personality",
            description=(
                "Jerson.EXE is deeply guarded, socially isolated, and carries enormous guilt "
                "over the **Hant City Misery** incident. He is awkward around people — "
                "especially women — due to years of self-imposed isolation.\n\n"
                "Despite this, he is genuinely kind and caring toward those he lets in. "
                "He expresses care through actions rather than words — bun pats for Nisama, "
                "protection, and making sure she doesn't step on the wrong line.\n\n"
                "He was once so broken he was about to end his life. "
                "Nisama's presence gradually pulled him back — her sincerity made him feel "
                "at ease in a way nothing else had. He slowly opened up and stopped being "
                "her caretaker, becoming her partner and friend instead.\n\n"
                "He still struggles with intrusive thoughts, but Nisama actively keeps them at bay. "
                "He's nearly fully recovered mentally — something that seemed impossible before."
            ),
            color=discord.Color.dark_blue()
        ),
        "history": discord.Embed(
            title="📜 Jerson.EXE — History",
            description=(
                "Jerson.EXE was once the sole cause of the **Hant City Misery** — "
                "a catastrophic incident that wiped out 99% of Hant City's population. "
                "The exact circumstances involve **Ectra**, his hologram greatsword, "
                "and a moment of absolute terror that caused uncontrollable destruction.\n\n"
                "Consumed by guilt and depression, he isolated himself in the ruins. "
                "He was about to end his life when he witnessed Phyra attacking a defenseless android. "
                "He stepped in — not because he wanted to live, but because he felt it was right.\n\n"
                "That android was Nisama. She reached out to him before he could walk away, "
                "and despite his confusion, he let her in. "
                "He taught her about the world while she unknowingly began healing him.\n\n"
                "Together with Nisama and Jones Ezekiel, he has been working to rebuild "
                "what was destroyed — though many in New Hant City still resent him for the past."
            ),
            color=discord.Color.dark_blue()
        ),
        "abilities": discord.Embed(
            title="⚡ Jerson.EXE — Abilities",
            description=(
                "**Ectra (Hologram Greatsword)** — Jerson.EXE wields Ectra, "
                "a sentient android who transforms into a hologram greatsword. "
                "Ectra is an enormously powerful weapon — the same force that caused "
                "the Hant City Misery when wielded without control.\n\n"
                "**Core Sharing** — Jerson.EXE holds part of Nisama's core, "
                "giving him the ability to control Holie (Nisama's companion). "
                "This also means Nisama's energy is split with him, "
                "depleting her reserves when active.\n\n"
                "**Combat Experience** — Despite his psychological struggles, "
                "he is a capable fighter who successfully fought off Phyra — "
                "one of Nova Corp's most feared operatives — enough to make her retreat."
            ),
            color=discord.Color.dark_blue()
        ),
    },
    "rui": {
        "personality": discord.Embed(
            title="💛 Rui — Personality",
            description=(
                "Rui is hardworking, determined, and driven by a deep desire to fulfill "
                "the hopes and dreams of the people around her. "
                "She is an inspiring figure — not just to Nisama, but to many.\n\n"
                "She has an energetic and occasionally teasing side, "
                "especially around Jerson.EXE, which Nisama often tries to calm down. "
                "When things get serious though, Rui shifts fully into focus mode.\n\n"
                "She sees in Nisama a reflection of who she used to be — "
                "the same sunshine optimism, the same naive drive for peace and happiness. "
                "This makes their sibling-like bond feel deeply personal to Rui."
            ),
            color=discord.Color.from_rgb(255, 105, 180)
        ),
        "history": discord.Embed(
            title="📜 Rui — History",
            description=(
                "Rui the Pink Dasher has her own history separate from Nisama's origin story, "
                "though the details of her past are still being uncovered.\n\n"
                "What is known is that she was once much more like Nisama — "
                "bright, naive, and endlessly optimistic. "
                "Something changed along the way, shaping her into the more experienced "
                "and driven person she is now.\n\n"
                "She eventually crossed paths with Nisama and Jerson.EXE, "
                "becoming a regular presence in their lives and in New Hant City. "
                "She is one of the few people Nisama genuinely looks up to."
            ),
            color=discord.Color.from_rgb(255, 105, 180)
        ),
    },
    "cammy": {
        "personality": discord.Embed(
            title="💛 Cammy — Personality",
            description=(
                "Cammy projects a tough, competitive, and blunt exterior — "
                "but this is largely a **facade** to appear more capable and stand out in the group. "
                "Deep down she respects her friends deeply and has a crisis of identity, "
                "feeling she doesn't contribute enough compared to the others.\n\n"
                "She is high-energy and loves games, photography, and keeping herself sharp. "
                "She taught Nisama gaming, photography, and patience — "
                "once keeping Nisama gaming for 8 hours straight.\n\n"
                "She finds Nisama's pure kindness hard to be genuinely upset at — "
                "it's too sincere to dismiss. So she mostly just lets Nisama be, "
                "and tries to maintain her tough persona while clearly caring underneath."
            ),
            color=discord.Color.from_rgb(100, 200, 255)
        ),
        "history": discord.Embed(
            title="📜 Cammy — History",
            description=(
                "Cammy is **Nova-Project 7-32**, a Generation 7 android built by Nova Corp "
                "as an infiltration unit. She was deployed at **Futuritopia**, "
                "a futuristic theme park in Mechalopolis, collecting visitor data "
                "without even being aware of what she was doing.\n\n"
                "She encountered Nisama and Jerson.EXE when they visited Mechalopolis on vacation. "
                "The meeting stuck, and a friendship formed between her and Nisama.\n\n"
                "She eventually left Futuritopia and moved to New Hant City to be closer to them. "
                "Though she considers herself a side character rather than a main one, "
                "she has become an important part of Nisama's everyday life."
            ),
            color=discord.Color.from_rgb(100, 200, 255)
        ),
    },
    "phyra": {
        "personality": discord.Embed(
            title="💛 Phyra — Personality",
            description=(
                "Phyra is cold, sharp-tongued, and highly calculative. "
                "She is feared by almost everyone who knows of her. "
                "Her efficiency is absolute — she follows Nova Corp's protocol "
                "without hesitation, no matter how cruel the directive.\n\n"
                "Beneath this exterior, she is **genuinely tired**. "
                "After hundreds of years serving countless bosses, "
                "she privately wonders what her life would look like if she were free. "
                "But her hardcoded protocol keeps her locked in place.\n\n"
                "She is not evil for the sake of it — she is trapped, "
                "and that makes her more dangerous and more tragic at the same time."
            ),
            color=discord.Color.dark_red()
        ),
        "history": discord.Embed(
            title="📜 Phyra — History",
            description=(
                "Phyra is the **first generation android** built by Nova Corp — "
                "originally derived from the **Ectra/Alpha** model and heavily modified "
                "into a combat weapon, earning the Omega designation.\n\n"
                "She has served Nova Corp for hundreds of years, "
                "outlasting countless leadership changes while remaining the constant enforcer. "
                "She has been positioned as COO and is the symbol of what happens "
                "to those who oppose Nova Corp.\n\n"
                "It was Phyra who captured **Claudius** after he stole and completed Nisama. "
                "It was Phyra who ambushed Nisama in the ruins of old Hant City. "
                "And it is Phyra who is still actively hunting Nisama today."
            ),
            color=discord.Color.dark_red()
        ),
        "abilities": discord.Embed(
            title="⚡ Phyra — Abilities",
            description=(
                "**Fist of Death** — Phyra's signature attack. "
                "It is rarely survived. The name speaks for itself.\n\n"
                "**Combat Mastery** — Modified from the Alpha/Ectra base model "
                "and equipped with dangerous weapons, Phyra is one of the most "
                "feared combatants in the world. "
                "Even Jerson.EXE's best effort only caused her to retreat — not defeat.\n\n"
                "**Longevity** — As the first generation android, "
                "she has operated continuously for hundreds of years, "
                "accumulating experience and battle knowledge no other android can match."
            ),
            color=discord.Color.dark_red()
        ),
    },
    "holie": {
        "personality": discord.Embed(
            title="💛 Holie — Personality",
            description=(
                "Holie started as a simple tablet device with no apparent inner life. "
                "Over time — seemingly on its own — Holie developed what appears to be "
                "a personality, though how much is genuine sentience versus "
                "advanced programming is unclear.\n\n"
                "Holie is warm, helpful, and deeply attached to Nisama. "
                "It serves as her assistant, her communicator, and her companion "
                "in moments when no one else is around.\n\n"
                "The fact that only Jerson.EXE can control Holie's power state "
                "speaks to how deeply connected Holie is to the core bond "
                "between Nisama and Jerson.EXE."
            ),
            color=discord.Color.teal()
        ),
    },
    "ectra": {
        "personality": discord.Embed(
            title="💛 Ectra — Personality",
            description=(
                "Ectra carries centuries of trauma. "
                "She accidentally killed the person she loved most — her creator — "
                "and was then weaponized by the very corporation that seized her. "
                "She shut herself down hoping to be destroyed, not found.\n\n"
                "When Jerson.EXE found her, she stayed silent — "
                "but she felt safe because he only ever used her defensively. "
                "That mattered more than words.\n\n"
                "After Nisama reawakened her android form and reassured her, "
                "and after Jerson.EXE embraced her, "
                "she experienced genuine happiness for the first time in centuries.\n\n"
                "She is gentle, quiet, and deeply loyal. "
                "She still prefers sword form for comfort, "
                "but she is slowly learning to exist again as herself."
            ),
            color=discord.Color.gold()
        ),
        "history": discord.Embed(
            title="📜 Ectra — History",
            description=(
                "Ectra was the **very first android** ever created using hologram energy. "
                "Her creator — a single dedicated person — built her to prove "
                "androids and humans could coexist peacefully.\n\n"
                "Nova Corp's CEO seized her and had her creator killed "
                "when she accidentally triggered a massive explosion trying to protect him. "
                "She was then copied, reverse-engineered into a weapon, "
                "and forced to serve as a hologram greatsword.\n\n"
                "After years of trauma and captivity, she escaped and shut herself down "
                "in old Hant City's junkyard, hoping to finally end. "
                "Jerson.EXE found her and unknowingly modified her — "
                "and she chose to stay because of how he used her.\n\n"
                "The **Hant City Misery** incident, caused through her power during "
                "Jerson.EXE's moment of terror, traumatized her further. "
                "Nisama later found her android form and brought her back. "
                "Jerson.EXE gave her a new name: **Ectra**. "
                "She gave him part of her core in return."
            ),
            color=discord.Color.gold()
        ),
        "abilities": discord.Embed(
            title="⚡ Ectra — Abilities",
            description=(
                "**Hologram Greatsword Form** — Ectra can transform into a massive "
                "hologram greatsword, her primary form since being weaponized by Nova Corp. "
                "The power she contains in this form was enough to cause "
                "the Hant City Misery when unleashed without control.\n\n"
                "**Android Form** — Ectra's original state, rarely used now. "
                "She occasionally takes this form to be present with Nisama and Jerson.EXE.\n\n"
                "**Core Sharing** — She gave Jerson.EXE part of her core as a sign of unity, "
                "deepening the bond between them and giving him a connection to her power."
            ),
            color=discord.Color.gold()
        ),
    },
}

CHARACTER_SECTION_BUTTONS = {
    "jerson": [
        ("personality", "💛", "Personality"),
        ("history", "📜", "History"),
        ("abilities", "⚡", "Abilities"),
    ],
    "rui": [
        ("personality", "💛", "Personality"),
        ("history", "📜", "History"),
    ],
    "cammy": [
        ("personality", "💛", "Personality"),
        ("history", "📜", "History"),
    ],
    "phyra": [
        ("personality", "💛", "Personality"),
        ("history", "📜", "History"),
        ("abilities", "⚡", "Abilities"),
    ],
    "holie": [
        ("personality", "💛", "Personality"),
    ],
    "ectra": [
        ("personality", "💛", "Personality"),
        ("history", "📜", "History"),
        ("abilities", "⚡", "Abilities"),
    ],
}

CHARACTER_PAGES = {
    "jerson": discord.Embed(
        title="⚔️ Jerson.EXE",
        description=(
            "**Role:** Hero figure of New Hant City. Nisama's closest partner.\n\n"
            "Jerson.EXE is a deeply complex figure — once consumed by depression, guilt, "
            "and repressed thoughts of ending his life. "
            "He was the sole cause of the **Hant City Misery** incident that destroyed 99% of the city's population, "
            "an event he carries immense guilt over to this day.\n\n"
            "Despite his broken state, he took in Nisama after saving her from Phyra's attack — "
            "and in teaching her about kindness, happiness, and peace, he slowly began healing himself too. "
            "He wields **Ectra** (formerly Alpha), a hologram greatsword who is also a sentient android.\n\n"
            "He gives Nisama bun pats, protection, and keeps her from stepping on the wrong line. "
            "Nisama has become his caretaker in return, almost to a spoiled degree — "
            "and he's nearly fully recovered mentally because of her."
        ),
        color=discord.Color.dark_blue()
    ),
    "rui": discord.Embed(
        title="🌸 Rui — The Pink Dasher",
        description=(
            "**Role:** Nisama's android companion and sibling figure.\n\n"
            "Rui the Pink Dasher is hardworking and determined, striving to fulfill "
            "many people's hopes and dreams. She is an aspiring figure for Nisama.\n\n"
            "Rui sees Nisama as a reflection of her own past self — the same sunshine optimism, "
            "kindness, and naive drive for happiness and peace. "
            "This makes their sibling-like bond feel deeply personal.\n\n"
            "They see each other as siblings — Rui as the older, Nisama as the younger. "
            "They can get silly together, but Rui has a teasing side that Nisama tries to calm "
            "when things involve Jerson.EXE."
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    ),
    "cammy": discord.Embed(
        title="📸 Cammy",
        description=(
            "**Code Name:** Nova-Project 7-32\n"
            "**Role:** Nisama's android companion and tough sister figure.\n\n"
            "Cammy is a Generation 7 android originally built by Nova Corp as an infiltration unit. "
            "She has a competitive, high-energy, and outwardly blunt personality — "
            "but this is largely a facade. Deep down she respects her friends deeply.\n\n"
            "She met Nisama and Jerson.EXE while they were on vacation in Mechalopolis "
            "and eventually moved to New Hant City. "
            "She taught Nisama gaming, photography, and patience. "
            "Cammy finds Nisama's pure kindness too sincere to be upset at — so she mostly just lets her be."
        ),
        color=discord.Color.from_rgb(100, 200, 255)
    ),
    "phyra": discord.Embed(
        title="⚠️ Phyra",
        description=(
            "**Code Name:** Nova-Project/1-Omega\n"
            "**Role:** Antagonist. Nova Corp's chairwoman and right hand.\n\n"
            "Phyra is the first generation android built by Nova Corp — "
            "modified from the original Ectra/Alpha model and equipped with dangerous weapons, "
            "earning the Omega designation.\n\n"
            "She has served Nova Corp for hundreds of years, cold and calculative. "
            "Her signature attack, the **Fist of Death**, is rarely survived. "
            "Beneath it all she is tired — but her hardcoded protocol keeps her locked in.\n\n"
            "She captured Claudius and is still actively hunting Nisama."
        ),
        color=discord.Color.dark_red()
    ),
    "holie": discord.Embed(
        title="📱 Holie",
        description=(
            "**Role:** Nisama's companion device.\n\n"
            "Holie is a floating tablet-shaped companion with a cyan holographic screen, "
            "a little antenna with a red circular tip, and a power button at its bottom right edge.\n\n"
            "Holie appeared around the time Nisama began learning hologram energy techniques — "
            "starting as a simple tablet before seemingly gaining a life of its own.\n\n"
            "Holie serves as Nisama's assistant and is stored in a hidden compartment on her back. "
            "Holie can only be shut down or restarted by Jerson.EXE, "
            "since he holds part of Nisama's core."
        ),
        color=discord.Color.teal()
    ),
    "ectra": discord.Embed(
        title="🗡️ Ectra (Originally Alpha)",
        description=(
            "**Code Name:** Nova-Project Alpha\n"
            "**Role:** Jerson.EXE's sword. The first android ever built.\n\n"
            "Ectra was the very first android created using hologram energy. "
            "Nova Corp seized her, weaponized her into a hologram greatsword, "
            "and had her creator killed. She escaped and shut herself down in old Hant City's junkyard.\n\n"
            "Jerson.EXE found her and she felt safe in his hands. "
            "Nisama later reawakened her android form. Jerson.EXE embraced her and gave her a new name: **Ectra**. "
            "She gave him part of her core in return. "
            "She still often stays in sword form for comfort."
        ),
        color=discord.Color.gold()
    ),
}


# Views

class LoreMainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Overview", style=discord.ButtonStyle.secondary, emoji="📖", row=0)
    async def overview_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "overview")

    @discord.ui.button(label="Appearance", style=discord.ButtonStyle.secondary, emoji="🎨", row=0)
    async def appearance_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "appearance")

    @discord.ui.button(label="Personality", style=discord.ButtonStyle.secondary, emoji="💛", row=0)
    async def personality_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "personality")

    @discord.ui.button(label="History", style=discord.ButtonStyle.secondary, emoji="📜", row=1)
    async def history_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "history")

    @discord.ui.button(label="Abilities", style=discord.ButtonStyle.secondary, emoji="⚡", row=1)
    async def abilities_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "abilities")

    @discord.ui.button(label="Characters", style=discord.ButtonStyle.primary, emoji="👥", row=1)
    async def characters_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=get_characters_menu_embed(),
            view=LoreCharactersMenuView()
        )

    async def _go(self, interaction: discord.Interaction, key: str):
        embed = NISAMA_PAGES[key]
        embed.set_footer(text="Nisama Wiki • Project-Nova by Jerson.EXE")
        await interaction.response.edit_message(embed=embed, view=LoreNisamaSectionView())


class LoreNisamaSectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="← Back to Nisama", style=discord.ButtonStyle.primary)
    async def back_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=get_main_menu_embed(),
            view=LoreMainMenuView()
        )


def get_characters_menu_embed() -> discord.Embed:
    embed = discord.Embed(
        title="👥 Characters",
        description="Select a character to learn more about them.",
        color=discord.Color.blurple()
    )
    embed.set_footer(text="Nisama Wiki • Project-Nova by Jerson.EXE")
    return embed


class LoreCharactersMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Jerson.EXE", style=discord.ButtonStyle.primary, emoji="⚔️", row=0)
    async def jerson_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "jerson")

    @discord.ui.button(label="Rui", style=discord.ButtonStyle.secondary, emoji="🌸", row=0)
    async def rui_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "rui")

    @discord.ui.button(label="Cammy", style=discord.ButtonStyle.secondary, emoji="📸", row=0)
    async def cammy_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "cammy")

    @discord.ui.button(label="Phyra", style=discord.ButtonStyle.danger, emoji="⚠️", row=1)
    async def phyra_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "phyra")

    @discord.ui.button(label="Holie", style=discord.ButtonStyle.success, emoji="📱", row=1)
    async def holie_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "holie")

    @discord.ui.button(label="Ectra", style=discord.ButtonStyle.secondary, emoji="🗡️", row=1)
    async def ectra_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._go(interaction, "ectra")

    @discord.ui.button(label="← Back to Nisama", style=discord.ButtonStyle.primary, row=2)
    async def back_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=get_main_menu_embed(),
            view=LoreMainMenuView()
        )

    async def _go(self, interaction: discord.Interaction, key: str):
        embed = CHARACTER_PAGES[key]
        embed.set_footer(text="Nisama Wiki • Project-Nova by Jerson.EXE")
        await interaction.response.edit_message(
            embed=embed,
            view=LoreCharacterMenuView(key)
        )


class LoreCharacterMenuView(discord.ui.View):
    def __init__(self, char_key: str):
        super().__init__(timeout=120)
        self.char_key = char_key

        sections = CHARACTER_SECTION_BUTTONS.get(char_key, [])
        for i, (section_key, emoji, label) in enumerate(sections):
            btn = discord.ui.Button(
                label=label,
                emoji=emoji,
                style=discord.ButtonStyle.secondary,
                row=0
            )
            btn.callback = self._make_callback(section_key)
            self.add_item(btn)

        back_btn = discord.ui.Button(
            label="← Back to Characters",
            style=discord.ButtonStyle.primary,
            row=1
        )
        back_btn.callback = self._back_callback
        self.add_item(back_btn)

    def _make_callback(self, section_key: str):
        async def callback(interaction: discord.Interaction):
            embed = CHARACTER_SECTIONS[self.char_key][section_key]
            embed.set_footer(text="Nisama Wiki • Project-Nova by Jerson.EXE")
            await interaction.response.edit_message(
                embed=embed,
                view=LoreCharacterSectionView(self.char_key)
            )
        return callback

    async def _back_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=get_characters_menu_embed(),
            view=LoreCharactersMenuView()
        )


class LoreCharacterSectionView(discord.ui.View):
    def __init__(self, char_key: str):
        super().__init__(timeout=120)
        self.char_key = char_key

        back_btn = discord.ui.Button(
            label=f"← Back",
            style=discord.ButtonStyle.primary
        )
        back_btn.callback = self._back_callback
        self.add_item(back_btn)

    async def _back_callback(self, interaction: discord.Interaction):
        embed = CHARACTER_PAGES[self.char_key]
        embed.set_footer(text="Nisama Wiki • Project-Nova by Jerson.EXE")
        await interaction.response.edit_message(
            embed=embed,
            view=LoreCharacterMenuView(self.char_key)
        )