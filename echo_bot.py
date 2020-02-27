# --------utf-8-----------

from _token import token
import vk_api
import vk_api.bot_longpoll
import random

group_id = 192423088


class Bot:

    def __init__(self, group_id_, token_):
        self.group_id = group_id_
        self.token = token_
        self.vk = vk_api.VkApi(token=token_)
        self.long_poll = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poll.listen():
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            print(event.object.text)
            self.api.messages.send(message=("Возвращаю строку: " + event.object.text),
                                   random_id=random.randint(0, 2 ** 20),
                                   peer_id=event.object.peer_id)
        else:
            print("не знаю событий такого типа", event.object.type)


if __name__ == '__main__':
    bot = Bot(group_id, token)
    bot.run()
