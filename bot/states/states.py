"""FSM holatlari."""
from aiogram.fsm.state import State, StatesGroup


class CalculatorStates(StatesGroup):
    waiting_price = State()
    waiting_custom_dp = State()
    waiting_custom_term = State()


class LeadStates(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_rooms = State()
    waiting_payment = State()
    waiting_notes = State()


class AdminStates(StatesGroup):
    waiting_broadcast_message = State()
    waiting_apartment_data = State()
