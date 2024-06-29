import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("help.py is ready!")

    @commands.hybrid_command(name="help", description="Lists all of Burnley's commands.", with_app_command = True)
    async def help(self, ctx):
        help_embed = discord.Embed(
            title="Burnley Help",
            description="Command list for the Burnley bot",
            colour=discord.Colour.blue()
        )

        help_embed.set_author(name="Burnley")
        help_embed.add_field(name="calculate", value="Calculates a given equation. Maths.", inline=False)
        help_embed.add_field(name="cat", value="Fetches a cute cat picture.", inline=False)
        help_embed.add_field(name="eightball", value="Ask away!", inline=False)
        help_embed.add_field(name="level", value="Check your user level.", inline=False)
        help_embed.add_field(name="meme", value="Fetches a meme from Reddit.", inline=False)
        help_embed.add_field(name="oilup", value="Don't even ask about this.", inline=False)
        help_embed.add_field(name="query", value="Ask Google AI any prompt and you shall be blessed with an answer!", inline=False)
        help_embed.add_field(name="quote", value="Sends you a random inspirational quote.", inline=False)
        help_embed.add_field(name="ping", value="Returns the bot's latency.", inline=False)
        help_embed.add_field(name="play", value="Plays the specified song in the current voice channel.", inline=False)
        help_embed.add_field(name="pause", value="Pauses the current song.", inline=False)
        help_embed.add_field(name="resume", value="Resumes the current song.", inline=False)
        help_embed.add_field(name="skip", value="Skips the current song.", inline=False)
        help_embed.add_field(name="setprefix", value="Sets a custom prefix for Burnley for this server only.", inline=False)
        help_embed.add_field(name="userinfo", value="Displays the information of the requested user.", inline=False)
        help_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
    
        await ctx.send(embed=help_embed)

async def setup(client):
    await client.add_cog(Help(client))
