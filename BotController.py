# -*- coding: utf-8 -*-
"""
:authors: MaksimFokht
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2020 MaksimFokht
"""

from BotModel import BotModel
from BotView import BotView


class BotController:
    """

    :param from_id: Поле с id получателя.
    :type from_id: int

    :param text: Поле с текстом, которое отправляет пользователь.
    :type text: str

    :param peer_id: Поле с id диалога, где бот и пользователь взаимодействуют.
    :type peer_id: int

    Класс представляет собой связь между пользователем и моделью.
    В нем описан список команд и их инициализация.
    Каждая команда пользователя - это создание нового экземпляра контроллера,
    в котором происходит выполнение валидации команды и передача выполнения методов представлению.
    """

    def __init__(self, from_id, peer_id, text):
        self.text = text
        self.from_id = from_id
        self.peer_id = peer_id
        self.command = ''
        self.args = ''
        self.model = BotModel(self.text, self.from_id)
        self.response = ''
        print('[DEBUG-CONTROLLER]: The controller is initialized with the following data: \n '
              '[DEBUG-CONTROLLER]: from_id - ' + str(self.from_id) + '\n '
              '[DEBUG-CONTROLLER]: peer_id - ' + str(self.peer_id) + '\n '
              '[DEBUG-CONTROLLER]: text - ' + self.text + '\n ')

    def commands(self, command, args):
        """

        :param command: Поле с командой.
        :type command: str

        :param args: Поле с аргументами к команде.
        :type args: str

        Метод содержит условный оператор, в котором проверяется соответсвтие введенной команды.

        :return: При совпадении возвращается результат выполнения методов в виде строки.
        """
        if command == '.test':
            return self.model.test()
        elif command == '.ca':
            return self.model.add_cmd(args)
        elif command == '.enable':
            return self.model.turn_on(args)
        elif command == '.disable':
            return self.model.turn_off(args)
        elif command == '.skip':
            return self.model.skipped(args, self.from_id)
        elif command == '.ci':
            return self.model.get_conversation_info()
        elif command == '.exam':
            return self.model.show_exam()
        elif command == '.ea':
            return self.model.add_exam(args, self.from_id)
        elif command == '.help':
            return self.model.show_help(self.from_id)

    def init(self):
        """
        Метод инициализации обработки текста, в который включена валидация отправленоого запроса и
        получение ответа для дальнейшей передачи в представление.
        """
        self.command, self.args = self.model.validation()[0], self.model.validation()[1]
        self.response = self.commands(self.command, str(self.args))
        view = BotView(self.response, self.peer_id)
        view.send_msg()
