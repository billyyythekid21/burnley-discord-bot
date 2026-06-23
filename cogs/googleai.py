from discord.ext import commands
import google.genai as genai
import asyncio

with open("../tokens/googleaikey.txt") as file:
    token = file.read().strip()

ai_client = genai.Client(api_key=token)

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("googleai.py is ready!")
    
    @commands.hybrid_command(name="query", description="Ask Google AI any prompt and you shall "
                                                       "be blessed with an answer!")
    async def query(self, ctx, *, question):
        try:
            response = await asyncio.to_thread(
                ai_client.models.generate_content,
                model="gemini-2.0-flash",
                contents=question,
            )
            if response and response.text:
                response_text = response.text
                for chunk in [response_text[i:i + 1900] for i in range(0, len(response_text), 1900)]:
                    await ctx.send(f"**Query:**\n{question}\n**Response:**\n{chunk}")
        except Exception as e:
            await ctx.send(f"ERROR: An error has occurred while processing your request: {e}")

    @commands.hybrid_command(name="summarise" description="Summarise the last few messages")
    async def summarise(self, ctx, *, query):
        try:
            response = await asyncio.to_thread(
                ai_client.models.generate_content,
                model="gemini-2.0-flash",
                contents=question,
            )
            if response and response.text:
                response_text = response.text
                for chunk in [response_text[i:i + 1900] for i in range(0, len(response_text), 1900)]:
                    await ctx.send(f"**Query:**\n{question}\n**Response:**\n{chunk}")
        except Exception as e:
            await ctx.send(f"ERROR: An error has occurred while processing your request: {e}")


async def setup(client):
    await client.add_cog(AI(client))