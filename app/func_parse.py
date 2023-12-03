import asyncio

import sqlite3 as sq

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetUsersRequest

from other import client
from create_bot import bot


async def main_func(channel1, channel2, channel3):
    task1 = asyncio.create_task(dump_all_messages_1(channel1))
    task2 = asyncio.create_task(dump_all_messages_2(channel2))
    task3 = asyncio.create_task(dump_all_messages_3(channel3))

    await task1
    await task2
    await task3


async def find_user(id_):
    return await client(GetUsersRequest([id_]))


async def dump_all_messages_1(channel1):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 3  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 3  # поменяйте это значение, если вам нужны не все сообщения
    while True:
        flag2 = cur.execute("SELECT flag1 FROM count").fetchone()
        if flag2 is not None:
            break
        while True:
            flag2 = cur.execute("SELECT flag1 FROM count").fetchone()
            if flag2 is not None:
                break
            key_words = cur.execute("SELECT keywords FROM counts_keywords").fetchall()
            minus_words = cur.execute("SELECT minuswords FROM counts_minuswords").fetchall()
            history = await client(GetHistoryRequest(
                peer=channel1,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            messages = history.messages

            for message in messages:
                channel_name = str(channel1.to_dict()['title'])
                message_dict = str(message.to_dict()['message'])
                message_id = int(message.to_dict()['id'])
                message_user_id = int(message.to_dict()['from_id']['user_id'])
                full = await find_user(message_user_id)
                message_username = full[0].username
                message_db = (cur.execute
                              ("SELECT message FROM messages WHERE id = {key}".format(key=message_id)).fetchone())
                if message_db is None:
                    message_db = [6578]
                for minus_word in minus_words:
                    for key_word in key_words:
                        if str(message_dict) != str(message_db[0]) and str(key_word[0]) in str(message_dict) and str(
                                minus_word[0]) not in str(message_dict):
                            userid = cur.execute("SELECT userid FROM userid_client").fetchone()
                            await bot.send_message(chat_id=userid[0],
                                                   text=f'*Сообщение:*\n{message_dict}\n\n'
                                                        f'*Пользователь:*\n'
                                                        f'@{message_username}\n\n*Чат:*\n`{channel_name}`',
                                                   parse_mode='Markdown')
                            (cur.execute
                             ("INSERT INTO messages (message, user_id, id) VALUES (?, ?, ?)",
                              (message_dict, message_user_id, message_id)))
                            db.commit()
                        else:
                            pass

                    all_messages.append(message.to_dict())
                offset_msg = 0
                total_messages = len(all_messages)
                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break
        await asyncio.sleep(1)


async def dump_all_messages_2(channel2):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 3  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 3  # поменяйте это значение, если вам нужны не все сообщения
    while True:
        flag2 = cur.execute("SELECT flag2 FROM count").fetchone()
        if flag2 is not None:
            break
        while True:
            flag2 = cur.execute("SELECT flag2 FROM count").fetchone()
            if flag2 is not None:
                break
            key_words = cur.execute("SELECT keywords FROM counts_keywords").fetchall()
            minus_words = cur.execute("SELECT minuswords FROM counts_minuswords").fetchall()
            history = await client(GetHistoryRequest(
                peer=channel2,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            messages = history.messages

            for message in messages:
                channel_name = str(channel2.to_dict()['title'])
                message_dict = str(message.to_dict()['message'])
                message_id = int(message.to_dict()['id'])
                message_user_id = int(message.to_dict()['from_id']['user_id'])
                full = await find_user(message_user_id)
                message_username = full[0].username
                message_db = (cur.execute
                              ("SELECT message FROM messages WHERE id = {key}".format(key=message_id)).fetchone())
                if message_db is None:
                    message_db = [6578]
                for minus_word in minus_words:
                    for key_word in key_words:
                        if str(message_dict) != str(message_db[0]) and str(key_word[0]) in str(message_dict) and str(
                                minus_word[0]) not in str(message_dict):

                            userid = cur.execute("SELECT userid FROM userid_client").fetchone()
                            await bot.send_message(chat_id=userid[0],
                                                   text=f'*Сообщение:*\n{message_dict}\n\n'
                                                        f'*Пользователь:*\n'
                                                        f'@{message_username}\n\n*Чат:*\n`{channel_name}`',
                                                   parse_mode='Markdown')
                            (cur.execute
                             ("INSERT INTO messages (message, user_id, id) VALUES (?, ?, ?)",
                              (message_dict, message_user_id, message_id)))
                            db.commit()
                        else:
                            pass

                    all_messages.append(message.to_dict())
                offset_msg = 0
                total_messages = len(all_messages)
                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break
        await asyncio.sleep(1)


async def dump_all_messages_3(channel3):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 3  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 3  # поменяйте это значение, если вам нужны не все сообщения
    while True:
        flag2 = cur.execute("SELECT flag3 FROM count").fetchone()
        if flag2 is not None:
            db.close()
            break
        while True:
            flag2 = cur.execute("SELECT flag3 FROM count").fetchone()
            if flag2 is not None:
                break
            key_words = cur.execute("SELECT keywords FROM counts_keywords").fetchall()
            minus_words = cur.execute("SELECT minuswords FROM counts_minuswords").fetchall()
            history = await client(GetHistoryRequest(
                peer=channel3,
                offset_id=offset_msg,
                offset_date=None, add_offset=0,
                limit=limit_msg, max_id=0, min_id=0,
                hash=0))
            if not history.messages:
                break
            messages = history.messages

            for message in messages:
                channel_name = str(channel3.to_dict()['title'])
                message_dict = str(message.to_dict()['message'])
                message_id = int(message.to_dict()['id'])
                message_user_id = int(message.to_dict()['from_id']['user_id'])
                full = await find_user(message_user_id)
                message_username = full[0].username
                message_db = (cur.execute
                              ("SELECT message FROM messages WHERE id = {key}".format(key=message_id)).fetchone())
                if message_db is None:
                    message_db = [6578]
                for minus_word in minus_words:
                    for key_word in key_words:
                        if str(message_dict) != str(message_db[0]) and str(key_word[0]) in str(message_dict) and str(
                                minus_word[0]) not in str(message_dict):
                            userid = cur.execute("SELECT userid FROM userid_client").fetchone()
                            await bot.send_message(chat_id=userid[0],
                                                   text=f'*Сообщение:*\n{message_dict}\n\n'
                                                        f'*Пользователь:*\n'
                                                        f'@{message_username}\n\n*Чат:*\n`{channel_name}`',
                                                   parse_mode='Markdown')
                            (cur.execute
                             ("INSERT INTO messages (message, user_id, id) VALUES (?, ?, ?)",
                              (message_dict, message_user_id, message_id)))
                            db.commit()
                        else:
                            pass

                    all_messages.append(message.to_dict())
                offset_msg = 0
                total_messages = len(all_messages)
                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break

        await asyncio.sleep(1)
        