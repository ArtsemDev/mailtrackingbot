from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()

bot = Bot(
    token=getenv('BOT_TOKEN'),
    parse_mode='Markdown'
)
dp = Dispatcher()
