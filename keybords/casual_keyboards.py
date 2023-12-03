from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('🔑 Ключевые слова'), KeyboardButton('➖ Минус слова')],
        [KeyboardButton('💬 Чаты')],
        [KeyboardButton('▶️ Начать подбор сообщений')],
        [KeyboardButton('🗑 Очистить историю сообщений')]
    ])
    return kb


def cancel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('❌ Отмена')]
    ])
    return kb


def parse_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton('❌ Отключить пересылку')]
    ])
    return kb
