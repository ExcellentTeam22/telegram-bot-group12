import math

import requests
from flask import Flask, Response, request

app = Flask(__name__)

TOKEN = '5717215788:AAF2l_7dHqQAXfKle1YS3HGWEAMBbSdsmGM'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://028b-82-80-173-170.eu.ngrok.io/message'.format(
    TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

command_history = {"prime": 0, "factorial": 0, "palindrome": 0, "sqrt": 0, "popular": 0}

GLOBAL_DICT = {}


def is_prime(number: int) -> bool:
    for i in range(2, number):
        if (number % i) == 0:
            return False
    return True


def is_sqrt(number: int) -> bool:
    sqrt = math.isqrt(number)
    if sqrt * sqrt == number:
        return True
    return False


def is_factorial(number: int) -> bool:
    i = 1
    while True:
        if number % i == 0:
            number //= i
        else:
            break
        i += 1
    if number == 1:
        return True
    else:
        return False


def is_palindrome(number: int) -> bool:
    temp = number
    rev = 0
    while number > 0:
        dig = number % 10
        rev = rev * 10 + dig
        number = number // 10
    if temp == rev:
        return True
    return False


def popular_number() -> int:
    popular = max(GLOBAL_DICT, key=GLOBAL_DICT.get)
    return popular


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/')
def main_page():
    return '<h1>Hello Michal!</h1>'


@app.route('/message', methods=["POST"])
def handle_message():
    chat = request.get_json()
    print(chat)
    chat_id = chat['message']['chat']['id']
    text = chat['message']['text']

    if text.startswith('hi') or text.startswith('hello'):
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                           .format(TOKEN, chat_id, "Hi! how are you doing?"))

    elif text.startswith('/prime'):
        command_history['prime'] += 1
        if is_prime(int(text.split()[1])):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The number is prime"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The number is not prime"))

    elif text.startswith('/sqrt'):
        command_history['sqrt'] += 1
        if is_sqrt(int(text.split()[1])):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The given number has a sqrt"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The given number does not have a sqrt"))

    elif text.startswith('/palindrome'):
        command_history['palindrome'] += 1
        if is_palindrome(int(text.split()[1])):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The given number is a palindrome"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The given number is not a palindrome"))

    elif text.startswith('/factorial'):
        command_history['factorial'] += 1
        if is_factorial(int(text.split()[1])):
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The given number is factorial"))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "The given number is not factorial"))

    elif text.startswith('/popular'):
        command_history['popular'] += 1
        max_searches = 0
        max_searched_command = ''
        for command in command_history:
            if command_history[command] > max_searches:
                max_searches = command_history[command]
                max_searched_command = command
        if max_searched_command != '':
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, max_searched_command))
        else:
            res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                               .format(TOKEN, chat_id, "No command was searched"))

    elif text.startswith('/'):
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                           .format(TOKEN, chat_id, "An unknown command!"))

    else:
        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                           .format(TOKEN, chat_id, "Got it"))
    return Response("success")


if __name__ == '__main__':
    app.run(port=5002)
