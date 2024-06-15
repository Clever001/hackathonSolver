"""
Пока что данный файл находится в проекте в ненужном месте.
Предполагалось, что данная папка будет в корневом каталоге,
но python ваш хваленый не хочет ее находить. Поэтому файл пока что здесь
пока я не разберусь с данной проблемой.
"""

import numpy as np
import pandas as pd
import os


def Embed(texts: pd.DataFrame) -> np.ndarray:
    return np.array([[1, 2, 3], [4, 5, 6]])


def Classify(embedding: np.ndarray, docs: pd.DataFrame, query: str) -> str:
    return "В одном маленьком городке, окруженном густыми лесами и высокими горами, жила девочка по имени Лиза. Она была известна своей любознательностью и любовью к приключениям. Каждый день Лиза отправлялась в лес, чтобы исследовать его тайны. Однажды, гуляя по лесной тропинке, она наткнулась на старую карту, спрятанную под корнями огромного дуба. На карте был изображен путь к загадочному сокровищу, спрятанному глубоко в горах. Лиза решила следовать указаниям карты и отправилась в увлекательное путешествие. Преодолевая трудности и встречая новых друзей, она наконец нашла сокровище. Но самым ценным оказалось не золото и драгоценности, а опыт и воспоминания, которые она приобрела в этом удивительном приключении."


def Transform(query: str) -> str:
    return "My short favorite answer."


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


def read_xlsx_files(file_paths):
    data = {
        "name": [],
        "content": []
    }

    for file_path in file_paths:
        df = pd.read_excel(file_path, usecols=[0], header=None)
        file_name = os.path.basename(file_path)
        for content in df.iloc[:, 0]:
            data["name"].append(file_name)
            data["content"].append(content)
    result_df = pd.DataFrame(data)
    return result_df


if __name__ == '__main__':
    directory = r'D:\download\dataset\Система технической поддержки\xlsx'
    file_paths = get_file_paths(directory)
    result_df = read_xlsx_files(file_paths)
    print(result_df)
