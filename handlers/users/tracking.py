from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.evropochta import check_evropochta
from utils.belpost import check_belpost
from states import TrackingStatesGroup
from loader import bot

tracking_router = Router(name='tracking')


@tracking_router.message(F.text == 'ЕВРОПОЧТА 📧')
async def evropochta(message: Message, state: FSMContext = None):
    await message.delete()
    await state.set_state(TrackingStatesGroup.track_number)
    await state.update_data(type='evropochta')
    await message.answer(
        text='***Введите Трек номер посылки!***'
    )


@tracking_router.message(F.text == 'БЕЛПОЧТА ✉️')
async def belpost(message: Message, state: FSMContext = None):
    await message.delete()
    await state.set_state(TrackingStatesGroup.track_number)
    await state.update_data(type='belpost')
    await message.answer(
        text='***Введите Трек номер посылки!***'
    )


async def schedule_check(message: Message, state_data: dict):
    from asyncio import sleep
    while True:
        await sleep(10)
        if state_data.get('type') == 'evropochta':
            response = await check_evropochta(track_number=message.text.replace(' ', ''))
            await message.answer(
                text=f'`{message.text}` \n\n__{response.get("data")[0].get("InfoTrack")}__'
            )
        elif state_data.get('type') == 'belpost':
            response = await check_belpost(track_number=message.text.replace(' ', ''))
            if response:
                await message.answer(
                    text=f'`{message.text} \n\n`__{response.get("data")[0].get("steps")[0].get("event")}__'
                )
            else:
                await sleep(60)


@tracking_router.message(TrackingStatesGroup.track_number)
async def get_track_number(message: Message, state: FSMContext):
    import  asyncio
    await message.delete()
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id - 1
        )
    except TelegramBadRequest:
        pass
    state_data = await state.get_data()
    loop = asyncio.get_running_loop()
    task = loop.create_task(schedule_check(message, state_data))
    if state_data.get('type') == 'evropochta':
        response = await check_evropochta(track_number=message.text.replace(' ', ''))
        if response.get('data')[0].get('ErrorDescription'):
            await message.answer(
                text='***Не верный Трек номер! 😢***\n__Проверьте данные и повторите!__'
            )
        else:
            await state.clear()
            await message.answer(
                text=f'`{message.text}` 👍\n\n__{response.get("data")[0].get("InfoTrack")}__'
            )
            await task
    elif state_data.get('type') == 'belpost':
        response = await check_belpost(track_number=message.text.replace(' ', ''))
        if not response:
            await message.answer(
                text='***Не верный Трек номер! 😢***\n__Проверьте данные и повторите!__'
            )
        else:
            await state.clear()
            await message.answer(
                text=f'`{message.text} 👍\n\n`__{response.get("data")[0].get("steps")[0].get("event")}__'
            )
            await task
