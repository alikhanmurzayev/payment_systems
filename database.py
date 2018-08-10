import sqlite3
import pandas
import os
import datetime

import config

def open_connection(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return conn, cursor
def close_connection(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()


def drop_table(table_name):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"DROP TABLE {table_name}"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)

def create_companies_table():
    conn, cursor = open_connection(config.database_name)
    # Create database if it does not exist
    try:
        query = f"CREATE TABLE {config.companies_table} " \
                f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, company varchar, " \
                f"email varhcar, password varchar)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def update_companies_table(company, email, password):
    conn, cursor = open_connection(config.database_name)
    check_existence = f"SELECT * FROM {config.companies_table} WHERE company='{company}'"
    result = cursor.execute(check_existence).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {config.companies_table} (company, email, password) " \
                f"VALUES ('{company}', '{email}', '{password}')"
        cursor.execute(query)
    close_connection(conn, cursor)

def get_company(company):
    conn, cursor = open_connection(config.database_name)
    # Create database if it does not exist
    query = f"SELECT email, password FROM {config.companies_table} WHERE company='{company}'"
    result = cursor.execute(query).fetchall()
    close_connection(conn, cursor)
    return result[0][0], result[0][1]



def create_messages_table():
    conn, cursor = open_connection(config.database_name)
    # Create database if it does not exist
    try:
        query = f"CREATE TABLE {config.messages_table} " \
                f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, message_id int, " \
                f"company varchar)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def get_unread_messages(id_list, company):
    conn, cursor = open_connection(config.database_name)
    unread_id = list()
    for message_id in id_list:
        message_id_int = int(message_id)
        query = f"SELECT * FROM {config.messages_table} WHERE message_id='{message_id_int}' " \
                f"and company='{company}'"
        result = cursor.execute(query).fetchall()
        if len(result) == 0:
            unread_id.append(message_id)
    close_connection(conn, cursor)
    return unread_id
def add_messages(message_id_list, company):
    conn, cursor = open_connection(config.database_name)
    for message_id in message_id_list:
        message_id = int(message_id)
        query = f"INSERT INTO {config.messages_table} (message_id, company) " \
                f"VALUES ('{message_id}', '{company}')"
        cursor.execute(query)
    close_connection(conn, cursor)


def create_payment_trans_table():
    conn, cursor = open_connection(config.database_name)
    # Create database if it does not exist
    try:
        query = f'CREATE TABLE {config.payment_trans_table} ' \
                f'(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, date date, date_created date, ' \
                f'order_id varchar, payment_amount double, payment_type varchar, ' \
                f'payment_reference varchar, status int, key_1 varchar, key_2 varchar, company varchar)'
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def update_payment_trans_table(date, date_created, order_id, payment_amount,
                                      payment_type, payment_reference, status, key_1, key_2, company):
    conn, cursor = open_connection(config.database_name)
    for i in range(len(date)):
        check_existence = f"SELECT * FROM {config.payment_trans_table} WHERE key_1='{key_1[i]}' " \
                          f"and company='{company}'"
        result = cursor.execute(check_existence).fetchall()
        if len(result) == 0:
            query = f"INSERT INTO {config.payment_trans_table} (date, date_created, order_id, " \
                    f"payment_amount, payment_type, payment_reference, status, key_1, key_2, company)" \
                    f"VALUES ('{date[i].date()}', '{date_created}', '{order_id[i]}', '{payment_amount[i]}', " \
                    f"'{payment_type}', '{payment_reference[i]}', '{status[i]}', '{key_1[i]}', '{key_2[i]}', " \
                    f"'{company}')"
            cursor.execute(query)
    close_connection(conn, cursor)
def get_daily_payment_trans(date, company):
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT * FROM {config.payment_trans_table} WHERE date='{date}' and company='{company}'"
    result = cursor.execute(query).fetchall()
    close_connection(conn, cursor)
    return result

def create_payment_trans_temp_table(table_name):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f'CREATE TABLE {table_name} ' \
                f'(id integer, date date, date_created date, ' \
                f'order_id varchar, payment_amount double, payment_type varchar, ' \
                f'payment_reference varchar, status int, key_1 varchar, key_2 varchar)'
        cursor.execute(query)
    except:
        pass
def create_choco_temp_table(table_name):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f'CREATE TABLE {table_name} ' \
                f'(date date, date_created date, ' \
                f'order_id varchar, payment_amount double, payment_type varchar, ' \
                f'payment_reference varchar, status int, key_1 varchar, key_2 varchar)'
        cursor.execute(query)
    except:
        pass

