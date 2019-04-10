import json
import random

from discord.ext import commands
from pathlib import Path

with open(Path('bot', 'resources', '8ball.json'), 'r', encoding="utf8") as f:
    eightBallJSON = json.load(f)


class MiniGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('8ball',))
    async def eightball(self, ctx, question: str = None):
        """Mystic Eight Ball - Responds With Random Answer"""

        if question is None:
            await ctx.send("Error, you have to ask a question!")
        else:
            await ctx.send(random.choice(eightBallJSON['answers']))


def setup(bot):
    bot.add_cog(MiniGames(bot))
