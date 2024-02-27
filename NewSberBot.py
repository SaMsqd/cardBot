import telebot
import sqlite3
from functions_menu import *
from functions import *
from db_functions import *
from markup import create_markup

bot = telebot.TeleBot('2054290165:AAGNEgLlp1eUDWs_NRldLCnshWl4-5nx-ug')

create_table('Money',
             'phone_number str, card_number int, balance_sber int,balance_partners int')

create_table('Phones',
             'number str')


@bot.message_handler()
def work(message): # распределение по функциям
    if message.text in ['/start']:
        start(message)
    elif message.text in ['Лимиты']:
        limited(message)
    elif message.text in ['Меню']:
        menu(message)
    elif message.text in ['Назад']:
        back(message)
    elif message.text in ['Добавить']:
        add(message)
    elif message.text in ['Добавить карту']:
        add_card(message)
    elif message.text in ['Добавить телефон']:
        add_phone(message)
    elif message.text in ['Удалить']:
        delete(message)
    elif message.text in ['Удалить карту']:
        delete_card(message)
    elif message.text in ['Удалить телефон']:
        delete_phone(message)
    elif message.text in ['Удалить всё']:
        delete_all(message)
    elif message.text in ['Обновить']:
        update(message)
    else:
        limits(message)


########################################################################################################################

# функция для списаний с карты
def limits(message):
    text = message.text.split(' ')  # text = [номер карты , банк , сумма]
    if len(text) == 3 and out_dots(text[2]).isdigit():
        limits3(text, message)
    elif len(text) == 4 and text[2].isdigit() and text[3].isdigit():  # объединение чисел если сумма введена через пробел
        text[2] = text[2] + text[3]
        limits3(text, message)
    else:
        bot.send_message(message.chat.id,
                         f'Введёна несуществующая команда',
                         reply_markup=m_start)


def limits3(text,message):
    if text[1] not in 'sp': # проверка на правильность ввода банка
        bot.send_message(message.chat.id,
                         f'Введён не существующий банк',
                         reply_markup=m_start) # возврат к начальному экрану
    else:
        text[2] = out_dots(text[2]) # убираем точки из чисел
        if text[1] in 's': # присваивание сбербанка банку
            bank = 'balance_sber'
        elif text[1] in 'p': # присваивание партнёров банку
            bank = 'balance_partners'
        card = get_column_where('Money',
                                f'{bank}',
                                'card_number',text[0])
        if card != None: # если card == None значит такой карты нет в базе
            apdate_values('Money',bank,text[0],int(card[0]) - int(text[2]))
            bot.send_message(message.chat.id,
                             f'Остаток по карте: {make_price_beautiful(int(card[0]) - int(text[2]))}',
                             reply_markup=m_start) # возврат к начальному экрану
        else:
            bot.send_message(message.chat.id,
                             f'Такой карты не существует',
                             reply_markup=m_start) # возврат к начальному экрану


#######################################################################################################################

# функция для добовления карты
def add_card(message):
    test = get_column('Phones', # получаем все телефоны
                      'number')
    test.append('Назад')
    m_add_card = create_markup(test) # создаем кнопки со всеми телефонами
    mesg = bot.send_message(message.chat.id,
                            'Выберите устройство, на которое хотите добавить карту:  ',
                            reply_markup=m_add_card)
    bot.register_next_step_handler(mesg,add_card_2)


def add_card_2(message):
    test = get_column('Phones',
                      'number') # получаем все телефоны
    global phone_number # обязательно так как в add_card_3 нам нужна будет эта переменная
    phone_number = message.text  # номер телефона
    if message.text in ['Назад']:
        bot.send_message(message.chat.id,
                         'Успешно',
                         reply_markup=m_menu)# возврат в меню
    elif message.text not in test: # проверка на наличие телефона в базе во избежании случайного добавления на несуществующий телефон
        bot.send_message(message.chat.id,
                         'Такого телефона не зарегестрировано',
                         reply_markup=m_menu)# возврат в меню
    else: # если телефон зарегестрирован в базе добавляем ему карту
        mesg = bot.send_message(message.chat.id,
                                f'Напишите последние 4 цифры карты.\n\
Для добавления нескольких карт, каждую карту пишите с новой строки\n\
пример: \n\
1567 \n\
3400 \n\
6789 \n\
....  ')
        bot.register_next_step_handler(mesg,
                                       add_card_3)
