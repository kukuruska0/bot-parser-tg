from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keybords import *

from aiogram import types, Dispatcher

from app import *
from other import *

flag = 'count'


async def start_cmd(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, Добро пожаловать в бот!',
                         reply_markup=start_kb())


async def cancel_cmd(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено ❌', reply_markup=start_kb())


async def key_words_cmd(message: types.Message):
    await ParseStatesKeywords.key_words.set()
    await message.answer('Для возврата в главное меню нажмите на кнопку ❌ Отмена',
                         reply_markup=cancel_kb())
    await message.answer('Выберите опцию ⚙️', reply_markup=keywords_ikb())


async def add_key_word2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['keyword'] = message.text
    await db_add_keyword(state)
    await message.answer('Ключевое слово добавлено ✅', reply_markup=start_kb())
    await state.finish()


async def delete_key_word2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['keyword'] = message.text
    await db_delete_keyword(state)
    await message.answer('Ключевое слово удалено ❌', reply_markup=start_kb())
    await state.finish()


async def minus_words_cmd(message: types.Message):
    await ParseStatesMinuswords.minus_words.set()
    await message.answer('Для возврата в главное меню нажмите на кнопку "❌ Отмена"',
                         reply_markup=cancel_kb())
    await message.answer('Выберите опцию ⚙️', reply_markup=minuswords_ikb())


async def add_minus_word2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['minusword'] = message.text
    await db_add_minusword(state)
    await message.answer('Минус слово добавлено ✅', reply_markup=start_kb())
    await state.finish()


async def delete_minus_word2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['minusword'] = message.text
    await db_delete_minusword(state)
    await message.answer('Минус слово удалено ❌', reply_markup=start_kb())
    await state.finish()


async def links_cmd(message: types.Message):
    await ParseStatesLinks.links.set()
    await message.answer('Для возврата в главное меню нажмите на кнопку ❌ Отмена',
                         reply_markup=cancel_kb())
    await message.answer('Выберите опцию ⚙️', reply_markup=links_ikb())


async def check_index(message: types.Message):
    await message.answer('Неправльный формат ввода❗️❗️❗️')


async def add_link1(message: types.Message, state: FSMContext):
    await ParseStatesLinks.links_add.set()
    async with state.proxy() as data:
        data['index'] = message.text
    await message.answer('Отправьте ссылку на чат, который хотите добавить.\nПример: https://t.me/freelead')


async def add_link2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await db_add_links(state)
    await message.answer('Чат добавлен ✅', reply_markup=start_kb())
    await state.finish()


async def delete_links2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await db_delete_links(state)
    await message.answer('Чат удален ❌', reply_markup=start_kb())
    await state.finish()


async def start_parse(message: types.Message, state: FSMContext):
    await ParseState.start_parse.set()
    async with state.proxy() as data:
        data['userid1'] = message.from_user.id
    await db_userid_client(state)

    await message.answer('Подбор сообщений начался ▶️', reply_markup=parse_kb())

    db = sq.connect('tg_message_parse.db')
    cur = db.cursor()

    if cur.execute("SELECT flag1 FROM count").fetchone() is not None:
        cur.execute("DELETE FROM count WHERE flag1 == ?", (flag,))
    if cur.execute("SELECT flag2 FROM count").fetchone() is not None:
        cur.execute("DELETE FROM count WHERE flag2 == ?", (flag,))
    if cur.execute("SELECT flag3 FROM count").fetchone() is not None:
        cur.execute("DELETE FROM count WHERE flag3 == ?", (flag,))
    db.commit()

    url1 = cur.execute("SELECT links FROM counts_links WHERE indexes == '1'").fetchone()
    url2 = cur.execute("SELECT links FROM counts_links WHERE indexes == '2'").fetchone()
    url3 = cur.execute("SELECT links FROM counts_links WHERE indexes == '3'").fetchone()
    channel1 = await client.get_entity(url1[0])
    channel2 = await client.get_entity(url2[0])
    channel3 = await client.get_entity(url3[0])
    await main_func(channel1, channel2, channel3)


async def cancel_parse(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Пересылка отключена ❌', reply_markup=start_kb())
    db = sq.connect('tg_message_parse.db')
    cur = db.cursor()
    cur.execute("INSERT INTO count (flag1, flag2, flag3) VALUES (?, ?, ?)", (flag, flag, flag))
    db.commit()


def register_message_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_message_handler(cancel_cmd, Text(equals='❌ Отмена'), state='*')
    dp.register_message_handler(key_words_cmd, Text(equals='🔑 Ключевые слова'))
    dp.register_message_handler(add_key_word2, state=ParseStatesKeywords.key_words_add)
    dp.register_message_handler(delete_key_word2, state=ParseStatesKeywords.key_words_delete)
    dp.register_message_handler(minus_words_cmd, Text(equals='➖ Минус слова'))
    dp.register_message_handler(add_minus_word2, state=ParseStatesMinuswords.minus_words_add)
    dp.register_message_handler(delete_minus_word2, state=ParseStatesMinuswords.minus_words_delete)
    dp.register_message_handler(links_cmd, Text(equals='💬 Чаты'))
    dp.register_message_handler(check_index,
                                lambda message: message.text != '1' and message.text != '2' and message.text != '3',
                                state=ParseStatesLinks.links)
    dp.register_message_handler(add_link1, state=ParseStatesLinks.links)
    dp.register_message_handler(add_link2, state=ParseStatesLinks.links_add)
    dp.register_message_handler(delete_links2, state=ParseStatesLinks.links_delete)
    dp.register_message_handler(start_parse, Text(equals='▶️ Начать подбор сообщений'))
    dp.register_message_handler(cancel_parse, Text(equals='❌ Отключить пересылку'),
                                state=ParseState.start_parse)
