"""
FSM States для управления состояниями пользователя в воронках
"""
from aiogram.fsm.state import State, StatesGroup


class FunnelStates(StatesGroup):
    """Состояния для всех воронок (Agency, CG, Express)"""

    # Состояние для выбора направления (fallback)
    choosing_direction = State()

    # Шаг 1: Визуальная квалификация (показываем фото с кнопками)
    step1_qualification = State()

    # Шаг 2: Ожидание контакта (номер телефона)
    step2_waiting_contact = State()

    # Шаг 3: Ожидание ответа на "Золотой Вопрос"
    step3_waiting_golden_question = State()

    # Шаг 4: Ожидание follow-up сообщения (ссылка/ТЗ) - DEPRECATED, больше не используется
    step4_waiting_followup = State()

    # Сценарий "Связь с менеджером": Ожидание контакта для прямой связи
    manager_contact_waiting = State()
