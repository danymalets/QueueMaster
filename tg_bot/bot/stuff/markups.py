from telebot import types

empty_markup = types.ReplyKeyboardRemove()

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add(
    types.KeyboardButton(text="1"),
    types.KeyboardButton(text="2"),
    types.KeyboardButton(text="3")
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
    types.KeyboardButton(text="обновить"),
    types.KeyboardButton(text="выход"),
)


