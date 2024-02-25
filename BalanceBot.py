import telebot
import sqlite3
from telebot import types

connect = sqlite3.connect(f'./data.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute(f'create table Money(phone_number str, card_number int, balance_sber int,balance_partners int)')

bot = telebot.TeleBot('7147815324:AAHG2-wR52qQfwdHFZoKxMObvAI_6owVafM')


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
m1 = types.KeyboardButton(text='Остаток')
m2 = types.KeyboardButton(text='Другое')
markup.add(m1, m2)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
m3 = types.KeyboardButton(text='Добавить карты')
m4 = types.KeyboardButton(text='Удалить 1 карту')
m5 = types.KeyboardButton(text='Удалить всё')
m6 = types.KeyboardButton(text='Все телефоны')
m7 = types.KeyboardButton(text='Обновить лимиты')
m8 = types.KeyboardButton(text='Назад')
markup2.add(m3, m4, m5, m6, m7, m8)

markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
m9 = types.KeyboardButton(text='Назад')
markup4.add(m9)

markup5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
m10 = types.KeyboardButton(text='Назад')
markup5.add(m10)

markup6 = types.ReplyKeyboardMarkup(resize_keyboard=True)
m11 = types.KeyboardButton(text='help')
markup6.add(m11)


def make_price_beautiful(price):  # функция для расставдения точек
    rl_price = list(str(price))
    rl_price.reverse()
    res = ""
    for i in range(len(rl_price)):
        if (i + 1) % 3 == 0:
            res += rl_price[i] + "."
        else:
            res += rl_price[i]
    if res[-1] == ".":
        res = res[:-1]
    return res[::-1]


@bot.message_handler()
def start(messege):
    if messege.text in ['/start']:
        bot.send_message(messege.chat.id,'Привет, я бот для работы с наличными по Сбербанк!\n\
Я буду помогать считать лимиты по картам и не запутаться.\n\
Нажми "help", прочти инструкцию и начни работу!',reply_markup=markup6)
    elif messege.text in ['help']:
        bot.send_message(messege.chat.id, '✅ Добавление карт:\n\
\n\
1️⃣ Для добавления карты нужно нажать кнопку «добавить карту»\n\
\n\
2️⃣ Команда "На какой телефон добавить данные?" добавлена для разделения на несколько устройств для работы с мирпей или сберпей\n\
\n\
Вы можете вписать название/номер телефона (можно использовать любые символы)\n\
\n\
3️⃣ Введите 4 последние цифры карты\n\
\n\
Чтобы добавлять сразу несколько напишите 4 последние цифры каждой карты на новой строке\n\
\n\
Формат:\n\
1111\n\
2222\n\
3333\n\
и тд.\n\
\n\
🔥 P.S. Карта добавиться с лимитами 500.000 на сбербанке и банках партнерах\n\
\n\
✅ Изменение лимитов на карте:\n\
\n\
Команду нужно написать боту\n\
\n\
Команда:\n\
«последние 4 цифры карты» «пробел» «s / p» «пробел» «сумма»\n\
\n\
‼️ s - снятие со Сбербанка\n\
‼️ p - снятие с банков партнеров\n\
\n\
Формат:\n\
1111 s 10000\n\
2222 p 500000', reply_markup=markup)

    elif messege.text in ['Назад']:
        bot.send_message(messege.chat.id, 'Успешно', reply_markup=markup)

    elif messege.text in ['Другое']:
        bot.send_message(messege.chat.id, 'Успешно', reply_markup=markup2)

    elif messege.text in ['Добавить карты']:
        mesg = bot.send_message(messege.chat.id, f'На какой телефон добавить данные?:')
        bot.register_next_step_handler(mesg, what_cards_number)

    elif messege.text in ['Удалить всё']:
        mesg = bot.send_message(messege.chat.id, f'Напишите "Yes" если вы уверены что хотите удалить все эллементы',
                                reply_markup=markup4)  # подтверждение удаления
        bot.register_next_step_handler(mesg, are_you_shure)

    elif messege.text in ['Удалить 1 карту']:
        mesg = bot.send_message(messege.chat.id, f'Напишите 4 последние цифры карты которую нужно удалить')
        bot.register_next_step_handler(mesg, delete)

    elif messege.text in ['Остаток']:
        cursor.execute(f'select distinct(phone_number) from Money')
        test = cursor.fetchall()
        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in test:
            markup3.add(types.KeyboardButton(text=str(elem[0])))
        markup3.add(types.KeyboardButton(text='Назад'))
        mesg = bot.send_message(messege.chat.id, f'Напишите на каком телефоне хотите проверить баланс',
                                reply_markup=markup3)
        bot.register_next_step_handler(mesg, view)

    elif messege.text in ['Обновить лимиты']:
        cursor.execute(f'select distinct(phone_number) from Money')
        test = cursor.fetchall()
        markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in test:
            markup3.add(types.KeyboardButton(text=str(elem[0])))
        markup3.add(types.KeyboardButton(text='Назад'))
        mesg = bot.send_message(messege.chat.id,
                                f'По какой карте сбросить лимиты?',
                                reply_markup=markup3)  # подтверждение сброса лимитов
        bot.register_next_step_handler(mesg, shure_apdate_limites)

    elif messege.text in ['Все телефоны']:
        cursor.execute(f'select distinct(phone_number) from Money')
        test = cursor.fetchall()
        for elem in test:
            bot.send_message(messege.chat.id, f'{elem[0]}')

    else:
        text = messege.text.split(' ')  # text = [номер карты , банк , сумма]
        if len(text) != 3:
            bot.send_message(messege.chat.id, f'Вы ввели не существующую команду\nНапишите "help" для вывода инструкции')
        elif text[1] not in 'SsPpСсПп':
            bot.send_message(messege.chat.id, f'Введён не существующий банк')
        else:
            if text[1] in 'SsСс':
                bank = 'balance_sber'
            elif text[1] in 'PpПп':
                bank = 'balance_partners'
            cursor.execute(f'select {bank} from Money where card_number = "{text[0]}"')
            card = cursor.fetchone()
            if card != None:
                cursor.execute(f'update Money set {bank} = {int(card[0]) - int(text[2])} where card_number = {text[0]}')
                connect.commit()
                bot.send_message(messege.chat.id, f'Остаток по карте: {make_price_beautiful(int(card[0]) - int(text[2]))}',reply_markup=markup)
            else:
                bot.send_message(messege.chat.id, f'Такой карты не существует')


def what_cards_number(messege): # функция для добавления карть - 1
    global phone_number
    phone_number = messege.text  # номер телефона
    mesg = bot.send_message(messege.chat.id, f'Введите 4 последние цифры каждой карты на новой строке')
    bot.register_next_step_handler(mesg, add_cards)


def add_cards(messege):        # функция для добавления карть - 2
    global markup
    k = 0  # счётчик добавленных карт
    global card_numbers
    card_numbers = messege.text.split('\n')  # номера карт
    for card_number in card_numbers:  # поочерёдное внесение карт
        cursor.execute(f'select * from Money where card_number = "{card_number}"')
        test = cursor.fetchall()
        if card_number.isdigit():  # проверка на число
            if test == []:  # проверка на дубликаты
                cursor.execute(f'insert into Money values("{phone_number}","{card_number}",500000,500000)')
                connect.commit()
                k += 1
            else:
                bot.send_message(messege.chat.id,
                                 f'Карта {card_number} уже добавлена в таблицу в телефон номер:{test[0][0]}')
        else:
            mesg = bot.send_message(messege.chat.id, f'{card_number} - это не может являться номером карты')
    bot.send_message(messege.chat.id, f'Успешно {k}/{len(card_numbers)}',reply_markup=markup)


def are_you_shure(messege):        #функция для удяления всех эллементов
    if messege.text == 'Yes':
        cursor.execute(f'delete from Money')
        connect.commit()
        bot.send_message(messege.chat.id, f'Успешно',reply_markup=markup)
    elif messege.text == 'Назад':
        bot.send_message(messege.chat.id, f'Вот и славненько', reply_markup=markup)


def delete(messege):  #функция для удаления одного эдемента
    cursor.execute(f'select * from Money where card_number = "{messege.text}"')
    test = cursor.fetchall()
    if test != []:
        cursor.execute(f'delete from Money where card_number = {messege.text}')
        connect.commit
        bot.send_message(messege.chat.id, f'Успешно', reply_markup=markup)
    else:
        bot.send_message(messege.chat.id, f'Такой карты нет в базе', reply_markup=markup)


def view(messege): # функция для вывода остатка
    cursor.execute(
        f'select * from Money where phone_number = "{messege.text}"')  # получаем всю инфу по выбранному телефону
    test = cursor.fetchall()
    if messege.text != 'Назад':
        if test == []:
            bot.send_message(messege.chat.id, f'На этот телефон не зарегестрировано ни одной карты', reply_markup=markup)
        else:
            bot.send_message(messege.chat.id, f'<b>Баланс</b>', parse_mode='html',
                             reply_markup=markup)
            for elem in test:
                if elem[2] == elem[3] == 500000:
                    smile = '✅'
                elif elem[2] == elem[3] == 0:
                    smile = '🅾️'
                else:
                    smile = '🟡'
                bot.send_message(messege.chat.id, f'{smile} <b>{elem[1]}</b> | s - {make_price_beautiful(elem[2])} | p - {make_price_beautiful(elem[3])}', parse_mode='html')
    else:
        bot.send_message(messege.chat.id,f'Успешно',reply_markup=markup)


def shure_apdate_limites(messege): # функция для обновления лимитов
    cursor.execute(f'update Money set balance_sber = 500000 where phone_number = "{messege.text}"')
    cursor.execute(f'update Money set balance_partners = 500000 where phone_number = "{messege.text}"')
    bot.send_message(messege.chat.id, f'Успешно', reply_markup=markup)



if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)