import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testcommand2(self, ctx):
        await ctx.send('Test Command 2')


def setup(bot):
    bot.add_cog(Owners(bot))
    logger.info('Owners cog loaded !')
