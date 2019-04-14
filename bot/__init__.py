import logging
import os
import pymysql.cursors
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


def mysql_query(query):
    # Connect to the database
    conn = pymysql.connect(
        host=os.environ.get('HOSTNAME'),
        user=os.environ.get('USERNAME'),
        port=os.environ.get('PORT'),
        password=os.environ.get('PASSWORD'),
        db=os.environ.get('DATABASE'),
    )
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        logging.info(f'MySQL: {query}')
        c = cursor.fetchall()
    except Exception as e:
        logging.error(str(e))
    finally:
        conn.close()
        return c


def mysql_edit(edit):
    # Connect to the database
    conn = pymysql.connect(
        host=os.environ.get('HOSTNAME'),
        user=os.environ.get('USERNAME'),
        port=os.environ.get('PORT'),
        password=os.environ.get('PASSWORD'),
        db=os.environ.get('DATABASE'),
    )
    cursor = conn.cursor()
    try:
        cursor.execute(edit)
        conn.commit()
        logging.getLogger().info(f'MySQL: {edit}')
    except Exception as e:
        logging.getLogger().error(str(e))
    finally:
        conn.close()
        return True