##################

def add_card_3(messege):
    k = 0  # счётчик добавленных карт
    card_numbers = messege.text.split('\n')  # номера карт
    for card_number in card_numbers:  # поочерёдное внесение карт
        test = get_columns_where('Money',
                                 '*',
                                 'card_number',
                                 f'"{card_number}"') # получения карты с таким же номером во избежании дубликатов
        if card_number.isdigit() and len(card_number)==4:  # проверка на число(т.к. номер карты должна быть числом)
            if test == None or test == []:  # проверка на дубликаты
                put_values('Money',
                           f'"{phone_number}","{card_number}",500000,500000')
                k += 1 # увеличение счётчика добавленных карт
            else: # если карта с таким номером уже существует то мы её не добавляем
                bot.send_message(messege.chat.id,
                                 f'Карта {card_number} уже добавлена в таблицу в телефон:{test[0][0]}')
        else: # если введёный номер не число то мы не принимает его как номер карты
            bot.send_message(messege.chat.id,
                                    f'{card_number} - это не может являться номером карты')
    bot.send_message(messege.chat.id,
                     f'Добавлено {k} карт(ы/a) из {len(card_numbers)}',
                     reply_markup=m_menu)# возврат в меню


########################################################################################################################

# функция добавления телефона
def add_phone(message):
    mesg = bot.send_message(message.chat.id,
                            'Напишите название устройства.\n\
пример: \n\
самсунг A3 или просто 1,2,3',
                            reply_markup=m_back)
    bot.register_next_step_handler(mesg,add_phone_2)


def add_phone_2(message):
    test = get_column('Phones',  # получаем список имеющихся телефонов
                      'number')
    if message.text in ['Назад']: # возврат в меню
        bot.send_message(message.chat.id,
                         'Успешно',
                         reply_markup=m_menu)
    else:
        if message.text not in test: # добавляем телефон если такого уже нет
            put_values('Phones',
                       f'"{message.text}"')
            mesg = bot.send_message(message.chat.id,
                                    'Успешно',
                                    reply_markup=m_add_phone)
            bot.register_next_step_handler(mesg,add_phone_3)
        else: # не добавляем телефон если такой уже есть
            mesg = bot.send_message(message.chat.id,
                                    'Такой телефон уже существует',
                                    reply_markup=m_menu)


def add_phone_3(message):
    if message.text in ['Назад']:
        bot.send_message(message.chat.id,
                         'Успешно',
                         reply_markup=m_menu)  # возврат в меню
    elif message.text in ['Добавить ещё']: # перенаправляем в начало для добавления нового телефона
        mesg = bot.send_message(message.chat.id,
                                'Напишите название устройства.\n\
пример: \n\
самсунг A3 или просто 1,2,3',
                                reply_markup=m_back)
        bot.register_next_step_handler(mesg, add_phone_2)


########################################################################################################################

# функция для удаления одной карты
def delete_card(message):
    mesg = bot.send_message(message.chat.id,
                            'Напиши последние 4 цифры карты, которую хотите удалить')
    bot.register_next_step_handler(mesg,delete_card_2)


def delete_card_2(message):
    test = get_columns_where('Money',  # получаем номер указаной карты
                             'card_number',
                             'card_number',
                             f'"{message.text}"')
    if test == []: # если test == [] значит такой карты не существует
        bot.send_message(message.chat.id,
                         f'Такой карты не существует',
                         reply_markup=m_menu)
    else:
        test = test[0][0] # избавляемся от вида [(1234,)]
        delete_out_table('Money',
                         'card_number',
                         f'{test}')
        bot.send_message(message.chat.id,
                         f'Успешно',
                         reply_markup=m_menu) # аозврат в меню


########################################################################################################################

# функция для удаления телефона
def delete_phone(message):
    test = get_column('Phones',  # получаем все телефоны
                      'number')
    test.append('Назад')
    m_delete_phone = create_markup(test)  # создаем кнопки со всеми телефонами
    mesg = bot.send_message(message.chat.id,
                            f'Выберите устройство, которое хотите удалить:',
                            reply_markup=m_delete_phone)
    bot.register_next_step_handler(mesg,
                                   delete_phone_2)


