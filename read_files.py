import pandas
import datetime
import os

import config
import database



def get_key_1(date, common_key, payment_amount, status):
    key = list()
    for i in range(len(date)):
        key_temp = '_'.join([str(date[i].date()), str(common_key[i]), str(float(payment_amount[i])), str(status[i])])
        key.append(key_temp)
    return key

def get_key_2(date, common_key, status):
    key = list()
    for i in range(len(date)):
        key_temp = '_'.join([str(date[i].date()), str(common_key[i]), str(status[i])])
        key.append(key_temp)
    return key


def read_kaspi(file_path):
    file = pandas.read_excel(file_path, skiprows=0, skipfooter=0)
    date = file['Дата транзакции']
    order_id = file['Номер бронирования']
    payment_amount_temp = file['Сумма']
    payment_type = config.kaspi_name
    payment_reference = file['Номер Транзакции']
    status = list()
    payment_amount = list()
    for payment_sum in payment_amount_temp:
        temp = float(payment_sum)
        payment_amount.append(abs(temp))
        if temp > 0:
            status.append(config.status_payment)
        else:
            status.append(config.status_refund)
    key_1 = get_key_1(date, order_id, payment_amount, status)
    key_2 = get_key_2(date, order_id, status)
    return date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2
def read_rps(file_path):
    file = pandas.read_excel(file_path, skiprows=1, skipfooter=1)
    date = file['Дата']
    order_id = file['Номер брони']
    payment_amount = file['Сумма платежа']
    payment_type = config.rps_name
    payment_reference = file['# Кассовой операции']
    status_temp = file['Код результата']
    status = list()
    succeed = list()
    for code in status_temp:
        if int(code) == 0:
            status.append(config.status_payment)
        else:
            status.append(config.status_refund)
        succeed.append('1')
    key_1 = get_key_1(date, order_id, payment_amount, status)
    key_2 = get_key_2(date, order_id, status)
    return date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2
def read_processing(file_path):
    file = pandas.read_excel(file_path, skiprows=4, skipfooter=0)
    date = file['AlmDate']
    order_id = file['Order ID']
    payment_amount = file['Tran_amoun']
    payment_type = config.processing_name
    payment_reference = file['RRN(Bank)']
    types = file['Type']
    succeed = file['Resp']
    for i in range(len(succeed)):
        if succeed[i] == 'Decline':
            payment_amount.at[i] = 0

    status = list()
    for type in types:
        if str(type) == 'A':
            status.append(config.status_payment)
        elif str(type) == 'F':
            status.append(config.status_refund)

    key_1 = get_key_1(date, order_id, payment_amount, status)
    key_2 = get_key_2(date, order_id, status)
    return date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2
def read_qazkom(file_path):
    file = pandas.read_html(file_path)
    # concatenate all the tables that contain needed information
    total_table = list()
    tables = file[4:]
    for table in tables:
        names = table.iloc[0].values.tolist()
        table = pandas.DataFrame.from_records(data=table.values[1:], columns=names)
        total_table.append(table)
    file = pandas.concat(total_table, ignore_index=True)
    date = file['Post Date']
    date = pandas.to_datetime(date)
    order_id = file['A Code']
    payment_amount_temp = file['Settl.Amount']
    payment_type = config.qazkom_name
    payment_reference = file['Ret Ref Number']
    status = list()
    succeed = list()
    payment_amount = list()
    for payment_sum in payment_amount_temp:
        temp = float(payment_sum)
        payment_amount.append(abs(temp))
        if temp > 0:
            status.append(config.status_payment)
        else:
            status.append(config.status_refund)
        succeed.append('1')
    key_1 = get_key_1(date, order_id, payment_amount, status)
    key_2 = get_key_2(date, order_id, status)
    return date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2


def files_into_database(file_names, company):
    for file_name in file_names:
        payment_type = ''
        file_path = os.path.join(config.attachment_dir, company, file_name)

        # kaspi
        if file_name.count(config.kaspi_name) != 0:
            date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2 = read_kaspi(file_path)
        # rps
        if file_name.count(config.rps_name) != 0:
            date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2 = read_rps(file_path)
        # processing
        if file_name.count(config.processing_name) != 0:
            date, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2 = read_processing(file_path)
        # qazkom
        if file_name.count(config.qazkom_name) != 0:
            date, order_id, payment_amount, payment_type, payment_reference, status, key_2, key_2 = read_qazkom(file_path)

        if payment_type:
            date_created = datetime.datetime.now()
            database.update_payment_trans_table(date, date_created, order_id, payment_amount,
                   payment_type, payment_reference, status, key_1, key_2, company)