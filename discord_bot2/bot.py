import discord
from discord.ext import commands
import os
import logging

# Bot prefix (you can change this)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Logging setup
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)  # Set logging level
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load cogs (feature modules)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py': # Check if it is not '__init__.py'
            try: 
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as error:
                print(f"Failed to load extension {filename}: {error}")

# Bot token (replace with your actual token)
TOKEN = "REDACTED"  # Replace with your bot token
bot.run(TOKEN)