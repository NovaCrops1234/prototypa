import discord


# TTT

class TicTacToeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.board = [None] * 9
        self.game_over = False
        self._add_buttons()

    def _add_buttons(self):
        for i in range(9):
            self.add_item(TicTacToeButton(i))

    def build_embed(self, status: str = None) -> discord.Embed:
        symbols = {None: "⬜", "X": "❌", "O": "⭕"}
        rows = []
        for r in range(3):
            rows.append(" ".join(symbols[self.board[r * 3 + c]] for c in range(3)))
        board_str = "\n".join(rows)

        if self.game_over:
            winner = self.check_winner()
            if winner == "X":
                title = "❌ One wins!"
                desc = "Eek— one won?! Nisama needs to analyze this more ehehe. Good game!"
                color = discord.Color.green()
            elif winner == "O":
                title = "⭕ Nisama wins!"
                desc = "Ahehe! Nisama wins here! Good game though ehehe!"
                color = discord.Color.red()
            else:
                title = "🔲 Draw!"
                desc = "Mm... it's a draw here! One played well ehehe."
                color = discord.Color.greyple()
        else:
            title = "Tic Tac Toe"
            desc = status or "One's turn! Pick a cell ehehe."
            color = discord.Color.blurple()

        embed = discord.Embed(title=title, description=desc, color=color)
        embed.add_field(name="Board", value=board_str, inline=False)
        embed.set_footer(text="❌ = You  |  ⭕ = Nisama")
        return embed

    def check_winner(self) -> str | None:
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if all(self.board):
            return "draw"
        return None

    def nisama_move(self):
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = "O"
                if self.check_winner() == "O":
                    return
                self.board[i] = None
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = "X"
                if self.check_winner() == "X":
                    self.board[i] = "O"
                    return
                self.board[i] = None
        if self.board[4] is None:
            self.board[4] = "O"
            return
        for i in [0, 2, 6, 8]:
            if self.board[i] is None:
                self.board[i] = "O"
                return
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = "O"
                return


