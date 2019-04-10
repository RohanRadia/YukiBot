import configparser

from datetime import datetime
from discord.ext import commands

# All the cogs that are to be loaded on launch
cogs = ['cogs.owners',
        'cogs.moderation',
        'cogs.info',
        'cogs.minigames']

# Open the config.ini file and get bot information
config = configparser.ConfigParser()
config.read('config.ini')


class Yuki(commands.Bot):
    def __init__(self):
        self.lime = 0x04ff00
        super().__init__(command_prefix = '?', # Needs to be changed to allow for database setup, simply a holder ATM
                         description = 'Description Here!')

    async def on_ready(self):
        for cog in cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f'Failed to load extension: {cog}\n{e}')
            else:
                print(f'Loaded extension: {cog}')

        print('---------------------------------\n'
              f'Client Logged in at {datetime.now()}\n'
              f'{self.user.name}\n'
              f'{self.user.id}\n'
              '---------------------------------')
    def run(self):
        super().run(config['BOT']['TOKEN'], reconnect=True) # We can make use of either the DB or configparser for token


if __name__ == '__main__':
    bot = Yuki()
    bot.run()
