from discord.ext import commands
import random

class Guessing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guess", help="This is a guessing game where the user(s) can guess the number. Use !guess. Later this can have multiple difficulty")
    async def guess(self, ctx):
        number = random.randint(1, 10)
        """I was thinking about a number"""
        await ctx.send("I'm thinking of a number between 1 and 10. Guess it!")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        while True:
            try:
                guess_message = await self.bot.wait_for("message", check=check, timeout=30.0) # 30 seconds timeout
                guess = int(guess_message.content)
                if guess == number:
                    points_cog = self.bot.get_cog("Points")
                    if points_cog:
                        points_cog.add_points(ctx.author.id, 10)
                    await ctx.send(f"You got it, {ctx.author.mention}! The number was {number}. You won 10 points.")
                    break
                elif guess < number:
                    await ctx.send("Too low! Make another guess.")
                else:
                    await ctx.send("Too high! Make another guess.")
            except TimeoutError:
                points_cog = self.bot.get_cog("Points")
                if points_cog:
                    points_cog.remove_points(ctx.author.id, 5)
                await ctx.send(f"You ran out of time, {ctx.author.mention}! The number was {number}.")
                break  # Exit the loop on timeout
            except ValueError:
                await ctx.send("That's not a number! Try again.")

async def setup(bot):
    await bot.add_cog(Guessing(bot))