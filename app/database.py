import sqlite3 as sq


async def db_start():
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS counts_keywords 
        (keywords TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS counts_minuswords 
            (minuswords TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS counts_links 
            (links TEXT,
            indexes TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS messages
    (message TEXT,
    user_id INTEGER,
    id INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS count
    (flag1 TEXT,
    flag2 TEXT,
    flag3 TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS userid_client
    (userid TEXT)""")

    db.commit()
    db.close()


async def delete_messages():
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    cur.execute("DELETE FROM messages")

    db.commit()
    db.close()


async def db_add_keyword(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("INSERT INTO counts_keywords (keywords) VALUES (?)", (data['keyword'],))

        db.commit()
    db.close()


async def db_delete_keyword(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("DELETE FROM counts_keywords WHERE keywords == ?", (data['keyword'],))

        db.commit()

    db.close()


async def db_add_minusword(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("INSERT INTO counts_minuswords (minuswords) VALUES (?)", (data['minusword'],))

        db.commit()
    db.close()


async def db_delete_minusword(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("DELETE FROM counts_minuswords WHERE minuswords == ?", (data['minusword'],))

        db.commit()

    db.close()


async def db_add_links(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("INSERT INTO counts_links (links, indexes) VALUES (?, ?)", (data['link'], data['index']))

        db.commit()
    db.close()


async def db_delete_links(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    async with state.proxy() as data:
        cur.execute("DELETE FROM counts_links WHERE links == ?", (data['link'],))

        db.commit()

    db.close()


async def db_userid_client(state):
    db = sq.connect('../tg_message_parse.db')
    cur = db.cursor()
    userid_show = cur.execute("SELECT userid FROM userid_client").fetchone()
    if userid_show is None:
        pass
    else:
        cur.execute("DELETE FROM userid_client WHERE userid == ?", (userid_show[0],))
    async with state.proxy() as data:
        cur.execute("INSERT INTO userid_client (userid) VALUES (?)", (data['userid1'],))

        db.commit()
    db.close()
