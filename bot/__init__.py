import asyncio
import logging
import os

import aiomysql
import pymysql

from pathlib import Path

# Silence irrelevant loggers
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("websockets").setLevel(logging.ERROR)

consoleLogger = logging.StreamHandler()
logFilePath = Path('bot', 'logs', 'logging.log')
fileLogging = logging.FileHandler(logFilePath)
logging.basicConfig(
    format='%(asctime)s : %(name)s : %(levelname)s: %(message)s',
    datefmt="%D %H:%M:%S",
    level=logging.DEBUG,
    handlers=[consoleLogger, fileLogging]
)

logging.getLogger().info('Logging configuration complete.')

guild_ids = []
guild_prefixes = []


async def test_example(loop):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                  user='root', password='', db='mysql',
                                  loop=loop)

    async with conn.cursor() as cur:
        await cur.execute("SELECT Host,User FROM user")
        print(cur.description)
        r = await cur.fetchall()
        print(r)
    conn.close()


async def mysql_query(query, value=()):
    # Connect to the database
    conn = await aiomysql.connect(
        host=os.environ.get('HOSTNAME'),
        user=os.environ.get('USERNAME'),
        port=int(os.environ.get('PORT')),
        password=os.environ.get('PASSWORD'),
        db=os.environ.get('DATABASE')
    )

    cursor = await conn.cursor()
    data = 'Error'
    try:
        await cursor.execute(query, value)
        logging.info(f'MySQL: {query}')
        data = await cursor.fetchall()
    except Exception as e:
        logging.error(str(e))
    finally:
        conn.close()
        return data


async def mysql_edit(edit, values=()):
    # Connect to the database
    conn = await aiomysql.connect(
        host=os.environ.get('HOSTNAME'),
        user=os.environ.get('USERNAME'),
        port=int(os.environ.get('PORT')),
        password=os.environ.get('PASSWORD'),
        db=os.environ.get('DATABASE')
    )
    cursor = await conn.cursor()
    bool = True
    try:
        await cursor.execute(edit, values)
        await conn.commit()
    except Exception as e:
        bool = False
        logging.getLogger().error(str(e))
    finally:
        logging.getLogger().info(f'MySQL: {edit}')
        conn.close()
        return bool


async def reappend_prefixes():
    guild_ids.clear()
    guild_prefixes.clear()
    all_guilds = await mysql_query("SELECT * FROM guild_settings")
    for guild in all_guilds:
        guild_ids.append(guild[0])
        guild_prefixes.append(guild[1])

loop = asyncio.get_event_loop()
loop.run_until_complete(reappend_prefixes())


