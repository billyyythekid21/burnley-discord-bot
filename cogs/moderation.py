import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation.py is ready!")

    @commands.hybrid_command(name="ban", description="Bans the specified user from the server.", with_app_command = True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modreason):
        # Ban the member
        await ctx.guild.ban(member)
        
        # Confirmation message
        conf_embed = discord.Embed(title="Ban successful!", color=discord.Colour.green)
        conf_embed.add_field(name="Banned", value=f"{member.mention} has been banned from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)

    @commands.hybrid_command(name="clear", description="Clears a specified amount of messages fom the current channel.", with_app_command = True, aliases=["clean", "wipe"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        # Clear messages
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} message(s) have been cleared by Burnley!")

    @commands.hybrid_command(name="kick", description="Kicks the specified user from the server.", with_app_command = True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, modreason):
        # Kick the member
        await ctx.guild.kick(member)
        
        # Confirmation message
        conf_embed = discord.Embed(title="Kick successful!", color=discord.Colour.green)
        conf_embed.add_field(name="Kicked", value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command(name="unban", description="Unbans the specified user from the server.", with_app_command = True)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userId):
        # Unban the user
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)

        # Confirmation message
        conf_embed = discord.Embed(title="Unban successful!", color=discord.Colour.green)
        conf_embed.add_field(name="Unbanned", value=f"<@{userId}> has been unbanned from the server by {ctx.author.mention}.", inline=False)
        
        await ctx.send(embed=conf_embed)

async def setup(client):
    await client.add_cog(Moderation(client))
