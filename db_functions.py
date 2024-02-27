import sqlite3

connect = sqlite3.connect('data.db',
                          check_same_thread=False)

cursor = connect.cursor()


def create_table(name,values):
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS {name}({values})')
    connect.commit()


def get_column_where(name,column,where_column,where_value):
    cursor.execute(f'select {column} from {name} where {where_column} = {where_value}')  # вывод нужного банка на нужной карте
    return cursor.fetchone()


def get_columns_where(name,column,where_column,where_value):
    cursor.execute(f'select {column} from {name} where {where_column} = {where_value}')  # вывод нужного банка на нужной карте
    return cursor.fetchall()


def apdate_values(name,column,where_column,mew_values):
    cursor.execute(
        f'update {name} set {column} = {mew_values} where card_number = {where_column}')  # меняем сумму в счёте
    connect.commit()


def put_values(name,values):
    cursor.execute(f'insert into {name} values({values})')
    connect.commit()


def get_column(name,column):
    cursor.execute(f'select {column} from {name}')
    text = cursor.fetchall()
    text2 = []
    for i in text:
        text2.append(str(i[0]))
    return text2


def delete_out_table(name,where_column,where_value):
    cursor.execute(f'delete from {name} where {where_column} == {where_value}')
    connect.commit()


def delete_table(name):
    cursor.execute(f'delete from {name}')
    connect.commit()





