import discord
from discord.ext import commands
import aiohttp  # For making HTTP requests asynchronously
import json
import logging  # Import the logging module


# Configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Replace if your Ollama runs elsewhere
MODEL_NAME = "huihui_ai/llama3.2-abliterate:latest"  # Replace with your desired model

class LLM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.http_session = aiohttp.ClientSession()  # Create a session for HTTP requests

        # Get the root logger
        self.logger = logging.getLogger("discord.llm") # Create a child logger under 'discord'
        self.logger.setLevel(logging.INFO) # Set the logging level for this specific cog

        # Create a separate file handler for the LLM cog if you want separate log files
        llm_handler = logging.FileHandler(filename="llm.log", encoding="utf-8", mode="w")
        llm_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        llm_handler.setFormatter(llm_formatter)
        self.logger.addHandler(llm_handler)

    async def query_ollama(self, prompt):
        """Sends a prompt to the Ollama API and returns the response."""
        headers = {"Content-Type": "application/json"}
        data = {
            "model": MODEL_NAME,
            "prompt": prompt + "After the response always make a TL;DR as a summary",
            "stream": False,  # Set to True if you want streaming responses
        }

        try:
            self.logger.info(f"Incoming request (query): {prompt}")  # Log the prompt
            async with self.http_session.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data)) as resp:
                if resp.status == 200:
                    response_data = await resp.json()
                    response = response_data["response"]  # Extract the generated text
                    self.logger.info(f"Outgoing response (query): {response}")  # Log the response
                    return response
                else:
                    error_message = f"Error: Ollama API returned status code {resp.status}"
                    print(error_message)
                    self.logger.error(error_message)
                    return None
        except aiohttp.ClientError as e:
            error_message = f"Error: Failed to connect to Ollama API: {e}"
            print(error_message)
            self.logger.error(error_message)
            return None
        
    async def ideas_ollama(self, prompt):
        """"Default Prompt Suggestions"""
        headers = {"Content-Type": "application/json" }
        data = {
            "model": MODEL_NAME,
            "prompt": f"Give 5 prompt suggestions in {prompt} which will start a conversation",
            "stream": False,  # Set to True if you want streaming responses
        }

        try:
            self.logger.info(f"Incoming request (ideas): {prompt}")  # Log the request for ideas
            async with self.http_session.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data)) as resp:
                if resp.status == 200:
                    response_data = await resp.json()
                    response = response_data["response"]  # Extract the generated text
                    self.logger.info(f"Outgoing response (ideas): {response}")  # Log the response
                    return response
                else:
                    error_message = f"Error: Ollama API returned status code {resp.status}"
                    print(error_message)
                    self.logger.error(error_message)
                    return None
        except aiohttp.ClientError as e:
            error_message = f"Error: Failed to connect to Ollama API: {e}"
            print(error_message)
            self.logger.error(error_message)
            return None

    @commands.command(name="ask", help="Ask the LLM a question to get better answers try to be as precise as possible.")
    async def ask(self, ctx, *, question: str):
        """Ask the LLM a question."""
        async with ctx.typing():  # Show typing indicator while processing
            response = await self.query_ollama(question)
            if response:
                for i in range(0, len(response), 2000):
                    chunk = response[i:i + 2000]
                    await ctx.send(chunk)
            else:
                await ctx.send("Sorry, I couldn't get a response from the LLM.")

    @commands.command(name="ideas", help="LLM gives back ideas of questions" )
    async def ideas(self, ctx, *, topic):
        async with ctx.typing():  # Show typing indicator while processing
            response = await self.ideas_ollama(topic)
            if response:
                for i in range(0, len(response), 2000):
                    chunk = response[i:i + 2000]
                    await ctx.send(chunk)
            else:
                await ctx.send("Sorry, I couldn't get a response from the LLM.")
                
    async def cog_unload(self):
        """Close the HTTP session when the cog is unloaded."""
        await self.http_session.close()

async def setup(bot):
    await bot.add_cog(LLM(bot))


    