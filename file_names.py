import config
import re

def kaspi_daily(file_name):
    file_name_regex = config.kaspi_daily_regex
    day, month, year = re.match(file_name_regex, file_name).groups()
    return year, month, day
def rps_daily(file_name):
    file_name_regex = config.rps_daily_regex
    year, month, day = re.match(file_name_regex, file_name).groups()
    return year, month, day
def processing_daily(file_name):
    file_name_regex = config.processing_daily_regex
    year, month, day = re.match(file_name_regex, file_name).groups()
    return year, month, day
def qazkom_interval(file_name):
    file_name_regex = config.qazkom_interval_regex
    from_day, from_month, from_year, to_day, to_month, to_year = re.match(file_name_regex, file_name).groups()
    return from_year, from_month, from_day, to_year, to_month, to_day

def set_file_name(file_name, payment_system):
    file_format = file_name[file_name.rfind('.')+1:]
    from_year = from_month = from_day = 'unknown'
    to_year, to_month, to_day = from_year, from_month, from_day
    payment_system_name = 'unknown'

    # kaspi_daily
    if payment_system is config.kaspi_key:
        from_year, from_month, from_day = kaspi_daily(file_name)
        to_year, to_month, to_day = from_year, from_month, from_day
        payment_system_name = config.kaspi_name
    # rps_daily
    if payment_system is config.rps_key:
        from_year, from_month, from_day = rps_daily(file_name)
        to_year, to_month, to_day = from_year, from_month, from_day
        payment_system_name = config.rps_name
    # processing_daily
    if payment_system is config.processing_key:
        from_year, from_month, from_day = processing_daily(file_name)
        to_year, to_month, to_day = from_year, from_month, from_day
        payment_system_name = config.processing_name
    # qazkom_interval
    if payment_system is config.qazkom_key:
        from_year, from_month, from_day, to_year, to_month, to_day = qazkom_interval(file_name)
        payment_system_name = config.qazkom_name

    new_file_name = '.'.join([from_year, from_month, from_day]) + '-' + \
                    '.'.join([to_year, to_month, to_day]) + '_' + payment_system_name + '.' \
                    + file_format
    return new_file_name

