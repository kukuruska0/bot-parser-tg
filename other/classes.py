from aiogram.dispatcher.filters.state import StatesGroup, State


class ParseStatesKeywords(StatesGroup):
    key_words = State()
    key_words_add = State()
    key_words_delete = State()


class ParseStatesMinuswords(StatesGroup):
    minus_words = State()
    minus_words_add = State()
    minus_words_delete = State()


class ParseStatesLinks(StatesGroup):
    links = State()
    links_index = State()
    links_add = State()
    links_delete = State()


class ParseState(StatesGroup):
    start_parse = State()
