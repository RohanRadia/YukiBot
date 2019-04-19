import logging

import discord
from discord.ext import commands

from bot import mysql_edit, mysql_query, guild_ids, guild_prefixes


logger = logging.getLogger(__name__)


class BotEvents(commands.Cog):
    """A cog to handle events."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logger.info(f'The bot joined server : {guild.name}')
        guild_id = guild.id
        prefix = '?'
        log_channel = 0
        guild_info = (guild_id, prefix, log_channel)
        default_cmd_status = (guild_id,)
        sql = await mysql_edit("INSERT INTO guild_settings VALUES (%s, %s, %s)", guild_info)
        print(sql)
        sql2 = await mysql_edit("INSERT INTO command_status(guild_id) VALUES (%s)", default_cmd_status)
        print(sql2)
        guild_ids.append(guild_id)
        guild_prefixes.append(prefix)
        print(guild_ids)
        print(guild_prefixes)
        embed = await self.settings_embed(guild_id)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logger.info(f'The bot was removed from {guild.name}')
        remove_settings = await mysql_edit('DELETE FROM guild_settings WHERE guild_id=%s', (guild.id,))
        remove_cmd_status = await mysql_edit('DELETE FROM command_status WHERE guild_id=%s', (guild.id,))
        index = guild_ids.index(guild.id)
        guild_ids.remove(guild_ids[index])
        guild_prefixes.remove(guild_prefixes[index])
        print(guild_ids)
        print(guild_prefixes)
        print(remove_settings)
        print(remove_cmd_status)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # sql = mysql_query('SELECT logs FROM command_status WHERE guild_id = %s', (426566445124812813,))
        log_channel = await mysql_query('SELECT log_channel FROM guild_settings WHERE guild_id = %s', (before.guild.id,))
        if log_channel[0][0] == 0:
            pass
        else:
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.title = f'Message edited\nby {before.author} in #{before.channel}'
            embed.description = ''
            embed.add_field(name='Before', value=before.content, inline=False)
            embed.add_field(name='After', value=after.content, inline=False)
            channel = self.bot.get_channel(log_channel[0][0])
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # sql = await mysql_query('SELECT logs FROM command_status WHERE guild_id = %s', (426566445124812813,))
        log_channel = await mysql_query('SELECT log_channel FROM guild_settings WHERE guild_id = %s', (message.guild.id,))
        if log_channel[0][0] == 0:
            pass
        else:
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.title = f'Message deleted\nby {message.author} in #{message.channel}'
            embed.description = message.content
            channel = self.bot.get_channel(log_channel[0][0])
            await channel.send(embed=embed)

    # USE OF TESTING on_guild_join()
    # @commands.command(name='testdb')
    # async def test_db(self, ctx):
    #     guild_id = ctx.guild.id
    #     prefix = self.bot.command_prefix
    #     log_channel = 0
    #     guild_info = (guild_id,  prefix, log_channel)
    #     default_cmd_status = (ctx.guild.id,)
    #     sql = await mysql_edit("INSERT INTO guild_settings VALUES (%s, %s, %s)", guild_info)
    #     print(sql)
    #     sql2 = await mysql_edit("INSERT INTO command_status(guild_id) VALUES (%s)", default_cmd_status)
    #     print(sql2)
    #     embed = self.settings_embed(ctx)
    #     await ctx.send(embed=embed)

    @commands.command(name='settings')
    async def send_config(self, ctx):
        embed = await self.settings_embed(ctx.guild.id)
        await ctx.send(embed=embed)

    async def settings_embed(self, guild_id):
        cmd_status = await mysql_query("SELECT * FROM command_status WHERE guild_id=%s", (guild_id,))
        cmd_status = cmd_status[0]
        guild_settings = await mysql_query("SELECT * FROM guild_settings WHERE guild_id=%s", (guild_id,))
        cols = await mysql_query("desc command_status")
        col_names = []
        for col in cols:
            col_names.append(col[0].replace('_', ' '))
        info_dict = {
            'purge': f"This command is for deleting messages in a channel.\n"
                     f"You can enable it by using {guild_settings[0][1]}enable purge",

            'logs': f"This is like audit logs but with more information.\n"
                    f"You can enable it by using {guild_settings[0][1]}enable logs <channel id> or just\n"
                    f"{guild_settings[0][1]}enable logs and the bot will create a channel called logs.",

            'member join message': f"This is the message sent when a memebr joins the server\n"
                                   f"Enable this by using {guild_settings[0][1]}enable joinmsg-<message>"
        }
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = 'Guild Settings'
        embed.description = ''
        embed.add_field(name='Prefix',
                        value=f'**Prefix : {guild_settings[0][1]}**\n'
                              f'You can change the prefix by using {guild_settings[0][1]}prefix <new prefix> command.',
                        inline=False)
        if guild_settings[0][2] == 0:
            log_channel = None
            log_channel_id = 0
        else:
            channel = self.bot.get_channel(guild_settings[0][2])
            log_channel = channel.name
            log_channel_id = channel.id
        embed.add_field(name='Log Channel', value=f'Channel - #{log_channel}\nID - {log_channel_id}', inline=False)
        for i in range(1, len(col_names)):
            embed.add_field(
                name=col_names[i].capitalize(),
                value=f'**Command : {cmd_status[i].capitalize()}**\n'
                      f'{info_dict[col_names[i]]}',
                inline=False
            )
        return embed


def setup(bot):
    bot.add_cog(BotEvents(bot))
    logger.info('Events cog loaded !')
