from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from other.classes import ParseStatesKeywords, ParseStatesMinuswords, ParseStatesLinks

from keybords import *

import sqlite3 as sq


async def add_key_word1(callback: types.CallbackQuery):
    await ParseStatesKeywords.key_words_add.set()
    await callback.answer('Опция выбрана')
    await callback.message.answer('Отправьте слово, которое хотите обозначить как ключевое')


async def delete_key_word1(callback: types.CallbackQuery):
    await ParseStatesKeywords.key_words_delete.set()
    await callback.answer('Опция выбрана')
    await callback.message.answer('Отправьте слово, которое хотите удалить из ключевых')


async def show_key_word1(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Опция выбрана')
    db = sq.connect('tg_message_parse.db')
    cur = db.cursor()
    for word in cur.execute("SELECT keywords FROM counts_keywords").fetchall():
        await callback.message.answer(f'{word[0]}', reply_markup=start_kb())
    await state.finish()
    db.close()


async def add_minus_word1(callback: types.CallbackQuery):
    await ParseStatesMinuswords.minus_words_add.set()
    await callback.answer('Опция выбрана')
    await callback.message.answer('Отправьте слово, которое хотите обозначить как минус слово')


async def delete_minus_word1(callback: types.CallbackQuery):
    await ParseStatesMinuswords.minus_words_delete.set()
    await callback.answer('Опция выбрана')
    await callback.message.answer('Отправьте слово, которое хотите удалить из минус слов')


async def show_minus_word1(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Опция выбрана')
    db = sq.connect('tg_message_parse.db')
    cur = db.cursor()
    for word in cur.execute("SELECT minuswords FROM counts_minuswords").fetchall():
        await callback.message.answer(f'{word[0]}', reply_markup=start_kb())
    await state.finish()
    db.close()


async def links_index_add(callback: types.CallbackQuery):
    await callback.answer('Опция выбрана')
    await callback.message.answer('Отправьте номер индексации для данной ссылки(от 1 до 3)')


async def delete_link1(callback: types.CallbackQuery):
    await ParseStatesLinks.links_delete.set()
    await callback.answer('Опция выбрана')
    await callback.message.answer('Отправьте ссылку на чат, которую хотите удалить')


async def show_links1(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Опция выбрана')
    db = sq.connect('tg_message_parse.db')
    cur = db.cursor()
    data = cur.execute("SELECT links, indexes FROM counts_links").fetchall()
    for row in data:
        link, index = row
        await callback.message.answer(f'<b>Номер индексации:</b>\n{index}\n\n{link}', reply_markup=start_kb(),
                                      parse_mode='html')
    await state.finish()
    db.close()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(add_key_word1, cb_key.filter(action='AddWord+'),
                                       state=ParseStatesKeywords.key_words)
    dp.register_callback_query_handler(delete_key_word1, cb_key.filter(action='DeleteWord+'),
                                       state=ParseStatesKeywords.key_words)
    dp.register_callback_query_handler(show_key_word1, cb_key.filter(action='ShowWords+'),
                                       state=ParseStatesKeywords.key_words)
    dp.register_callback_query_handler(add_minus_word1, cb_key.filter(action='AddWord-'),
                                       state=ParseStatesMinuswords.minus_words)
    dp.register_callback_query_handler(delete_minus_word1, cb_key.filter(action='DeleteWord-'),
                                       state=ParseStatesMinuswords.minus_words)
    dp.register_callback_query_handler(show_minus_word1, cb_key.filter(action='ShowWords-'),
                                       state=ParseStatesMinuswords.minus_words)
    dp.register_callback_query_handler(links_index_add, cb_key.filter(action='AddLink'),
                                       state=ParseStatesLinks.links)
    dp.register_callback_query_handler(delete_link1, cb_key.filter(action='DeleteLink'),
                                       state=ParseStatesLinks.links)
    dp.register_callback_query_handler(show_links1, cb_key.filter(action='ShowLinks'),
                                       state=ParseStatesLinks.links)
