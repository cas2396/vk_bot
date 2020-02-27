# --------utf-8-----------

from _token import token
import vk_api
import vk_api.bot_longpoll

group_id = 192423088


class Bot:

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=token)
        self.long_poll = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

    def run(self):
        pass


if __name__ == '__main__':
    bot = Bot(group_id, token)
    bot.run()