def update_payment_trans_temp_table(table_name, data):
    conn, cursor = open_connection(config.database_name)
    for i in range(len(data)):
        id = data[i][0]
        date = data[i][1]
        date_created = data[i][2]
        order_id = data[i][3]
        payment_amount = data[i][4]
        payment_type = data[i][5]
        payment_reference = data[i][6]
        status = data[i][7]
        key_1 = data[i][8]
        key_2 = data[i][9]
        check_existence = f"SELECT * FROM {table_name} WHERE key_1='{key_1}'"
        result = cursor.execute(check_existence).fetchall()
        if len(result) == 0:
            query = f"INSERT INTO {table_name} (id, date, date_created, order_id, " \
                    f"payment_amount, payment_type, payment_reference, status, key_1, key_2) " \
                    f"VALUES ('{id}', '{date}', '{date_created}', '{order_id}', '{payment_amount}', " \
                    f"'{payment_type}', '{payment_reference}', '{status}', '{key_1}', '{key_2}')"
            cursor.execute(query)
    close_connection(conn, cursor)
def update_choco_temp_table(table_name, date, date_created, order_id, payment_amount,
                            payment_type, payment_reference, status, key_1, key_2):
    conn, cursor = open_connection(config.database_name)
    for i in range(len(date)):
        check_existence = f"SELECT * FROM {table_name} WHERE key_1='{key_1[i]}'"
        result = cursor.execute(check_existence).fetchall()
        if len(result) == 0:
            query = f"INSERT INTO {table_name} (date, date_created, order_id, " \
                    f"payment_amount, payment_type, payment_reference, status, key_1, key_2) " \
                    f"VALUES ('{date[i]}', '{date_created[i]}', '{order_id[i]}', '{payment_amount[i]}', " \
                    f"'{payment_type[i]}', '{payment_reference[i]}', '{status[i]}', '{key_1[i]}', '{key_2[i]}')"
            cursor.execute(query)
    close_connection(conn, cursor)

def create_error_temp_table(table_name):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {table_name} " \
                f"(id int, date date, date_created date, order_id varchar, payment_amount double, " \
                f"payment_type varchar, payment_reference varchar, status int, key_1 varchar, " \
                f"key_2 varchar, difference double)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)

def get_first_second_errors(A_name, B_name):
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT A.* FROM {A_name} A LEFT JOIN {B_name} B " \
            f"ON A.key_1=B.key_1 WHERE B.key_1 IS NULL"
    result = cursor.execute(query).fetchall()
    return result
def get_third_error(A_name, B_name):
    conn, cursor = open_connection(config.database_name)
    query_payment = f"SELECT A.* FROM {A_name} A LEFT JOIN {B_name} B ON A.key_2=B.key_2 WHERE B.key_2 IS NOT NULL"
    query_choco = f"SELECT B.* FROM {A_name} A LEFT JOIN {B_name} B ON A.key_2=B.key_2 WHERE B.key_2 IS NOT NULL"
    result_payment = cursor.execute(query_payment).fetchall()
    result_choco = cursor.execute(query_choco).fetchall()
    keys = list()
    for i in result_payment:
        keys.append(i[9])
    return result_payment, result_choco, keys
def get_full_table(table_name):
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT * FROM {table_name}"
    result = cursor.execute(query).fetchall()
    return result


def update_first_error_temp_table(table_name, data):
    conn, cursor = open_connection(config.database_name)
    for i in range(len(data)):
        id = data[i][0]
        date = data[i][1]
        date_created = data[i][2]
        order_id = data[i][3]
        payment_amount = data[i][4]
        payment_type = data[i][5]
        payment_reference = data[i][6]
        status = data[i][7]
        key_1 = data[i][8]
        key_2 = data[i][9]
        query = f"INSERT INTO {table_name} (id, date, date_created, order_id, payment_amount, " \
                f"payment_type, payment_reference, status, key_1, key_2, difference) " \
                f"VALUES ('{id}', '{date}', '{date_created}', '{order_id}', '{payment_amount}', " \
                f"'{payment_type}', '{payment_reference}', '{status}', '{key_1}', '{key_2}', '0')"
        cursor.execute(query)
    close_connection(conn, cursor)
