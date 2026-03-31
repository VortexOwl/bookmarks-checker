# ----------------------------------------------------------------------------#
# Embedded libraries                                                          #
# ----------------------------------------------------------------------------#
from datetime import timedelta, datetime
from os import mkdir, listdir
from os.path import isdir, getsize
from re import search

# ----------------------------------------------------------------------------#
# Project modules                                                             #
# ----------------------------------------------------------------------------#
from src.logs.config import is_clear_logs


def creating_necessary_folders(path:str) -> None:
    if not isdir(s=path):
        mkdir(path=path)


def read_file_line_by_line(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()


def clearing_logs() -> None:
    if is_clear_logs:
        is_write_lines_in_file = False
        keywords = {'INFO', 'DEBUG', 'WARNING', 'ERROR', 'FATAL'}
        last_date = datetime.now()
        last_date_log = last_date
        print('Введите названия файлов журналов через пробел для их очистки.')
        file_names = input().split(' ')
        if isdir(s='logs'):
            log_files = listdir(path='logs')
            for file_name in file_names:
                file_name = search(pattern=r'(?:.*/)?([^./]+)', string=file_name)
                if file_name in ['info', 'debug', 'error', 'warning', 'fatal']:
                    file_name = f'logs_{file_name}'
                if file_name in log_files:
                    if getsize(f'logs/{file_name}.log') / 1048576 > 1024:
                        print(f'Начата очистка файла {file_name}.log от данных месячной давности.с')
                        with open(f'logs/{file_name}.log', 'w') as file_logs:
                            for read_line in read_file_line_by_line(file_path=f'logs/{file_name}.log'):
                                if is_write_lines_in_file:
                                    file_logs.write(read_line)
                                else:
                                    if any(log_name in read_line for log_name in keywords):
                                        last_date_log = datetime.strptime(read_line.split(' |')[0], '%Y-%m-%d %H:%M:%S')
                                        if last_date - last_date_log <= timedelta(days=30):
                                            file_logs.write(read_line)
                                            is_write_lines_in_file = True
