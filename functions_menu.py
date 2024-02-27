import telebot
from markup import create_markup

bot = telebot.TeleBot('7147815324:AAHG2-wR52qQfwdHFZoKxMObvAI_6owVafM')



m_start = create_markup(['Лимиты',
                         'Меню'])

m_menu = create_markup(['Добавить',
                        'Удалить',
                        'Обновить',
                        'Назад'])

m_add = create_markup(['Добавить карту',
                       'Добавить телефон',
                       'Назад'])

m_back = create_markup(['Назад'])

m_add_phone = create_markup(['Добавить ещё',
                             'Назад'])

m_delete = create_markup(['Удалить карту',
                          'Удалить телефон',
                          'Удалить всё',
                          'Назад'])

m_delete_all = create_markup(['Да',
                             'Нет'])

def start(message): # начало работы/приветствие
    bot.send_message(message.chat.id,
                     'Привет 👋 Я бот по работе с Лимитами!\nМоя функция считать лимиты и вести учет карт.',
                     reply_markup=m_start)

def menu(message): # вызов меню
    bot.send_message(message.chat.id,
                     'Выберите необходимый раздел',
                     reply_markup=m_menu)

def back(message):
    bot.send_message(message.chat.id,
                     'Успешно',
                     reply_markup=m_start)


def add(message):
    bot.send_message(message.chat.id,
                     'Выберите что вы хотите добавить',
                     reply_markup=m_add)


def delete(message):
    bot.send_message(message.chat.id,
                     'Выберите что вы хотите удалить',
                     reply_markup=m_delete)
