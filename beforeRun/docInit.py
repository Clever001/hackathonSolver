import os
import pandas as pd
import requests


def get_file_paths(directory, extension=".xlsx"):
    """
    Получает список всех файлов с заданным расширением в указанной директории.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_paths.append(os.path.join(root, file))
    return file_paths


def post_doc(name, content):
    url = 'http://127.0.0.1:8000/api/v1/docs/'

    data = {
        "name": name,
        "content": content
    }

    response = requests.post(url, json=data)

    if response.status_code != 201:
        print(f'ERROR: Failed to post document {name} with content {content}')
        return False
    return True


def init_doc(directory):
    # Получение списка всех файлов .xlsx в директории
    file_paths = get_file_paths(directory)

    for file_path in file_paths:
        # Считывание файла .xlsx
        df = pd.read_excel(file_path, usecols=[0], header=None)

        # Извлечение названия файла
        file_name = os.path.basename(file_path)

        # Отправка каждой строки первого столбца на сервер
        for content in df.iloc[:, 0]:
            if not post_doc(file_name, content):
                print(f'Failed to post content from file {file_name}')
            else:
                print(f'Successfully posted content from file {file_name}')


if __name__ == '__main__':
    directory = r'C:\Users\cakev\PycharmProjects\hackathonSolver\xlsx'
    init_doc(directory)
