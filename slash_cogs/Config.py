# ------Discord------
from discord.ext import commands
from discord import app_commands
import discord
# ------Other--------
from pypinyin import lazy_pinyin, Style
from typing import List

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Config(bot))
