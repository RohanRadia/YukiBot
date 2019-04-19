import asyncio
import os

import aiomysql


async def test_example():
    conn = await aiomysql.connect(

            host=os.environ.get('HOSTNAME'),
            user=os.environ.get('USERNAME'),
            port=int(os.environ.get('PORT')),
            password=os.environ.get('PASSWORD'),
            db=os.environ.get('DATABASE')
    )

    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM guild_settings")
        print(cur.description)
        r = await cur.fetchall()
        print(r)
    conn.close()
    return r


async def main():
    result = await test_example()
    print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

