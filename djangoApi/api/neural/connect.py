def tokenize(content: str) -> list[str]:
    """
    Пример работы токенизатора. Backend будет использовать данную функцию,
    чтобы получать слова из текста запроса пользователя.
    Пишите все что хотите, но бэк будет взаимодействовать только с этой функцией.

    :param content: Текст запроса.
    :return: Токенизированная строка.
    """
    return list(content.split(' '))


if __name__ == '__main__':
    data = tokenize("У меня сломался роутер. Не знаю что делать.")
    for word in data:
        print(word, end='/')
    print()
