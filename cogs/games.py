import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("games.py is ready!")
    
    @commands.hybrid_command(name="eightball", description="Ask away!", with_app_command = True, aliases=["8ball", "magiceight", "magic8"])
    async def eightball(self, ctx, *, question):
        try:
            with open("eightballresponses.txt", "r") as f:
                random_responses = f.readlines()
            response = random.choice(random_responses).strip()
            await ctx.send(response)
        except FileNotFoundError:
            await ctx.send("Responses file not found. Please make sure `eightballresponses.txt` exists.")

async def setup(client):
    await client.add_cog(Games(client))
