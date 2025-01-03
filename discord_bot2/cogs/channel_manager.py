import discord
from discord.ext import commands
import logging

class ChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Get the root logger
        self.logger = logging.getLogger("discord.channelmanager") # Create a child logger under 'discord'
        self.logger.setLevel(logging.INFO) # Set the logging level for this specific cog

        # Create a separate file handler for the LLM cog if you want separate log files
        channelmanager_handler = logging.FileHandler(filename="channelmanager.log", encoding="utf-8", mode="w")
        channelmanager_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        channelmanager_handler.setFormatter(channelmanager_formatter)
        self.logger.addHandler(channelmanager_handler)

    @commands.command(name="createchannel", aliases=["cc"], help="Creates a new text channel. eg. !cc 'textchannelName' 'textchannelgroup'")
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name: str, *, category_name: str = None):
        """Creates a new text channel."""
        try:
            self.logger.info(f"A new channel creation has been called with a name: {channel_name}, by: {ctx.author}")
            guild = ctx.guild
            category = None
            if category_name:
                category = discord.utils.get(guild.categories, name=category_name)
                if not category:
                    error_message = f"Category '{category_name}' not found."
                    self.logger.info(error_message)
                    await ctx.send(error_message)
                    return
            new_channel = await guild.create_text_channel(channel_name)
            self.logger.info(f"A new channel has been succesfully created with a name: {new_channel}, by: {ctx.author}")
            await ctx.send(f"Text channel '{new_channel.name}' created successfully!")
        except discord.Forbidden:
            forbidden_message = "I don't have permission to create channels."
            self.logger.info(forbidden_message)
            await ctx.send(forbidden_message)
        except discord.HTTPException as e:
            error_message = f"An error occurred: {e}"
            self.logger.error(error_message)
            await ctx.send(error_message)

    @commands.command(name="createvoicechannel", aliases=["cvc"], help="Creates a new voice channel. eg. !cvc 'voicechannelName' 'voicechannelGroup'")
    @commands.has_permissions(manage_channels=True)
    async def create_voice_channel(self, ctx, channel_name: str, *, category_name: str = None):
        """Creates a new voice channel, optionally in a specified category."""
        try:
            self.logger.info(f"A new voice channel creation has been called with a name: {channel_name}, by: {ctx.author}")
            guild = ctx.guild
            category = None
            if category_name:
                category = discord.utils.get(guild.categories, name=category_name)
                if not category:
                    error_message = f"Category '{category_name}' not found."
                    self.logger.info(error_message)
                    await ctx.send(error_message)
                    return

            new_channel = await guild.create_voice_channel(channel_name, category=category)
            self.logger.info(f"A new voice channel has been successfully created with a name: {new_channel.name}, by: {ctx.author}")
            await ctx.send(f"Voice channel '{new_channel.name}' created successfully!")
        except discord.Forbidden:
            forbidden_message = "I don't have permission to create channels."
            self.logger.info(forbidden_message)
            await ctx.send(forbidden_message)
        except discord.HTTPException as e:
            error_message = f"An error occurred: {e}"
            self.logger.error(error_message)
            await ctx.send(error_message)

    @commands.command(name="deletechannel", aliases=["dc"], help="Deletes a channel. eg. !dc 'textchannelName' or 'voicehannelName'")
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel_name: str):
        """Deletes a specified channel."""
        try:
            self.logger.info(f"An existent channels deletion has been called, channel name: {channel_name}, by: {ctx.author}")
            guild = ctx.guild
            channel = discord.utils.get(guild.channels, name=channel_name)
            if channel:
                await channel.delete()
                self.logger.info(f"Channel with the name has been successfully deleted: {channel_name}, by: {ctx.author}")
                await ctx.send(f"Channel '{channel_name}' deleted successfully!")
            else:
                self.logger.info(f"Channel with the following name has not been found: {channel_name}")
                await ctx.send(f"Channel '{channel_name}' not found.")
        except discord.Forbidden:
            forbidden_message = "I don't have permission to delete channels."
            self.logger.info(forbidden_message)
            await ctx.send(forbidden_message)
        except discord.HTTPException as e:
            error_message = f"An error occurred: {e}"
            self.logger.error(error_message)
            await ctx.send(error_message)
    
    @commands.command(name="editchannel", aliases=["ec"], help="Edits a channel's name or topic. eg. !ec 'textchannelName' 'resourceOption' ")
    @commands.has_permissions(manage_channels=True)
    async def edit_channel(self, ctx, channel_name: str, new_resource: str = None):
        """Edits a channel's name or topic."""
        try:
            self.logger.info(f"Edit channel has been called on the channel: {channel_name}, by: {ctx.author}")
            guild = ctx.guild
            channel = discord.utils.get(guild.channels, name=channel_name)
            if channel:
                if new_resource:
                    await channel.edit(resource=new_resource)
                self.logger.info(f"Channel with the name has been successfully edited: {channel_name}, by: {ctx.author}")
                await ctx.send(f"Channel '{channel_name}' updated successfully!")
            else:
                self.logger.info(f"Channel with the name has not been found: {channel_name}")
                await ctx.send(f"Channel '{channel_name}' not found.")
        except discord.Forbidden:
            forbidden_message = "I don't have permission to edit channels."
            self.logger.info(forbidden_message)
            await ctx.send(forbidden_message)
        except discord.HTTPException as e:
            error_massage = f"An error occurred: {e}"
            self.logger.error(error_massage)
            await ctx.send(error_massage)

    @commands.command(name="listgroups", aliases=["lg"], help="List all the groups in the server to help channel creation")
    @commands.has_guild_permissions(manage_channels=True)
    async def list_groups(self, ctx):
        """" Calls list category groups by name"""
        try:
            guild = ctx.guild
            guild_category = guild.categories
            self.logger.info(f"list category groups has been called by: {ctx.author} the guild is: {guild}")
            await ctx.send(f"Here is a full list of available categories: {guild_category}")
        except discord.Forbidden:
            forbidden_message = "I don't have permission to edit channels."
            self.logger.info(forbidden_message)
            await ctx.send(forbidden_message)
        except discord.HTTPException as e:
            error_massage = f"An error occurred: {e}"
            self.logger.error(error_massage)
            await ctx.send(error_massage)

    @commands.command(name="channelinfo", aliases=["ci"], help=" !!!NOT WORKING YET!!! Gives back all the channel related informations. eg. !ci 'textchannelName'")
    @commands.has_guild_permissions(manage_channels=True)
    async def list_groups(self, ctx):
        """" """
        try:
            guild = ctx.guild
            guild_channel = guild.channels.permissions
            self.logger.info(f"Channel information has been called by: {ctx.author} the guild is: {guild}")
            await ctx.send(f"Here is all the information available: {guild_channel}")
        except discord.Forbidden:
            forbidden_message = "I don't have permission to edit channels."
            self.logger.info(forbidden_message)
            await ctx.send(forbidden_message)
        except discord.HTTPException as e:
            error_massage = f"An error occurred: {e}"
            self.logger.error(error_massage)
            await ctx.send(error_massage)
    

async def setup(bot):
    await bot.add_cog(ChannelManager(bot))