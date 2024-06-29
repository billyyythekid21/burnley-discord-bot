import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw
import requests

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id="v-XPRBwxYlmOxCLGvhasGw", client_secret="oPqkwz2Bfn8Sf__aHHnaZzraDPNLQQ",user_agent="script://Burnley:v1.0 (by u/DatHopeGames)")


    @commands.Cog.listener()
    async def on_ready(self):
        print("fun.py is ready!")

    @commands.hybrid_command(name="cat", description="Fetches a cute cat picture.", with_app_command = True, aliases=["cats", "kitty"])
    async def cat(self, ctx: commands.Context):

        subreddit = await self.reddit.subreddit("cats")
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))
        
        if posts_list:

            random_post = choice(posts_list)

            meme_embed = discord.Embed(title="Cat!", colour=discord.Colour.random())
            meme_embed.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Author: r/{random_post[1]}", icon_url=None)
            await ctx.send(embed=meme_embed)

        else:
            await ctx.send("Unable to fetch cats from reddit, please try again later.")

    @commands.hybrid_command(name="dog", description="Fetches a cute dog picture.", with_app_command = True, aliases=["dogs"])
    async def dog(self, ctx: commands.Context):

        subreddit = await self.reddit.subreddit("dog")
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))
        
        if posts_list:

            random_post = choice(posts_list)

            meme_embed = discord.Embed(title="Dog!", colour=discord.Colour.random())
            meme_embed.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Author: r/{random_post[1]}", icon_url=None)
            await ctx.send(embed=meme_embed)

        else:
            await ctx.send("Unable to fetch dogs from reddit, please try again later.")

    @commands.hybrid_command(name="meme", description="Fetches a meme from Reddit.", with_app_command = True, aliases=["memes", "dankmeme"])
    async def meme(self, ctx: commands.Context):

        subreddit = await self.reddit.subreddit("memes")
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if not post.over_18 and post.author is not None and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))
        
        if posts_list:

            random_post = choice(posts_list)

            meme_embed = discord.Embed(title="Meme", colour=discord.Colour.random())
            meme_embed.set_author(name=f"Meme requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Author: r/{random_post[1]}", icon_url=None)
            await ctx.send(embed=meme_embed)

        else:
            await ctx.send("Unable to fetch any memes from reddit, please try again later.")

    @commands.hybrid_command(name="oilup", description="Don't even ask about this.", with_app_command = True, aliases=["oil", "oilup!"])
    async def oilup(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author
        elif user is not None:
            user = user

        await ctx.send("https://tenor.com/view/no-gif-6533142189269812111")
        await user.send("https://tenor.com/view/sam-tailor-gif-443562058520030623")
        await user.send("https://tenor.com/view/noel-noel-deyzel-oil-noel-oil-oil-up-gif-15231228810340005316")

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())

    @commands.hybrid_command(name="quote", description="Sends you a random inspirational quote.", aliases=["quotes", "inspire"])
    async def quote(self, ctx, user: discord.Member = None):
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            message = response.json()
            quote = f"{message['content']} - {message['author']}"
            if user is None:
                user = ctx.author
                await ctx.send(quote)
            else:
                await ctx.send(f"{user.mention}, check your DMs for an inspirational quote!")
                await user.send(quote)
        else:
            await ctx.send("Failed to retrieve a quote. Please try again later.")

async def setup(client):
   await client.add_cog(Fun(client))
