import discord
from discord.ext import commands
import google.generativeai as genai

with open("../tokens/googleaikey.txt") as file:
    token = file.read().strip()

GEMINI_API_KEY = str(token)

genai.configure(api_key=GEMINI_API_KEY)

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("googleai.py is ready!")
    
    @commands.hybrid_command(name="query", description="Ask Google AI any prompt and you shall be blessed with an answer!")
    async def query(self, ctx, *, question):
        if not question:
            await ctx.send("ERROR: Please provide a query.")
            return
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(question)
            if response and hasattr(response, 'text'):
                response_text = response.text
                for chunk in [response_text[i:i + 1900] for i in range(0, len(response_text), 1900)]:
                    await ctx.send(f"**Query:**\n{question}\n**Response:**\n{chunk}")
        except Exception as e:
            await ctx.send(f"ERROR: An error has occured while processing your request: {e}")

async def setup(client):
    await client.add_cog(AI(client))