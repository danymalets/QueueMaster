from telebot import types

empty_markup = types.ReplyKeyboardRemove()

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add(
    types.KeyboardButton(text="изменить"),
    types.KeyboardButton(text="присоединиться"),
    types.KeyboardButton(text="создать")
)

group_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
group_markup.add(
    types.KeyboardButton(text="создать"),
    types.KeyboardButton(text="обновить"),
    types.KeyboardButton(text="выход")
)

queue_creating_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
queue_creating_markup.add(
    types.KeyboardButton(text="выход")
)

queue_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
queue_markup.add(
    types.KeyboardButton(text="записаться"),
    types.KeyboardButton(text="выписаться"),
    types.KeyboardButton(text="обновить"),
    types.KeyboardButton(text="выход"),
)


