import numpy
import os
import numpy as np
from numpy import ndarray
import pandas as pd
import pickle

from sentence_transformers import SentenceTransformer

from sklearn.metrics import DistanceMetric

# (полный список: https://www.sbert.net/docs/pretrained_models.html)
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L12-v2', device='cuda')


def classify(df: pd.DataFrame) -> ndarray:
    """
    Массив ответов обрабатывается моделью,
    формируя n-мерный массив с float-числами (эмбеддинг)
    :param df: Список строк (ответов).
    :return: N-мерный массив эмбеддинга.
    """

    # Cоздаем эмбеддинг
    embedding_arr = model.encode(df['content'])

    return embedding_arr


def query_search(query: str, embedding: ndarray, df: pd.DataFrame) -> str:
    """
    Находит ближайший ответ по текстовому запросу query.
    :param query: Текстовой запрос пользователя
    :param embedding: N-мерный массив с числами, заранее сгенерированный
    :param df: Список ответов (текстов)
    :return: Наиболее подходящую строку-ответ из texts
    """

    query_embedding = model.encode(query)

    # Определяем дистанции (метрически)
    dist = DistanceMetric.get_metric("euclidean")

    # Рассчитываем попарные дистанции между запросом и данными эмбеддинга
    dist_arr = dist.pairwise(embedding, query_embedding.reshape(1, -1)).flatten()
    # Сортируем результаты
    idist_arr_sorted = np.argsort(dist_arr)

    answer = df['content'].iloc[idist_arr_sorted[0]]

    print(1)
    return df["content"].iloc[idist_arr_sorted[0]]


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
        data["name"].extend([file_name for _ in df.values])
        data["content"].extend(df.iloc[:, 0].astype(str))
    result_df = pd.DataFrame(data)
    return result_df


if __name__ == '__main__':
    file_paths = get_file_paths(r'D:\Other\Scripts\Tokenizer\datatsets')

    df = read_xlsx_files(file_paths)
    #print(df.to_dict())
    #texts = [i[0] for i in df.values.tolist()]
    embedding = classify(df)
    #with open('data.pkl', 'rb') as file:
    #    embedding = pickle.load(file)

    query = """Контакты для связи: XXXXXXXXXXX Добрый день. В ЕРПX необходимо провести корректировку по пяти СД ПТУ с ин. НДС за предыдущие периоды, убрать сумму НДС и отнести ее на счет затарт, то есть ПТУ должны быть без НДС. По проведенным ПТУ по с/ф также есть проводки по перекурсовке ин. НДС. Прошу уточнить, каким  документом провести данные исправления."""
    answer = query_search(query, embedding, df)
    names = [name for name in answer['name']]
    content = [content for content in answer['content']]

    for i in range(len(names)):
        print(names[i])
        print(content[i])
        print()

    with open('data.pkl', 'wb') as file:
        pickle.dump(embedding, file)