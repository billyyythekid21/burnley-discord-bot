import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from requests import get
import json
from pyrandmeme import *

intents = discord.Intents().all()

DISCORD_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="$", intents = discord.Intents.all())

TOKEN="MzY2MzkxOTMzNjM2OTY4NDQ4.Gl1tdP.IknjVX6F9aE_I5XQnAOf9QgyXlk_7CaGBBhnyM"

games = {}

#musicplayer

#memegenerator

@bot.command()
async def meme(ctx):
    await ctx.send(embed=await pyrandmeme())

#say

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! This command uses slash!", ephemeral=True)

@bot.tree.command(name="say")
@app_commands.describe (msg = "What should I say?")
async def say(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {msg}`")

#multiplayer chess

@bot.command()
async def chess(ctx, opponent: discord.Member):
    if ctx.author.id == opponent.id:
        await ctx.send("You cannot play chess with yourself.")
        return

    if ctx.channel.id in games:
        await ctx.send("A game is already in progress in this channel.")
        return

    games[ctx.channel.id] = {
        "white": ctx.author,
        "black": opponent,
        "board": chess.Board()
    }

    message = f"A game of chess has started between {ctx.author.mention} and {opponent.mention}."
    message += f"\n{ctx.author.mention} is playing as White."
    await ctx.send(message)

    await display_board(ctx.channel)

@bot.command()
async def move(ctx, move_str):
    if ctx.channel.id not in games:
        await ctx.send("No game is in progress in this channel.")
        return

    game = games[ctx.channel.id]
    author = ctx.author

    if game["board"].is_game_over():
        await ctx.send("The game is already over.")
        return

    if author != game["white"] and author != game["black"]:
        await ctx.send("You are not a player in this game.")
        return

    if (author == game["white"] and game["board"].turn == chess.BLACK) or (author == game["black"] and game["board"].turn == chess.WHITE):
        await ctx.send("It's not your turn to move.")
        return

    try:
        move = game["board"].parse_san(move_str)
    except ValueError:
        await ctx.send("Invalid move format.")
        return

    if move not in game["board"].legal_moves:
        await ctx.send("Invalid move.")
        return

    game["board"].push(move)
    await display_board(ctx.channel)

    if game["board"].is_game_over():
        result = game["board"].result()
        await ctx.send(f"The game is over. Result: {result}")
        del games[ctx.channel.id]

async def display_board(channel):
    game = games[channel.id]
    svg_board = chess.svg.board(board=game["board"])
    await channel.send(file=discord.File(svg_board, "chess_board.svg"))

bot.run(TOKEN)