import json
import logging
import random
from pathlib import Path

from discord.ext import commands


logger = logging.getLogger(__name__)

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

    @commands.command(name='choice')
    async def choices(self, ctx, *, options):
        """
        Having a hard time choosing between something?

        Try this command!
        """
        choices = options.split('-')
        choice = random.choice(choices)
        await ctx.send(f'My choice is\"{choice}\"')


def setup(bot):
    bot.add_cog(MiniGames(bot))
    logger.info('MiniGames cog loaded.')
