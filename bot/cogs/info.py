import logging

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=('latency', 'pong'))
    async def ping(self, ctx):
        """Command to Retrieve Latency of Bot"""

        emb = discord.Embed(colour=self.bot.lime)
        emb.add_field(name='Latency', value=f'{round((self.bot.latency * 1000), 2)}')

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Info(bot))
    logger.info('Info cog loaded!')
