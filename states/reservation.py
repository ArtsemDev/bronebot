from aiogram.fsm.state import State, StatesGroup


class RevisionStateGroup(StatesGroup):
    count = State()
    date = State()
    time = State()