def delete_phone_2(message):
    test = get_column('Phones',  # получаем все телефоны
                      'number')
    if message.text in ['Назад']:
        bot.send_message(message.chat.id,
                         'Успешно',
                         reply_markup=m_menu)  # возврат в меню
    elif message.text in test:
        delete_out_table('Phones','number',f'{message.text}')
        delete_out_table('Money', 'phone_number', f'{message.text}')
        bot.send_message(message.chat.id,
                         f'Успешно',
                         reply_markup=m_menu)
    else:
        bot.send_message(message.chat.id,
                         'Такого телефона не существует',
                         reply_markup=m_menu)


########################################################################################################################

# функция для удаления всего
def delete_all(mesage):
    mesg = bot.send_message(mesage.chat.id,
                            f'Вы точно уверены, что хотите удалить все данные?  ',
                            reply_markup=m_delete_all)
    bot.register_next_step_handler(mesg,
                                   delete_all_2)


def delete_all_2(message):
    if message.text in ['Да']:
        delete_table('Phones')
        delete_table('Money')
        bot.send_message(message.chat.id,
                         f'Успешно',
                         reply_markup=m_menu)
    elif message.text in ['Нет']:
        bot.send_message(message.chat.id,
                         f'Данные не удалились',
                         reply_markup=m_menu)


########################################################################################################################

# функция для обновления лимитов
def update(message):
    test = get_column('Phones',  # получаем все телефоны
                      'number')
    test.append('Обновить всё')
    test.append('Назад')
    m_update = create_markup(test)  # создаем кнопки со всеми телефонами
    mesg = bot.send_message(message.chat.id,
                            f'Bыберите устройство на котором хотите обновить лимиты  ',
                            reply_markup=m_update)
    bot.register_next_step_handler(mesg,
                                   update_2)


def update_2(message):
    if message.text in ['Назад']:
        bot.send_message(message.chat.id,
                         'Успешно',
                         reply_markup=m_menu)  # возврат в меню
    elif message.text in ['Обновить всё']:
        cursor.execute(f'update Money set balance_sber = 500000')
        cursor.execute(f'update Money set balance_partners = 500000')
        connect.commit()
        bot.send_message(message.chat.id,
                         f'Успешно',
                         reply_markup=m_menu)
    else:
        cursor.execute(f'update Money set balance_sber = 500000 where phone_number = "{message.text}"')
        cursor.execute(f'update Money set balance_partners = 500000 where phone_number = "{message.text}"')
        connect.commit()
        bot.send_message(message.chat.id,
                         f'Успешно',
                         reply_markup=m_menu)


########################################################################################################################

# функция для вывода лимитов
def limited(message):
    test = get_column('Phones',  # получаем все телефоны
                      'number')
    test.append('Назад')
    markup3 = create_markup(test)
    mesg = bot.send_message(message.chat.id, f'Напишите на каком телефоне хотите проверить баланс',
                            reply_markup=markup3)
    bot.register_next_step_handler(mesg, limited_2)
    cursor.execute(
        f'select * from Money where phone_number = "{message.text}"')  # получаем всю инфу по выбранному телефону
    test = cursor.fetchall()


def limited_2(message):
    cursor.execute(
        f'select * from Money where phone_number = "{message.text}"')  # получаем всю инфу по выбранному телефону
    test = cursor.fetchall()
    if message.text != 'Назад':
        if test == []:
            bot.send_message(message.chat.id, f'На этот телефон не зарегестрировано ни одной карты',
                                 reply_markup=m_menu)
        else:
            bot.send_message(message.chat.id, f'<b>Баланс</b>', parse_mode='html',
                                 reply_markup=m_menu)
            for elem in test:
                if elem[2] == elem[3] == 500000:
                    smile = '✅'
                elif elem[2] == elem[3] == 0:
                    smile = '🅾️'
                else:
                    smile = '🟡'
                bot.send_message(message.chat.id,
                                f'{smile} <b>{elem[1]}</b> | s - {make_price_beautiful(elem[2])} | p - {make_price_beautiful(elem[3])}',
                                parse_mode='html')
    else:
        bot.send_message(message.chat.id,
                         f'Успешно',
                         reply_markup=m_menu)


########################################################################################################################

if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
