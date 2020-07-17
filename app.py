# -*- coding: utf-8 -*-
"""
:authors: MaksimFokht
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2020 MaksimFokht
"""

from flask import Flask, request
import bot_config
from BotController import BotController

BotVK4 = Flask(__name__)


@BotVK4.route('/', methods=['POST'])
def processing():
    """
    Метод обрабатывает маршруты c POST-запросом приходящие на сайт бота и далее парсит его
    для отправки запроса в контроллер.

    :return: Метод возвращает 'ok' или 'not ok' в api VK.
    """
    data = request.get_json(force=True, silent=True)
    if not data or 'type' not in data:
        return 'not ok'
    if data['type'] == 'confirmation':
        return bot_config.confirmation_token
    elif data['type'] == 'message_new':
        try:
            peer_id = data['object']['message']['peer_id']
            from_id = data['object']['message']['from_id']
            text = data['object']['message']['text']
            print("[DEBUG]: New message from " + str(from_id) + ": " + text + '\n ')
            controller = BotController(from_id, peer_id, text)
            controller.init()
        finally:
            return 'ok'
    else:
        return 'ok'


if __name__ == '__main__':
    BotVK4.run()
