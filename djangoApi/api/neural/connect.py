"""
Пока что данный файл находится в проекте в ненужном месте.
Предполагалось, что данная папка будет в корневом каталоге,
но python ваш хваленый не хочет ее находить. Поэтому файл пока что здесь
пока я не разберусь с данной проблемой.
"""


def tokenize(content: str) -> list[str]:
    """
    Пример работы токенизатора. Backend будет использовать данную функцию,
    чтобы получать слова из текста запроса пользователя.
    Пишите все что хотите, но бэк будет взаимодействовать только с этой функцией.

    :param content: Текст запроса.
    :return: Токенизированная строка.
    """
    return list(content.split(' '))


def classify(tokenized_str: list[str]) -> (str, str):
    """
    Здесь должен работать ваш классификатор.
    Back будет использовать данную функцию.
    :param tokenized_str: Токенизированная строка.
    :return: Первый str - название файла, второй - заголовок.
    """
    return 'HelloWorld.txt', 'Relaxing'


def transformer(request: str, answers: list[str]) -> str:
    """

    :param answers: Предполагаемые ответы.
    :return: Самый релевантный ответ.
    """

    return answers[0]


if __name__ == '__main__':
    data = tokenize("У меня сломался роутер. Не знаю что делать.")
    for word in data:
        print(word, end='/')
    print()

    scope_id = classify(data)
    print(f"Айди сферы вопросов в базе данных: {scope_id}.")
