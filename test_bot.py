# --------utf-8-----------

from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from echo_bot import Bot
from vk_api.bot_longpoll import VkBotMessageEvent


class MyTestCase(TestCase):
    RAW_EVENT = {'type': 'message_new', 'object': 
        {'date': 1583740869, 'from_id': 395383914, 'id': 97, 'out': 0, 'peer_id': 395383914, 'text': 'и еще раз привет',
         'conversation_message_id': 96, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
         'is_hidden': False}, 'group_id': 192423088, 'event_id': 'c128ef521357768ebf7ad1c86b4b77f5c89fbfea'}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)

        send_mock = Mock()

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock

                bot.on_event(event)

        send_mock.assert_called_once_with(
            message=("Возвращаю строку: " + self.RAW_EVENT['object']['text']),
            random_id=ANY,
            peer_id=self.RAW_EVENT['object']['peer_id']
        )
