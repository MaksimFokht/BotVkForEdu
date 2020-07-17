from vk_api.utils import get_random_id
import vkbot_api


class BotView:
    """

    :param result: Поле с текстом, которое отправляет бот.
    :type result: str

    :param peer_id: Поле с id диалога, где бот и пользователь взаимодействуют.
    :type peer_id: int

    Данный класс предназначен для вывода результата пользователю после ввода команды.
    """

    def __init__(self, result, peer_id):
        self.result = result
        self.peer_id = peer_id
        print('[DEBUG-VIEW]: The view is initialized with the following data: \n '
              '[DEBUG-VIEW]: result - ' + self.result + '\n '
              '[DEBUG-VIEW]: peer_id - ' + str(self.peer_id) + '\n ')

    def send_msg(self):
        """
        Метод отправки сообщения пользователю.
        """
        vkbot_api.vk.messages.send(
            message=self.result,
            random_id=get_random_id(),
            peer_id=self.peer_id)