class TicTacToeButton(discord.ui.Button):
    def __init__(self, index: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="·", row=index // 3)
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        if view.game_over or view.board[self.index] is not None:
            await interaction.response.defer()
            return

        view.board[self.index] = "X"
        self.style = discord.ButtonStyle.danger
        self.label = "❌"
        self.disabled = True

        winner = view.check_winner()
        if winner:
            view.game_over = True
            for item in view.children:
                item.disabled = True
            embed = view.build_embed()
            await interaction.response.edit_message(embed=embed, view=view)
            return

        view.nisama_move()
        for item in view.children:
            if isinstance(item, TicTacToeButton):
                if view.board[item.index] == "O":
                    item.style = discord.ButtonStyle.primary
                    item.label = "⭕"
                    item.disabled = True

        winner = view.check_winner()
        if winner:
            view.game_over = True
            for item in view.children:
                item.disabled = True

        embed = view.build_embed()
        await interaction.response.edit_message(embed=embed, view=view)


# UTT

BOARD_NAMES = [
    "Top-Left", "Top-Center", "Top-Right",
    "Middle-Left", "Center", "Middle-Right",
    "Bottom-Left", "Bottom-Center", "Bottom-Right"
]

class UltimateTTTGame:
    def __init__(self):
        self.boards = [[None] * 9 for _ in range(9)]
        self.board_winners = [None] * 9
        self.active_board = None
        self.game_over = False
        self.global_winner = None
        self.move_log = []
        self.move_number = 0

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

    def get_playable_boards(self) -> list:
        if self.active_board is not None:
            if self.board_winners[self.active_board] is None and any(c is None for c in self.boards[self.active_board]):
                return [self.active_board]
        return [
            i for i in range(9)
            if self.board_winners[i] is None and any(c is None for c in self.boards[i])
        ]

    def nisama_move(self):
        playable = self.get_playable_boards()
        for bi in playable:
            for ci in range(9):
                if self.boards[bi][ci] is None:
                    self.boards[bi][ci] = "O"
                    if self.check_board_winner(self.boards[bi]) == "O":
                        self.board_winners[bi] = "O"
                        return bi, ci
                    self.boards[bi][ci] = None
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
        for bi in playable:
            if self.boards[bi][4] is None:
                self.boards[bi][4] = "O"
                w = self.check_board_winner(self.boards[bi])
                if w:
                    self.board_winners[bi] = w
                return bi, 4
        for bi in playable:
            for ci in range(9):
                if self.boards[bi][ci] is None:
                    self.boards[bi][ci] = "O"
                    w = self.check_board_winner(self.boards[bi])
                    if w:
                        self.board_winners[bi] = w
                    return bi, ci
        return None, None

    def render_global_board(self) -> str:
        symbols = {None: "⬜", "X": "❌", "O": "⭕", "draw": "🔲"}
        rows = []
        for r in range(3):
            row = []
            for c in range(3):
                bi = r * 3 + c
                if self.board_winners[bi]:
                    row.append(symbols[self.board_winners[bi]])
                elif bi == self.active_board:
                    row.append("🟦")
                else:
                    row.append("⬜")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def render_local_board(self, board_index: int) -> str:
        cells = self.boards[board_index]
        rows = []
        for r in range(3):
            row = []
            for c in range(3):
                ci = r * 3 + c
                v = cells[ci]
                row.append("❌" if v == "X" else "⭕" if v == "O" else "·")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def build_embed(self, status: str = None, log_page: int = 0) -> discord.Embed:
        playable = self.get_playable_boards()
        active = self.active_board if self.active_board is not None else (playable[0] if playable else 0)

        if self.game_over:
            if self.global_winner == "X":
                title = "❌ One wins the Super Board!"
                desc = "Eek— one won the whole thing?! Nisama needs to analyze this more ehehe. Amazing game!"
                color = discord.Color.green()
            elif self.global_winner == "O":
                title = "⭕ Nisama wins the Super Board!"
                desc = "Ahehe! Nisama wins here! Really good game though ehehe!"
                color = discord.Color.red()
            else:
                title = "🔲 Full Draw!"
                desc = "Mm... it's a full draw here! One played really well ehehe."
                color = discord.Color.greyple()
        else:
            title = f"Ultimate Tic Tac Toe — {BOARD_NAMES[active]}"
            desc = status or "One's turn! Pick a cell in the active board ehehe."
            color = discord.Color.blurple()

        embed = discord.Embed(title=title, description=desc, color=color)
        embed.add_field(
            name="🌐 Global Board",
            value=self.render_global_board(),
            inline=True
        )
        embed.add_field(
            name=f"🎯 Active — {BOARD_NAMES[active] if not self.game_over else 'Done'}",
            value=self.render_local_board(active) if not self.game_over else "Game over!",
            inline=True
        )

        # Paginated move log — 8 moves per page
        if self.move_log:
            page_size = 8
            total_pages = max(1, (len(self.move_log) + page_size - 1) // page_size)
            log_page = max(0, min(log_page, total_pages - 1))
            start = log_page * page_size
            end = start + page_size
            log_text = "\n".join(self.move_log[start:end])
            embed.add_field(
                name=f"📋 Move Log (Page {log_page + 1}/{total_pages})",
                value=log_text,
                inline=False
            )

        embed.set_footer(text="❌ = You  |  ⭕ = Nisama  |  🟦 = Active Board  |  🔲 = Draw")
        return embed

    def build_message(self, status: str = None, log_page: int = 0) -> tuple:
        playable = self.get_playable_boards()
        active = self.active_board if self.active_board is not None and not self.game_over else (playable[0] if playable else 0)
        embed = self.build_embed(status=status, log_page=log_page)
        view = UltimateTTTView(self, active if not self.game_over else None, log_page=log_page)
        return embed, view


class UltimateTTTView(discord.ui.View):
    def __init__(self, game: UltimateTTTGame, board_index: int | None, log_page: int = 0):
        super().__init__(timeout=300)
        self.game = game
        self.board_index = board_index
        self.log_page = log_page

        # Game buttons — rows 0,1,2
        if board_index is not None:
            cells = game.boards[board_index]
            symbols = {"X": "❌", "O": "⭕"}
            for ci in range(9):
                taken = cells[ci] is not None
                btn = discord.ui.Button(
                    style=discord.ButtonStyle.danger if cells[ci] == "X"
                          else discord.ButtonStyle.primary if cells[ci] == "O"
                          else discord.ButtonStyle.secondary,
                    label=symbols.get(cells[ci], "·"),
                    row=ci // 3,
                    disabled=taken or game.game_over
                )
                btn.callback = self._make_callback(ci)
                self.add_item(btn)

        # Pagination buttons — row 3
        total_pages = max(1, (len(game.move_log) + 7) // 8)
        prev_btn = discord.ui.Button(
            label="◀",
            style=discord.ButtonStyle.secondary,
            disabled=log_page <= 0,
            row=3
        )
        next_btn = discord.ui.Button(
            label="▶",
            style=discord.ButtonStyle.secondary,
            disabled=log_page >= total_pages - 1,
            row=3
        )
        prev_btn.callback = self._make_page_callback(log_page - 1)
        next_btn.callback = self._make_page_callback(log_page + 1)
        self.add_item(prev_btn)
        self.add_item(next_btn)

    def _make_page_callback(self, new_page: int):
        async def callback(interaction: discord.Interaction):
            embed, view = self.game.build_message(log_page=new_page)
            await interaction.response.edit_message(embed=embed, view=view)
        return callback

    def _make_callback(self, cell_index: int):
        async def callback(interaction: discord.Interaction):
            game = self.game
            bi = self.board_index

            if game.game_over or game.boards[bi][cell_index] is not None:
                await interaction.response.defer()
                return

            # Player move
            game.move_number += 1
            game.boards[bi][cell_index] = "X"
            w = game.check_board_winner(game.boards[bi])
            if w:
                game.board_winners[bi] = w
                game.move_log.append(f"#{game.move_number} ❌ won {BOARD_NAMES[bi]}!")
            else:
                game.move_log.append(f"#{game.move_number} ❌ → {BOARD_NAMES[bi]}, cell {cell_index + 1}")

            next_board = cell_index
            if game.board_winners[next_board] is not None or all(c is not None for c in game.boards[next_board]):
                game.active_board = None
            else:
                game.active_board = next_board

            gw = game.check_global_winner()
            if gw:
                game.game_over = True
                game.global_winner = gw
                embed, view = game.build_message()
                await interaction.response.edit_message(embed=embed, view=view)
                return

            # Nisama move
            nbi, nci = game.nisama_move()
            if nbi is not None:
                game.move_number += 1
                if game.board_winners[nbi] is not None:
                    game.move_log.append(f"#{game.move_number} ⭕ won {BOARD_NAMES[nbi]}!")
                else:
                    game.move_log.append(f"#{game.move_number} ⭕ → {BOARD_NAMES[nbi]}, cell {nci + 1}")

                next_board2 = nci
                if game.board_winners[next_board2] is not None or all(c is not None for c in game.boards[next_board2]):
                    game.active_board = None
                else:
                    game.active_board = next_board2

                gw = game.check_global_winner()
                if gw:
                    game.game_over = True
                    game.global_winner = gw
                    embed, view = game.build_message()
                    await interaction.response.edit_message(embed=embed, view=view)
                    return

            playable = game.get_playable_boards()
            if not playable:
                game.game_over = True
                game.global_winner = "draw"
                embed, view = game.build_message()
                await interaction.response.edit_message(embed=embed, view=view)
                return

            next_active = game.active_board if game.active_board is not None else playable[0]
            status = f"Nisama moved! Now playing in **{BOARD_NAMES[next_active]}** ehehe."

            # Stay on last page to show latest moves
            last_page = max(0, (len(game.move_log) - 1) // 8)
            embed, view = game.build_message(status=status, log_page=last_page)
            await interaction.response.edit_message(embed=embed, view=view)

        return callback