import logging
from pathlib import Path


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