from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb_key = CallbackData('ikb', 'action')


def keywords_ikb():
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('👁‍🗨 Показать ключевые слова', callback_data=cb_key.new('ShowWords+'))],
        [InlineKeyboardButton('✅ Добавить слово', callback_data=cb_key.new('AddWord+'))],
        [InlineKeyboardButton('❌ Убрать слово', callback_data=cb_key.new('DeleteWord+'))]
    ])
    return ikb


def minuswords_ikb():
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('👁‍🗨 Показать минус слова', callback_data=cb_key.new('ShowWords-'))],
        [InlineKeyboardButton('✅ Добавить слово', callback_data=cb_key.new('AddWord-'))],
        [InlineKeyboardButton('❌ Убрать слово', callback_data=cb_key.new('DeleteWord-'))]
    ])
    return ikb


def links_ikb():
    ikb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('👁‍🗨 Показать ссылки на чаты', callback_data=cb_key.new('ShowLinks'))],
        [InlineKeyboardButton('✅ Добавить ссылку', callback_data=cb_key.new('AddLink'))],
        [InlineKeyboardButton('❌ Убрать ссылку', callback_data=cb_key.new('DeleteLink'))]
    ])
    return ikb
