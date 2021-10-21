import threading
import traceback

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from utils import VkUtils
from command_handler import CommandHandler
from user_pool import VkUsers


class VkGroupLongpoll(threading.Thread):
    def __init__(self, group_id, group_access_token, user_access_tokens, chat_config, db):
        super().__init__()
        self.group_id = group_id
        self.group_access_token = group_access_token
        self.user_acceess_tokens = user_access_tokens
        self.chat_config = chat_config

        self.command_handler = None
        self.group_longpoll = None
        self.group_api = None
        self.user_pool = None
        self.utils = None
        self.db = db

    def run(self):
        self.user_auth()
        self.group_auth()
        self.utils = VkUtils(self.group_api)
        self.command_handler = CommandHandler(self.group_api, self.user_pool, self.chat_config, self.utils, self.db)
        threading.Thread(target=self.group_lp, name='GroupLongpollThread').start()

    def user_auth(self):
        self.user_pool = VkUsers(self.user_acceess_tokens)
        self.user_pool.auth(first=True)

    def group_auth(self):
        vk_session = vk_api.VkApi(token=self.group_access_token, api_version='5.131')
        self.group_longpoll = VkBotLongPoll(vk_session, self.group_id)
        self.group_api = vk_session.get_api()

    def group_lp(self):
        while True:
            try:
                for event in self.group_longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        self.command_handler.parse_event(event)
                    elif event.type == VkBotEventType.MESSAGE_EVENT:
                        self.command_handler.parse_event(event)
            except Exception as err:
                traceback.print_exc()
                print(str(err) + '\n')