def update_second_error_temp_table(table_name, data):
    conn, cursor = open_connection(config.database_name)
    for i in range(len(data)):
        date = data[i][0]
        date_created = data[i][1]
        order_id = data[i][2]
        payment_amount = data[i][3]
        payment_type = data[i][4]
        payment_reference = data[i][5]
        status = data[i][6]
        key_1 = data[i][7]
        key_2 = data[i][8]
        query = f"INSERT INTO {table_name} (date, date_created, order_id, payment_amount, " \
                f"payment_type, payment_reference, status, key_1, key_2, difference) " \
                f"VALUES ('{date}', '{date_created}', '{order_id}', '{payment_amount}', " \
                f"'{payment_type}', '{payment_reference}', '{status}', '{key_1}', '{key_2}', '0')"
        cursor.execute(query)
    close_connection(conn, cursor)
def clear_error_table_by_keys(table_name, keys):
    conn, cursor = open_connection(config.database_name)
    for key in keys:
        try:
            query = f"DELETE FROM {table_name} WHERE key_2='{key}'"
            cursor.execute(query)
        except:
            pass
    close_connection(conn, cursor)
def update_third_error_temp_tablle(table_name, payment, choco):
    conn, cursor = open_connection(config.database_name)
    for i in range(len(payment)):
        id = payment[i][0]
        date = choco[i][1]
        date_created = choco[i][2]
        order_id = choco[i][3]
        payment_amount = choco[i][4]
        payment_type = choco[i][5]
        payment_reference = choco[i][6]
        status = choco[i][7]
        key_1 = payment[i][8]
        key_2 = payment[i][9]
        difference = float(payment_amount) - float(payment[i][4])
        query = f"INSERT INTO {table_name} (id, date, date_created, order_id, payment_amount, " \
                f"payment_type, payment_reference, status, key_1, key_2, difference) " \
                f"VALUES ('{id}', '{date}', '{date_created}', '{order_id}', '{payment_amount}', " \
                f"'{payment_type}', '{payment_reference}', '{status}', '{key_1}', '{key_2}', '{difference}')"
        cursor.execute(query)
    close_connection(conn, cursor)


def are_lists_equal(first, second):
    a = list()
    b = list()
    for i in first:
        temp_list = list()
        for j in i:
            temp_list.append(str(j))
        a.append(temp_list)
    for i in second:
        temp_list = list()
        for j in i:
            temp_list.append(str(j))
        b.append(temp_list)
    a.sort()
    b.sort()
    return a == b

def create_daily_analysis_table(table_name):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {table_name} " \
                f"(primary_id integer PRIMARY KEY AUTOINCREMENT NOT NULL, id int, " \
                f"date date, date_created date, order_id varchar, payment_amount double, " \
                f"payment_type varchar, payment_reference varchar, status int, " \
                f"key_1 varchar, key_2 varchar, error_type int, difference double, queue int, " \
                f"date_analysed date)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def update_daily_analysis_table(table_name, data, date_analysed):
    conn, cursor = open_connection(config.database_name)
    flag = False
    check_rows = f"SELECT * FROM {table_name}"
    result = cursor.execute(check_rows).fetchall()
    if len(result) == 0:
        queue = 1
        flag = True
    else:
        old_queue = result[-1][13]
        query = f"SELECT id, date, date_created, order_id, payment_amount, " \
                f"payment_type, payment_reference, status, key_1, key_2, difference, error_type " \
                f"FROM {table_name} WHERE queue='{old_queue}'"
        old_table = list(cursor.execute(query).fetchall())
        if not are_lists_equal(old_table, data):
            flag = True
            queue = int(old_queue) + 1
    if flag:
        print(table_name, "updating queue:", queue)
        for trans in data:
            id = trans[0]
            date = trans[1]
            date_created = trans[2]
            order_id = trans[3]
            payment_amount = trans[4]
            payment_type = trans[5]
            payment_reference = trans[6]
            status = trans[7]
            key_1 = trans[8]
            key_2 = trans[9]
            difference = trans[10]
            error_type = trans[11]
            query = f"INSERT INTO {table_name} " \
                    f"(id, date, date_created, order_id, payment_amount, payment_type, " \
                    f"payment_reference, status, key_1, key_2, error_type, difference, queue, date_analysed) " \
                    f"VALUES ('{id}', '{date}', '{date_created}', '{order_id}', '{payment_amount}', " \
                    f"'{payment_type}', '{payment_reference}', '{status}', '{key_1}', '{key_2}', " \
                    f"'{error_type}', '{difference}', '{queue}', '{date_analysed}')"
            cursor.execute(query)
    else:
        print(table_name, ": don't need to update")
    close_connection(conn, cursor)
