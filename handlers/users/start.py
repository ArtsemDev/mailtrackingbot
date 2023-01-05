from aiogram import Router, F
from aiogram.types import Message

from keyboards.reply import main_panel_kb

start_router = Router(name='start')


@start_router.message(F.text.startswith('/start'))
async def start_command(message: Message):
    await message.answer(
        text=f'Hello {message.from_user.full_name}!',
        reply_markup=main_panel_kb
    )
