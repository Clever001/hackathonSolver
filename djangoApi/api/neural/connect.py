"""
Пока что данный файл находится в проекте в ненужном месте.
Предполагалось, что данная папка будет в корневом каталоге,
но python ваш хваленый не хочет ее находить. Поэтому файл пока что здесь
пока я не разберусь с данной проблемой.
"""

import numpy as np
import pandas as pd


def Embed(texts: pd.DataFrame) -> np.ndarray:
    return np.array([[1, 2, 3], [4, 5, 6]])


def Classify(embedding: np.ndarray, docs: pd.DataFrame, query: str) -> str:
    return "My very large favorite answer."


def Transform(query: str) -> str:
    return "My short favorite answer."


if __name__ == '__main__':
    pass
