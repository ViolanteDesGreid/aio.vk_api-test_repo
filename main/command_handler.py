from vk_api.bot_longpoll import VkBotEventType

import commands.registration
import commands.passport
import commands.passport_event


class CommandHandler:
    def __init__(self, group_api, user_api, chat_config, utils, db):
        self.group_api = group_api
        self.user_api = user_api

        self.chat_config = chat_config
        self.utils = utils
        self.db = db

    def _message_new(self, event):
        peer_id, text = event.message.peer_id, event.message.text if len(event.message.text) != 0 else None

        if text is not None:
            split_text = text.split()
            if split_text[0] in ['!registration', '!регистрация']:
                commands.registration.handle(event.message, self.db, self.group_api, self.user_api, self.chat_config)
            if split_text[0] in ['!passport', '!паспорт']:
                commands.passport.handle(event.message, self.utils)
        else:
            pass

    def _message_event(self, event):
        if event.object.payload['next_action'] in ['show_first_page', 'show_second_page', 'hide_passport']:
            commands.passport_event.handle(event, self.db, self.utils, self.group_api)

    def parse_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            self._message_new(event)
        if event.type == VkBotEventType.MESSAGE_EVENT:
            self._message_event(event)
