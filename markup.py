from telebot import types

def create_markup(list_markup):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(list_markup)):
            list_markup[i] = types.KeyboardButton(text = list_markup[i])
        markup.add(*list_markup)
        return markup

