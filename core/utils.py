import argparse
import os
import sys


def add_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Путь до каталога/файла который будет загружен."
    )
    parser.add_argument(
        "--action",
        type=str,
        required=True,
        help="Действие которое нужно сделать с файлом(upload, delete)."
    )

    namespace = parser.parse_args()
    return namespace


def get_files(path) -> str:
    for file in os.listdir(path):
        _file = os.path.join(path, file)
        if os.path.isfile(_file):
            yield _file


def check_file(path) -> list[str]:
    result = []
    try:
        with open(path, 'rb') as f:
            result.append(f.name)
    except FileNotFoundError as e:
        sys.stdout.write(f"{path} - такого файла не найдено.\nошибка: {e}\n")
    except IsADirectoryError:
        for file in get_files(path):
            with open(file, 'rb') as f:
                result.append(f.name)
    return result
