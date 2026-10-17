"""Finite State Machine (FSM) states for Admin operations."""

from aiogram.fsm.state import State, StatesGroup


class PublishNewsSG(StatesGroup):
    waiting_for_title = State()
    waiting_for_text = State()


class BroadcastSG(StatesGroup):
    waiting_for_text = State()
    confirming = State()
