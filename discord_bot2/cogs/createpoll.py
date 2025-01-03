import discord
import asyncio
from discord.ext import commands
from datetime import timedelta  # Import timedelta

class CreatePoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = {} 

    @commands.command(name="poll", help="Creates a poll with reactions for voting. Use !poll 'question' '*options' [duration_seconds].")
    async def poll(self, ctx, question: str, *options, duration: int = 300):
         # Separate the actual options from the duration argument
        if len(options) > 1 and options[-1].isdigit():
            try:
                duration = int(options[-1])
                options = options[:-1]  # Remove the last element (duration) from options
            except ValueError:
                pass  # Handle cases where the last element is not a valid integer
            
        if len(options) > 9:
            await ctx.send("You can have a maximum of 9 options.")
            return

        if duration <= 0:
            await ctx.send("The duration must be a positive number of seconds.")
            return

        # Create poll embed
        embed = discord.Embed(title=question, description="React with the corresponding number to vote!", color=discord.Color.blue())
        for i, option in enumerate(options):
            embed.add_field(name=f"{i+1}. {option}", value="0 votes", inline=False)

        embed.set_footer(text=f"Poll ends in {duration} seconds. Total votes: 0")
        poll_message = await ctx.send(embed=embed)
        self.polls[poll_message.id] = {
            "options": options,
            "votes": {str(i+1): [] for i in range(len(options))}, # {option_number: [user_ids]}
            "message": poll_message,
            "end_time": discord.utils.utcnow() + timedelta(seconds=duration), # Corrected line
            "total_votes": 0
        }

        # Add number reactions
        for i in range(len(options)):
            await poll_message.add_reaction(f"{i+1}\u20e3") # Number emoji

        # Start timer
        asyncio.create_task(self.poll_timer(poll_message.id))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or reaction.message.id not in self.polls:
            return

        poll_data = self.polls[reaction.message.id]
        emoji_number = str(reaction.emoji)[0] # Get the number from the emoji

        if emoji_number in poll_data["votes"]:
            if user.id not in poll_data["votes"][emoji_number]:
                # Remove other votes from the same user
                for option in poll_data["votes"]:
                    if user.id in poll_data["votes"][option]:
                        poll_data["votes"][option].remove(user.id)

                # Add new vote
                poll_data["votes"][emoji_number].append(user.id)

                # Update poll message
                await self.update_poll_message(reaction.message.id)

    async def update_poll_message(self, message_id):
        poll_data = self.polls[message_id]
        message = poll_data["message"]
        embed = message.embeds[0]

        for i, option in enumerate(poll_data["options"]):
            vote_count = len(poll_data["votes"][str(i + 1)])
            embed.set_field_at(i, name=f"{i + 1}. {option}", value=f"{vote_count} votes", inline=False)

        remaining_time = int((poll_data["end_time"] - discord.utils.utcnow()).total_seconds())
        if remaining_time > 0:
             embed.set_footer(text=f"Poll ends in {remaining_time} seconds. Total votes: {poll_data['total_votes']}")
        else:
            embed.set_footer(text=f"Poll ended. Total votes: {poll_data['total_votes']}")

        await message.edit(embed=embed)

    async def poll_timer(self, message_id):
        """Closes the poll after the specified duration."""
        poll_data = self.polls[message_id]
        end_time = poll_data["end_time"]

        while True:
            remaining_time = (end_time - discord.utils.utcnow()).total_seconds()
            if remaining_time <= 0:
                await self.close_poll(message_id)
                break

            await self.update_poll_message(message_id)
            await asyncio.sleep(min(remaining_time, 5))  # Update every 5 seconds or less

    async def close_poll(self, message_id):
        """Closes the poll and removes reactions."""
        if message_id in self.polls:
            poll_data = self.polls[message_id]
            message = poll_data["message"]
            await self.update_poll_message(message_id)
            
            # Remove all reactions
            await message.clear_reactions()

            del self.polls[message_id]

async def setup(bot):
    await bot.add_cog(CreatePoll(bot))