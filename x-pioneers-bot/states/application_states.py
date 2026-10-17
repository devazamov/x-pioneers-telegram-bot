"""Finite State Machine (FSM) states for team application process."""

from aiogram.fsm.state import State, StatesGroup


class ApplicationSG(StatesGroup):
    waiting_for_name = State()
    waiting_for_interest = State()
    waiting_for_skills = State()
    waiting_for_motivation = State()
    reviewing = State()
