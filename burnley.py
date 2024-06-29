import asyncio
import discord
from discord.ext import commands, tasks
from itertools import cycle
import os

# Initialise the bot with dynamic prefix based on the guild
client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

client.remove_command("help")

# Define a cycle of statuses for the bot to display
bot_status = cycle([
    "My default prefix is $", "Hi guys!", "Ready to rumble!", 
    "Change the world!", "I am tired.", "Programmed by billyyythekid21!"
])

@tasks.loop(seconds=2)
async def change_status():
    """
    Changes the bot's status every 2 seconds to the next status in the bot_status cycle.
    """
    await client.change_presence(activity=discord.Game(next(bot_status)))

@client.event
async def on_ready():
    """
    Event handler called when the bot is ready. Starts the status change loop and prints a message.
    """
    print("Burnley is connected to Discord.")
    change_status.start()

async def load():
    """
    Loads all cog extensions from the ./cogs directory.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename} has been loaded.")

async def main():
    """
    Main function to start the bot. Loads extensions, reads the token from token.txt, and starts the bot.
    """
    async with client:
        await load()
        with open("token.txt") as file:
            token = file.read().strip()
        await client.start(token)

@client.command(name="sync")
@commands.has_permissions(administrator=True)  # Ensure only administrators can use this command
async def sync(ctx):
    # Synchronize the commands
    try:
        await client.tree.sync()
        await ctx.send("Commands have been synchronised.")
        print("Commands synchronised successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        print(f"An error occurred while synchronising commands: {e}") 

if __name__ == "__main__":
    # Run the main function to start the bot
    asyncio.run(main())
