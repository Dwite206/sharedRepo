import discord
from discord.ext import commands
import sqlite3

class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "data/points.db"  # Path to your database file
        self.create_table()

    def create_table(self):
        """Creates the points table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS points (
                user_id INTEGER PRIMARY KEY,
                points INTEGER DEFAULT 0
            )
        """)
        conn.commit()
        conn.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Points cog is ready.")

    def get_points(self, user_id):
        """Retrieves the points for a given user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT points FROM points WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return 0  # User not in the database yet

    def add_points(self, user_id, amount):
        """Adds points to a user's balance."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Insert or update
        cursor.execute("""
            INSERT INTO points (user_id, points) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET points = points + ?
        """, (user_id, amount, amount))

        conn.commit()
        conn.close()

    def remove_points(self, user_id, amount):
        """Removes points from a user's balance."""
        current_points = self.get_points(user_id)
        if current_points >= amount:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE points SET points = points - ? WHERE user_id = ?", (amount, user_id))
            conn.commit()
            conn.close()
            return True
        else:
            return False # Not enough points

    @commands.command(name="balance")
    async def balance(self, ctx):
        """Displays the user's current point balance."""
        user_id = ctx.author.id
        points = self.get_points(user_id)
        await ctx.send(f"{ctx.author.mention}, you have {points} points!")

async def setup(bot):
    await bot.add_cog(Points(bot))