import discord
from discord.ext import commands
import wikipediaapi
import random

try:
    wiki = wikipediaapi.Wikipedia('en', user_agent="blank")
    print("Wikipedia initialisation successful")
except TypeError as e:
    print(f"TypeError: {e}")

class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("wikipedia.py is ready!")
    
    @commands.hybrid_command(name="wikisummary", description="Returns a Wikipedia summary")
    async def summary(self, ctx, *, query):
        page = wiki.page(query)
        if page.exists():
            await ctx.send(page.summary[0:2000])  # Discord message limit is 2000 characters
        else:
            await ctx.send("Sorry, that page does not exist on Wikipedia.")

    @commands.hybrid_command(name="wikisearch", description="Search Wikipedia")
    async def search(self, ctx, *, query):
        search_results = wiki.search(query)
        if search_results:
            result_message = "\n".join(f"- {result}" for result in search_results[:5])  # Show top 5 results
            await ctx.send(f"Top search results:\n{result_message}")
        else:
            await ctx.send("Sorry, no results found on Wikipedia.")

    @commands.hybrid_command(name="wikiurl", description="Obtain a URL to a page on Wikipedia")
    async def url(self, ctx, *, query):
        page = wiki.page(query)
        if page.exists():
            await ctx.send(page.fullurl)
        else:
            await ctx.send("Sorry, that page does not exist on Wikipedia.")
        
    @commands.hybrid_command(name="wiki_random", description= "Finds a random Wikipedia article")
    async def random_article(self, ctx):
        random_page_title = wiki.random(pages=1)
        page = wiki.page(random_page_title)
        if page.exists():
            await ctx.send(f"**{page.title}**\n\n{page.summary[0:2000]}\n\n{page.fullurl}")
        else:
            await ctx.send("Sorry, something went wrong with Wikipedia. Please try again.")

async def setup(client):
    await client.add_cog(Wiki(client))
