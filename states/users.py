from aiogram.fsm.state import StatesGroup, State


class TrackingStatesGroup(StatesGroup):
    track_number = State()
