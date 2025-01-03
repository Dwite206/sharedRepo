from discord.ext import commands

introduction =  """ Hello, my name is Python Musk. I'm here to help you! I'm a Python bot.
You can use the following commands with the prefix '!':
!hello
!help
!guess
!poll
!info
"""
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello", help="This is a hello command use !hello")
    async def hello(self, ctx):
        """Says hello to the user."""
        await ctx.send(f"Hello, {ctx.author.mention}! Use !help for more")

    @commands.command(name="info", help="This is an introduction command")
    async def info(self, ctx):
        await ctx.send(introduction)


async def setup(bot):
    await bot.add_cog(Greetings(bot))