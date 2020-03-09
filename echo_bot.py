# --------utf-8-----------

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import logging

try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

log = logging.getLogger('bot')


def configure_log():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))

    file_handler = logging.FileHandler("bot.log", 'a', 'utf-8', False)
    file_handler.setFormatter(logging.Formatter(datefmt='%Y-%m-%d %H:%M',
                                                fmt='%(asctime)s %(levelname)s %(message)s'))

    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)


class Bot:
    """"
    Echo bot для vk.com

    Use python3.7
    """

    def __init__(self, group_id, token):
        """

        :param group_id: group id из группы vk.com
        :param token: секретный токен
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """Запуск бота"""
        for event in self.long_poll.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """Отправляет сообщение назад, если это текст
        :param event: VkBotMessageEvent
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('Отправляем сообщение назад')
            self.api.messages.send(message=("Возвращаю строку: " + event.object.text),
                                   random_id=random.randint(0, 2 ** 20),
                                   peer_id=event.object.peer_id)
        else:
            log.info("не знаю событий такого типа %s", event.type)


if __name__ == '__main__':
    configure_log()
    bot = Bot(GROUP_ID, TOKEN)
    bot.run()
