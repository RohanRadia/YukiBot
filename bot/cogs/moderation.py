import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testcommand1(self, ctx):
        """Holder Command To Be Over Written"""

        await ctx.send('Test Command 1')


def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.info('Moderation cog loaded !')
