from datetime import datetime
from discord.ext import commands

cogs = ['cogs.owners',
        'cogs.moderation']


class Yuki(commands.Bot):
    def __init__(self):
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
        super().run('TOKEN HERE', reconnect=True) # We can make use of either the DB or configparser for token


if __name__ == '__main__':
    bot = Yuki()
    bot.run()