def get_latest_queue(table_name):
    conn, cursor = open_connection(config.database_name)
    latest_queue_query = f"SELECT queue FROM {table_name}"
    result = cursor.execute(latest_queue_query).fetchall()
    queue = int(result[-1][-1])
    close_connection(conn, cursor)
    return queue
def get_daily_analysis_table(table_name, payment_systems, latest=True, queue=1):
    conn, cursor = open_connection(config.database_name)
    if latest:
        latest_queue_query = f"SELECT queue FROM {table_name}"
        result = cursor.execute(latest_queue_query).fetchall()
        queue = int(result[-1][13])
    total = list()
    for payment_system in payment_systems:
        query = f"SELECT * FROM {table_name} WHERE queue='{queue}' and payment_type='{payment_system}'"
        result = cursor.execute(query).fetchall()
        total += result
    close_connection(conn, cursor)
    return total


def get_trans_by_key_value(table_name, key, value):
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT * FROM {table_name} WHERE {str(key)}='{value}'"
    result = cursor.execute(query).fetchall()
    return result

def create_report_table(table_name):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {table_name} " \
                f"(primary_id integer PRIMARY KEY AUTOINCREMENT NOT NULL, id int, " \
                f"date date, date_created date, order_id varchar, payment_amount double, " \
                f"payment_type varchar, payment_reference varchar, status int, " \
                f"key_1 varchar, key_2 varchar, error_type int, difference double, date_analysed date)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def update_report_table(table_name, data):
    conn, cursor = open_connection(config.database_name)
    for trans in data:
        id = trans[1]
        date = trans[2]
        date_created = trans[3]
        order_id = trans[4]
        payment_amount = trans[5]
        payment_type = trans[6]
        payment_reference = trans[7]
        status = trans[8]
        key_1 = trans[9]
        key_2 = trans[10]
        error_type = trans[11]
        difference = trans[12]
        date_analysed = trans[14]
        query = f"INSERT INTO {table_name} " \
                f"(id, date, date_created, order_id, payment_amount, payment_type, " \
                f"payment_reference, status, key_1, key_2, error_type, difference, date_analysed) " \
                f"VALUES ('{id}', '{date}', '{date_created}', '{order_id}', '{payment_amount}', " \
                f"'{payment_type}', '{payment_reference}', '{status}', '{key_1}', '{key_2}', " \
                f"'{error_type}', '{difference}', '{date_analysed}')"
        cursor.execute(query)
    close_connection(conn, cursor)


def create_log_table():
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {config.log_table} " \
                f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, " \
                f"date date, company varchar, log varchar)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def get_log_by_date(date, company):
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT log FROM {config.log_table} where date='{date}' and company='{company}'"
    result = cursor.execute(query).fetchall()
    close_connection(conn, cursor)
    return result
def update_log_table(date, company, log):
    conn, cursor = open_connection(config.database_name)
    # checking existence of log for particular date
    check_date = f"SELECT * FROM {config.log_table} WHERE date='{date}' and company='{company}'"
    result = cursor.execute(check_date).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {config.log_table} (date, company, log) VALUES ('{date}', '{company}', '{log}')"
    else:
        query = f"UPDATE {config.log_table} SET log='{log}' WHERE date='{date}' and company='{company}'"
    cursor.execute(query)
    close_connection(conn, cursor)

