import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw
import aiohttp
import csv

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("../tokens/reddittokens.txt") as file:
            file = csv.DictReader(file, delimiter=',')
            for token in file:
                client_id = token["client_id"].strip()
                client_secret = token["client_secret"].strip()
                user_agent = token["user_agent"].strip()
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


    @commands.Cog.listener()
    async def on_ready(self):
        print("fun.py is ready!")

    async def _fetch_reddit_image(self, ctx: commands.Context, subreddit_name: str, title: str):
        subreddit = await self.reddit.subreddit(subreddit_name)
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if not post.over_18 and any(post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name if post.author else "N/A"
                posts_list.append((post.url, author_name))

        if posts_list:
            random_post = choice(posts_list)
            embed = discord.Embed(title=title, colour=discord.Colour.random())
            embed.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            embed.set_image(url=random_post[0])
            embed.set_footer(text=f"u/{random_post[1]}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Unable to fetch from r/{subreddit_name}, please try again later.")

    @commands.hybrid_command(name="cat", description="Fetches a cute cat picture.", with_app_command=True,
                             aliases=["cats", "kitty"])
    async def cat(self, ctx: commands.Context):
        await self._fetch_reddit_image(ctx, "cats", "Cat!")

    @commands.hybrid_command(name="dog", description="Fetches a cute dog picture.", with_app_command=True,
                             aliases=["dogs"])
    async def dog(self, ctx: commands.Context):
        await self._fetch_reddit_image(ctx, "dog", "Dog!")

    @commands.hybrid_command(name="meme", description="Fetches a meme from Reddit.", with_app_command=True,
                             aliases=["memes", "dankmeme"])
    async def meme(self, ctx: commands.Context):
        await self._fetch_reddit_image(ctx, "memes", "Meme")

    @commands.hybrid_command(name="news", description="Fetches the latest news on a topic.", with_app_command=True,
                                 aliases=["headlines"])
    async def news(self, ctx: commands.Context, *, topic: str = "technology"):
        async with aiohttp.ClientSession() as session:
            with open("../tokens/newsapitoken.txt") as f:
                api_key = f.read().strip()

            params = {
                "q": topic,
                "pageSize": 5,
                "sortBy": "publishedAt",
                "apiKey": api_key,
                "language": "en"
            }

            async with session.get("https://newsapi.org/v2/everything", params=params) as response:
                if response.status != 200:
                    return await ctx.send("Failed to fetch news. Please try again later.")

                data = await response.json()
                articles = data.get("articles", [])

                if not articles:
                    return await ctx.send(f"No news found for **{topic}**.")

                embed = discord.Embed(title=f"Top news: {topic}", colour=discord.Colour.blue())
                embed.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)

                for article in articles:
                    title = article.get("title", "No title")
                    url = article.get("url", "")
                    source = article.get("source", {}).get("name", "Unknown")
                    embed.add_field(name=f"{source}", value=f"[{title}]({url})", inline=False)

                await ctx.send(embed=embed)

    @commands.hybrid_command(name="oilup", description="Don't even ask about this.", with_app_command = True,
                             aliases=["oil", "oilup!"])
    async def oilup(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.author
        elif user is not None:
            user = user

        await ctx.send("https://tenor.com/view/no-gif-6533142189269812111")
        await user.send("https://tenor.com/view/sam-tailor-gif-443562058520030623")
        await user.send("https://tenor.com/view/noel-noel-deyzel-oil-noel-oil-oil-up-gif-15231228810340005316")

    def cog_unload(self):
        self.client.loop.create_task(self.reddit.close())

    @commands.hybrid_command(name="quote", description="Sends you a random inspirational quote.",
                             aliases=["quotes", "inspire"])
    async def quote(self, ctx, user: discord.Member = None):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.quotable.io/random") as response:
                if response.status == 200:
                    message = await response.json()
                    quote = f"{message['content']} - {message['author']}"
                    if user is None:
                        await ctx.send(quote)
                    else:
                        await ctx.send(f"{user.mention}, check your DMs for an inspirational quote!")
                        await user.send(quote)
                else:
                    await ctx.send("Failed to retrieve a quote. Please try again later.")

async def setup(client):
   await client.add_cog(Fun(client))
