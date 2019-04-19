import logging

from discord.ext import commands

from bot import mysql_query, mysql_edit, reappend_prefixes

logger = logging.getLogger(__name__)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete', aliases=['del', 'd', 'purge'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages have been deleted!')

    @commands.command(name='prefix', aliases=['p'])
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix):
        data = (new_prefix, ctx.guild.id)
        prefix_update = await mysql_edit('UPDATE guild_settings SET prefix=%s WHERE guild_id = %s', data)
        print(prefix_update)
        await reappend_prefixes()
        await ctx.send(f'The prefix has been changed to `{new_prefix}`')

    @commands.group(name='enable', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def enable_features(self, ctx, feature=None):
        pass

    @enable_features.command(name='logs')
    async def enable_logs(self, ctx, channel_id=None):
        status = await mysql_query('SELECT logs FROM command_status WHERE guild_id=%s', (ctx.guild.id,))
        if status[0][0] == 'enabled':
            return await ctx.send("Logs is already enabled!")
        if channel_id is None:
            guild = self.bot.get_guild(ctx.guild.id)
            channel = await guild.create_text_channel('logs')
            channel_id = channel.id
        else:
            pass
        guild = self.bot.get_guild(ctx.guild.id)
        add_log_data = (channel_id, ctx.guild.id)
        enable_data = ('enabled', ctx.guild.id)
        channels = [channel.id for channel in guild.channels]
        print(channels)
        print(channel_id)
        if channel_id in channels:
            return await ctx.send("Incorrect channel id")
        add_log_channel = await mysql_edit('UPDATE guild_settings SET log_channel=%s WHERE guild_id = %s', add_log_data)
        enable_logs = await mysql_edit('UPDATE command_status SET logs=%s WHERE guild_id = %s', enable_data)
        await ctx.send("logs has been now enabled!")
        print(add_log_channel)
        print(enable_logs)

    @commands.group(name='disable', invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def disable_features(self, ctx, feature=None):
        pass

    @disable_features.command(name='logs')
    async def disable_logs(self, ctx):
        status = await mysql_query('SELECT logs FROM command_status WHERE guild_id=%s', (ctx.guild.id,))
        if status[0][0] == 'disabled':
            return await ctx.send("Logs are already disabled!")
        data = (0, ctx.guild.id)
        disable_data = ('disabled', ctx.guild.id)
        set_log_channel = await mysql_edit('UPDATE guild_settings SET log_channel=%s WHERE guild_id = %s', data)
        disable_logs_feature = await mysql_edit('UPDATE command_status SET logs=%s WHERE guild_id = %s', disable_data)
        await ctx.send('Logs are now disabled!')
        print(set_log_channel)
        print(disable_logs_feature)


def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.info('Moderation cog loaded !')
