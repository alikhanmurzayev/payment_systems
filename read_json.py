import json
import pandas

import config
import read_files

def get_key_1(date, common_key, payment_amount, status):
    key = list()
    for i in range(len(date)):
        key_temp = '_'.join([str(date[i]), str(common_key[i]), str(payment_amount[i]), str(status[i])])
        key.append(key_temp)
    return key

def get_key_2(date, common_key, status):
    key = list()
    for i in range(len(date)):
        key_temp = '_'.join([str(date[i]), str(common_key[i]), str(status[i])])
        key.append(key_temp)
    return key


def get_payment_type(key):
    if key == config.kaspi_json_key:
        return config.kaspi_name
    if key == config.rps_json_key:
        return config.rps_name
    if key == config.processing_json_key:
        return config.processing_name
    if key == config.qazkom_json_key:
        return config.qazkom_name
    return 'unknown'

def read_api_response(json_object):
    date = list()
    date_created = list()
    order_id = list()
    payment_amount = list()
    payment_type = list()
    payment_reference = list()
    status = list()
    for trans in json_object:
        date_temp = trans['date_created']
        date_created.append(pandas.to_datetime(date_temp))
        date.append(date_created[-1].date())
        order_id.append(trans['order_id'])
        payment_amount.append(trans['payment_amount'])
        payment_type.append(get_payment_type(trans['payment_code']))
        payment_reference.append(trans['payment_reference'])
        status.append(trans['status'])
    key_1 = get_key_1(date, order_id, payment_amount, status)
    key_2 = get_key_2(date, order_id, status)
    return date, date_created, order_id, payment_amount, payment_type, payment_reference, status, key_1, key_2