import discord
from discord.ext import commands
import sympy as sp

class Calculator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("calculator.py is ready!")

    @commands.hybrid_command(name="calculate", description="Calculates a given equation. Maths.", with_app_command = True, aliases=["calc", "solve", "calculator"])
    async def calculate(self, ctx, *, expression: str):
        try:
            # Parse and evaluate the expression using SymPy
            expr = sp.sympify(expression)
            answer = sp.simplify(expr)
            await ctx.send(f"{expression} = {answer}")
        except (sp.SympifyError, ValueError):
            await ctx.send("ERROR: Math expression is invalid. Please try again.")
        
async def setup(client):
    await client.add_cog(Calculator(client))
