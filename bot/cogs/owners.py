import aiohttp
import logging

from discord.ext import commands


logger = logging.getLogger(__name__)


class Owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='api', aliases=['apicall'])
    @commands.is_owner()
    async def Api_call(self, ctx, url):
        session = self.bot.http_session
        data = await self.fetch(session, url)
        print(data)

    async def fetch(self, session, url):
        params = {}
        headers = {}
        async with session.get(url=url, params=params, headers=headers) as response:
            return await response.json()


def setup(bot):
    bot.add_cog(Owners(bot))
    logger.info('Owners cog loaded !')
