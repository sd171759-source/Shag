import requests
import json
import os
from CSV import save_steps, sum_steps_days, avg_steps_days
from dotenv import load_dotenv
from time import sleep
load_dotenv()

telegram_token = os.getenv("key").strip()
URL = f"https://api.telegram.org/bot{telegram_token}/"

def reply(chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text
    }
    requests.get(f"{URL}sendMessage", params=params)

def get_updates(offset=None):
    params = {}
    if offset:
        params["offset"] = offset
    return requests.get(f"{URL}getUpdates", params=params).json()

def main():
    last_update_id = None

    while True:
        try:
            updates = get_updates(last_update_id)
            result = updates.get("result", [])
            if not result:
                sleep(1)
                continue

            update = result[-1]
            last_update_id = update["update_id"] + 1


            message = update.get("message")
            if message:
                chat_id = message["chat"]["id"]
                user_id = message["from"]["id"]
                text = message.get("text", "").strip()

                if text.isdigit():
                    steps = int(text)
                    if steps >= 0:
                        save_steps(user_id, steps)
                        reply(chat_id, f" Записано: {steps:,} шагов!")
                    else:
                        reply(chat_id, " Шаги должны быть положительными")
                else:

                    buttons = {
                        "inline_keyboard": [

                            [{"text": "Ср. за неделю", "callback_data": f"avg7_{user_id}"}],
                            [{"text": "Ср. за месяц", "callback_data": f"avg30_{user_id}"}],
                            [{"text": "Ср. за квартал", "callback_data": f"avg90_{user_id}"}]
                        ]
                    }
                    params = {
                        "chat_id": chat_id,
                        "text": "Привет, выбери статистику или напишите число шагов:",
                        "reply_markup": json.dumps(buttons)
                    }
                    requests.get(f"{URL}sendMessage", params=params)


            callback = update.get("callback_query")
            if callback:
                chat_id = callback["message"]["chat"]["id"]
                data = callback["data"]
                user_id = callback["from"]["id"]


                if data.startswith("avg7_"):
                    avg = avg_steps_days(user_id, 7)
                    reply(chat_id, f" Среднее за неделю: {avg:,.0f} шагов/день")
                elif data.startswith("avg30_"):
                    avg = avg_steps_days(user_id, 30)
                    reply(chat_id, f" Среднее за месяц: {avg:,.0f} шагов/день")
                elif data.startswith("avg90_"):
                    avg = avg_steps_days(user_id, 90)
                    reply(chat_id, f" Среднее за квартал: {avg:,.0f} шагов/день")


                requests.get(f"{URL}answerCallbackQuery", params={"callback_query_id": callback["id"]})

        except Exception as e:
            print(f"Ошибка: {e}")
            sleep(1)
main()
