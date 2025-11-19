import discord
from discord.ext import commands
import cogs.chess as chess
import chess.svg
from io import BytesIO
import cairosvg

class Chess(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.games = {}

    class ChessGame:
        def __init__(self, player1, player2):
            self.board = chess.Board()
            self.player1 = player1
            self.player2 = player2
            self.current_turn = player1

        def move(self, move):
            try:
                chess_move = chess.Move.from_uci(move)
                if chess_move in self.board.legal_moves:
                    self.board.push(chess_move)
                    self.current_turn = self.player2 if self.current_turn == self.player1 else self.player1
                    return True
                else:
                    return False
            except:
                return False

        def is_game_over(self):
            return self.board.is_game_over()

        def get_winner(self):
            if self.board.is_checkmate():
                return self.player2 if self.current_turn == self.player1 else self.player1
            else:
                return None

        def get_board_image(self):
            svg_data = chess.svg.board(board=self.board).encode('utf-8')
            png_data = cairosvg.svg2png(bytestring=svg_data)
            return BytesIO(png_data)

    @commands.Cog.listener()
    async def on_ready(self):
        print("chess.py is ready!")

    @commands.hybrid_command(name="chess_startgame", description="Start a game of chess with an opponent.")
    async def start_game(self, ctx, opponent: discord.Member):
        if ctx.author.id in self.games or opponent.id in self.games:
            await ctx.send("One of the players is already in a game.")
            return

        self.games[ctx.author.id] = self.ChessGame(ctx.author, opponent)
        self.games[opponent.id] = self.games[ctx.author.id]
        
        await ctx.send(f"Game started between {ctx.author.mention} and {opponent.mention}. {ctx.author.mention} goes first.")
        await self.send_board(ctx)

    @commands.hybrid_command(name="chess_move", description="Make a move in your current chess game.")
    async def make_move(self, ctx, move: str):
        if ctx.author.id not in self.games:
            await ctx.send("You are not in a game.")
            return

        game = self.games[ctx.author.id]
        if ctx.author != game.current_turn:
            await ctx.send("It's not your turn.")
            return

        if game.move(move):
            await ctx.send(f"{ctx.author.mention} made a move: {move}")
            await self.send_board(ctx)

            if game.is_game_over():
                winner = game.get_winner()
                if winner:
                    await ctx.send(f"Game over! {winner.mention} wins!")
                else:
                    await ctx.send("Game over! It's a draw!")
                del self.games[game.player1.id]
                del self.games[game.player2.id]
        else:
            await ctx.send("Invalid move.")

    async def send_board(self, ctx):
        game = self.games[ctx.author.id]
        board_image = game.get_board_image()
        file = discord.File(fp=board_image, filename="board.png")
        await ctx.send(file=file)

async def setup(client):
    await client.add_cog(Chess(client))