def export_to_excel(table_name):
    first_error_fields = 'date, date_created, order_id, payment_amount, payment_type, ' \
                     'payment_reference, status'
    second_error_fields = 'date, date_created, order_id, payment_amount, payment_type, ' \
                         'payment_reference, status'
    third_error_fields = 'date, date_created, order_id, payment_amount, payment_type, ' \
                         'payment_reference, status, difference'
    conn, cursor = open_connection(config.database_name)
    query1 = f"SELECT {first_error_fields} FROM {table_name} WHERE error_type==1"
    query2 = f"SELECT {second_error_fields} FROM {table_name} WHERE error_type==2"
    query3 = f"SELECT {third_error_fields} FROM {table_name} WHERE error_type==3"
    # Saving SQL table to Dataframes
    df1 = pandas.read_sql_query(query1, conn)
    df2 = pandas.read_sql_query(query2, conn)
    df3 = pandas.read_sql_query(query3, conn)
    # Saving dfs to different sheets
    file_name = table_name + '.xlsx'
    file_path = config.reports_dir + '/' + file_name
    writer = pandas.ExcelWriter(file_path, engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Ошибка №1')
    df2.to_excel(writer, sheet_name='Ошибка №2')
    df3.to_excel(writer, sheet_name='Ошибка №3')
    writer.save()
    close_connection(conn, cursor)
    return file_name

def get_mix_max_date():
    conn, cursor = open_connection(config.database_name)
    min_query = f"SELECT MIN(date) FROM {config.payment_trans_table}"
    max_query = f"SELECT MAX(date) FROM {config.payment_trans_table}"
    min_date = cursor.execute(min_query).fetchall()
    max_date = cursor.execute(max_query).fetchall()
    return min_date[0][0], max_date[0][0]

def get_report_table_rows(table_name):
    conn = sqlite3.connect(config.database_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def create_working_table():
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {config.working_table} " \
                f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, " \
                f"login varchar, current_stage int, max_stage int, working_table_name varchar)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def update_working_table(login, current_stage, max_stage, working_table_name):
    conn, cursor = open_connection(config.database_name)
    check_existence = f"SELECT * FROM {config.working_table} WHERE login='{login}'"
    result = cursor.execute(check_existence).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {config.working_table} (login, current_stage, max_stage, working_table_name) " \
                f"VALUES ('{login}', '{current_stage}', '{max_stage}', '{working_table_name}')"
    else:
        query = f"UPDATE {config.working_table} " \
                f"SET current_stage='{current_stage}', max_stage='{max_stage}', " \
                f"working_table_name='{working_table_name}' WHERE login='{login}'"
    cursor.execute(query)
    close_connection(conn, cursor)
def get_working_table(login):
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"SELECT current_stage, max_stage, working_table_name " \
                f"FROM {config.working_table} WHERE login='{login}'"
        result = cursor.execute(query).fetchall()
        result = result[0]
        close_connection(conn, cursor)
        return result[0], result[1], result[2]
    except:
        return 0, 0

def create_users_table():
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {config.users_table} " \
                f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, " \
                f"login varchar, password varchar, role varchar)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def add_user(login, password, role):
    conn, cursor = open_connection(config.database_name)
    check_existence = f"SELECT * FROM {config.users_table} WHERE login='{login}'"
    result = cursor.execute(check_existence).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {config.users_table} (login, password, role) " \
                f"VALUES ('{login}', '{password}', '{role}')"
        cursor.execute(query)
    close_connection(conn, cursor)
def check_user(login, password):
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT password FROM {config.users_table} WHERE login='{login}'"
    result = cursor.execute(query).fetchall()
    close_connection(conn, cursor)
    if result:
        if result[0][0] == password and password != '':
            return True
    return False




def create_daily_tables_table():
    conn, cursor = open_connection(config.database_name)
    try:
        query = f"CREATE TABLE {config.daily_tables_table} " \
                f"(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, date date, company varchar)"
        cursor.execute(query)
    except:
        pass
    close_connection(conn, cursor)
def update_daily_tables_table(date, company):
    conn, cursor = open_connection(config.database_name)
    check_existence = f"SELECT * FROM {config.daily_tables_table} WHERE date='{date}' " \
                      f"and company='{company}'"
    result = cursor.execute(check_existence).fetchall()
    if len(result) == 0:
        query = f"INSERT INTO {config.daily_tables_table} (date, company) VALUES ('{date}', '{company}')"
        cursor.execute(query)
    close_connection(conn, cursor)
def get_daily_tables():
    conn, cursor = open_connection(config.database_name)
    query = f"SELECT date FROM {config.daily_tables_table}"
    result = cursor.execute(query).fetchall()
    return result

create_messages_table()
create_payment_trans_table()
create_log_table()
create_working_table()
create_daily_tables_table()
################################
create_companies_table()
update_companies_table('chocotravel', 'chococasetest@gmail.com', 'kanatakbayev')
update_companies_table('chocolife', 'salambayev.choco@gmail.com', 'S31Amchina')
################################
create_users_table()
add_user('1', '1', 'appointee')
add_user('2', '2', 'executor')
add_user('3', '3', 'executor')


if not os.path.exists(config.attachment_dir):
    os.makedirs(config.attachment_dir)

if not os.path.exists(config.reports_dir):
    os.makedirs(config.reports_dir)

if not os.path.exists(config.json_dir):
    os.makedirs(config.json_dir)