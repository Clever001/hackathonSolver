from transformers import logging

logging.set_verbosity_warning()
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TextClassificationPipeline

def Bert(query: str) -> str:
    # Установка фиксированного seed
    def set_seed(seed):
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


    set_seed(42)  # Вы можете использовать любое значение seed

    # Загрузка токенизатора и модели для задачи классификации предложений на русском языке
    tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
    model = AutoModelForSequenceClassification.from_pretrained("cointegrated/rubert-tiny2")

    # Создание пайплайна для классификации предложений
    classification_pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)


    # Функция для выделения релевантных предложений
    def extract_relevant_sentences(text, threshold=0.5):
        sentences = text.split('. ')
        relevant_sentences = []

        for sentence in sentences:
            # Классификация предложения
            results = classification_pipeline(sentence)
            # Предполагаем, что релевантность - это вероятность положительной классификации
            score = results[0][1]['score']

            if score > threshold:
                relevant_sentences.append(sentence)

        return relevant_sentences


    text = query

    ans = []

    relevant_sentences = extract_relevant_sentences(text)
    print("Relevant sentences:")
    for sentence in relevant_sentences:
        ans += sentence
        ans += ' '
    # if relevant_sentences == []:
    #     # перевести на статистику
    #     ans += '\n'
    return ''.join(ans)


if __name__ == "__main__":
    print(Bert("Данный этап является подготовительным для создания документов по планированию работы ТС по заказам в информационной системе. На предприятиях отсутствует. На данном этапе производится заполнение справочника. Сценарии планирования Входящие документы: нет. Исходящие документы: нет. Справочник «Сценарии планирования» предназначен для задания разделения планирования по произвольному признаку. Например, деление на пессимистичное и оптимистичное планирование, а также для определения периодичности планирования (возможные значения: месяц, квартал, год). Справочник содержит перечень сценариев, в разрезе которых ведется планирование закупок и продаж."))
