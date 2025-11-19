import discord
from discord.ext import commands

class CommonCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("commoncog.py is ready!")

    @commands.command()
    async def embed(self, ctx):
        # Creating an embed message
        embed_message = discord.Embed(
            title="Embed test",
            description="Description test",
            color=discord.Colour.yellow()
        )

        # Setting author and thumbnail
        embed_message.set_author(
            name=f"Requested by {ctx.author.mention}",
            icon_url=ctx.author.avatar.url
        )
        embed_message.set_thumbnail(url=ctx.guild.icon.url)

        # Setting image and adding field
        embed_message.set_image(url=ctx.guild.icon.url)
        embed_message.add_field(name="Field name", value="Field Value", inline=False)

        # Setting footer and sending the embed
        embed_message.set_footer(text="This is the footer")
        await ctx.send(embed=embed_message)

    @commands.hybrid_command(name="ping", description="Returns the bot's latency.", with_app_command = True)
    async def ping(self, ctx):
        """
        Returns the bot's latency.
        """
        # Calculating bot latency
        bot_latency = round(self.client.latency * 1000)  # Calculate latency in milliseconds
        await ctx.send(f"Ping: {bot_latency} ms")  # Send the latency as a message

    @commands.hybrid_command(name="userinfo", description="Displays the information of the requested user.", with_app_command = True, aliases=["info", "user"])
    async def userinfo(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        info_embed = discord.Embed(title=f"{member.name}'s User Information", description="Information about this user", colour=member.color)
        info_embed.set_thumbnail(url=member.avatar)
        info_embed.add_field(name="Name:", value=member.name, inline=False)
        info_embed.add_field(name="Server Nickname:", value=member.display_name, inline=False)
        info_embed.add_field(name="ID:", value=member.id, inline=False)
        info_embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        info_embed.add_field(name="Status:", value=member.status, inline=False)
        info_embed.add_field(name="Is Bot?", value=member.bot, inline=False)
        info_embed.add_field(name="Account Creation Date:", value=member.created_at.__format__("%A %d %B %Y at %H:%M:%S"), inline=False)
        info_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=info_embed)

async def setup(client):
    await client.add_cog(CommonCog(client))
