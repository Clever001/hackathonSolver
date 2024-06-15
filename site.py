import asyncio
import requests
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import defer_call, info as session_info, run_async, run_js

chat_msgs = []
online_users = set()

MAX_MESSAGES_COUNT = 100

async def main():
    global chat_msgs

    put_markdown("## Задавайте свой вопрос!")

    msg_box = output()
    put_scrollable(msg_box, height=600, keep_bottom=True)

    nickname = "Вы"

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    msg_box.append(put_markdown(
        "Добрый день, пользователь. Напишите свой вопрос, а мы сделаем всё возможное, чтобы дать на него ответ."))

    while True:
        data = await input_group("💭 Новое сообщение", [input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить"])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        chat_msgs.append((nickname, data['msg']))


        try:
            response = requests.get('http://127.0.0.1:8000/api/v1/ask_question/', data={'message': data['msg']})
            chat_msgs.append(('Чат поддержки', response.text[11:-2]))
        except:
            msg_box.append(put_markdown(f"Нет связи с ботом."))
    refresh_task.close()
    print(data['msg'])
    online_users.remove(nickname)


async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        # remove expired
        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)


if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)
