from os import mkdir
from os.path import getsize, isdir
from sys import exit
from logging import basicConfig, getLogger, Formatter, FileHandler, StreamHandler, INFO, DEBUG, WARNING, ERROR, FATAL
from traceback import extract_stack
from datetime import timedelta, datetime

from config import is_file_info, is_file_debug, is_file_warning, is_file_error, is_file_fatal, is_clear_logs


def clearing_logs(name_file:str) -> None:
    if getsize(f'logs/{name_file}.log') / 1048576 > 1024:
        debug(f'Начата очистка файла {name_file}.log от данных месячной давности')
        with open(f'logs/{name_file}.log', 'r') as file_logs:
            lines = file_logs.readlines()
        with open(f'logs/{name_file}.log', 'w') as file_logs:
            last_date = datetime.now()
            last_date_log = last_date
            for line in lines:
                if line.find('INFO') != -1 or line.find('DEBUG') != -1 or line.find('WARNING') != -1 or line.find(
                        'ERROR') != -1 or line.find('FATAL') != -1:
                    date = datetime.strptime(line.split(' |')[0], '%Y-%m-%d %H:%M:%S')
                    last_date_log = date
                    if last_date - date <= timedelta(days=30):
                        file_logs.write(line)
                else:
                    if last_date - last_date_log <= timedelta(days=30):
                        file_logs.write(line)


def log_info(line:str) -> None:
    line = 'Module: ' + extract_stack(limit=2)[0].filename.split('/')[-1] + ' | Func: ' + extract_stack(limit=2)[0].name + ' | Line: ' + str(extract_stack(limit=2)[0].lineno) + ' | Message: ' + str(line)
    logger.info(line)
    if is_file_info:
        logger_info.info(line)
    

def log_debug(line:str) -> None:
    line = 'Module: ' + extract_stack(limit=2)[0].filename.split('/')[-1] + ' | Func: ' + extract_stack(limit=2)[0].name + ' | Line: ' + str(extract_stack(limit=2)[0].lineno) + ' | Message: ' + str(line)
    logger.debug(line)
    if is_file_debug:
        logger_debug.debug(line)    
    

def log_warning(line:str) -> None:
    line = 'Module: ' + extract_stack(limit=2)[0].filename.split('/')[-1] + ' | Func: ' + extract_stack(limit=2)[0].name + ' | Line: ' + str(extract_stack(limit=2)[0].lineno) + ' | Message: ' + str(line)
    logger.warning(line)
    if is_file_warning:
        logger_warning.warning(line)


def log_error(line:str) -> None:
    line = 'Module: ' + extract_stack(limit=2)[0].filename.split('/')[-1] + ' | Func: ' + extract_stack(limit=2)[0].name + ' | Line: ' + str(extract_stack(limit=2)[0].lineno) + ' | Message: ' + str(line)
    logger.error(line)
    if is_file_error:
        logger_error.error(line)


def log_fatal(line:str) -> None:
    line = 'Module: ' + extract_stack(limit=2)[0].filename.split('/')[-1] + ' | Func: ' + extract_stack(limit=2)[0].name + ' | Line: ' + str(extract_stack(limit=2)[0].lineno) + ' | Message: ' + str(line)
    logger.fatal(line)
    if is_file_fatal:
        logger_fatal.fatal(line)
    exit()


def set_global_variable() -> None:
    global logger, logger_info, logger_debug, logger_warning, logger_error, logger_fatal
    
    basicConfig(level=DEBUG)

    formatter = Formatter(fmt="{asctime} | {levelname} | {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S")

    logger = getLogger('basic')
    logger.propagate = False
    file_handler = FileHandler('logs/logs.log', mode='a', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)
    console_handler = StreamHandler()
    console_handler.setLevel(DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger_info = getLogger('info')
    logger_info.propagate = False
    file_handler = FileHandler('logs/logs_info.log', mode='a', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)
    logger_info.addHandler(file_handler)

    logger_debug = getLogger('debug')
    logger_debug.propagate = False
    file_handler = FileHandler('logs/logs_debug.log', mode='a', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)
    logger_debug.addHandler(file_handler)

    logger_warning = getLogger('warning')
    logger_warning.propagate = False
    file_handler = FileHandler('logs/logs_warning.log', mode='a', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)
    logger_warning.addHandler(file_handler)

    logger_error = getLogger('error')
    logger_error.propagate = False
    file_handler = FileHandler('logs/logs_error.log', mode='a', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)
    logger_error.addHandler(file_handler)

    logger_fatal = getLogger('fatal')
    logger_fatal.propagate = False
    file_handler = FileHandler('logs/logs_fatal.log', mode='a', encoding='utf-8')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)
    logger_fatal.addHandler(file_handler)


def creating_necessary_folders() -> None:
    if not isdir('logs'):
        mkdir('logs')
    if not isdir('docs'):
        mkdir('docs')
    if not isdir('src'):
        mkdir('src')


def start_logs() -> None:
    creating_necessary_folders()
    set_global_variable()
    if is_clear_logs:
        log_info('Введитие названия файлов журнала для их очистки через пробел')
        files_names = input().split(' ')
        if files_names[0] == '':
            files_names[0] = 'logs'
        for file_name in files_names:
            clearing_logs(name_file=file_name)


start_logs()
