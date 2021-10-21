import json
import random


def handle(event, db, utils, api):
    action = event.object.payload.pop('next_action')
    ids = event.object.payload.pop('ids')

    if ids['caller_id'] == event.object.user_id or ids['caller_id'] == 0:
        user_passport = db.find({'user_id': ids['passport_id']}) if ids['passport_id'] != 0 else 0

        if user_passport is not None:
            if action == 'show_first_page':
                keyboard_one = utils.get_callback_keyboard(
                    {'b1': {'label': 'открыть вторую страницу.', 'color': 'positive', 'payload':
                     {'type': 'show_snackbar', 'text': 'вы открыли вторую страницу паспорта.', 'next_action': 'show_second_page',
                      'ids': {'caller_id': ids['caller_id'], 'passport_id': ids['passport_id']}}}},
                    {'b1': {'label': 'скрыть паспорт.', 'color': 'secondary', 'payload':
                     {'type': 'show_snackbar', 'text': 'вы скрыли паспорт.', 'next_action': 'hide_passport',
                      'ids': {'caller_id': ids['caller_id'], 'passport_id': 0}}}})
                utils.message_pool.edit(text=f'💳 паспорт [id{ids["passport_id"]}|пользователя]:\n'
                                             f'| имя - {user_passport["first_name"]}.\n'
                                             f'| фамилия - {user_passport["last_name"]}.\n'
                                             f'| роль - {user_passport["role"]}.\n',
                                        cmid=event.object.conversation_message_id,
                                        peer_id=event.object.peer_id,
                                        disable_mentions=True, keyboard=keyboard_one)
            if action == 'show_second_page':
                keyboard_two = utils.get_callback_keyboard(
                    {'b1': {'label': 'открыть первую страницу.', 'color': 'positive', 'payload':
                     {'type': 'show_snackbar', 'text': 'вы открыли первую страницу паспорта.', 'next_action': 'show_first_page',
                      'ids': {'caller_id': ids['caller_id'], 'passport_id': ids['passport_id']}}}},
                    {'b1': {'label': 'скрыть паспорт.', 'color': 'secondary', 'payload':
                     {'type': 'show_snackbar', 'text': 'вы скрыли паспорт.', 'next_action': 'hide_passport',
                      'ids': {'caller_id': ids['caller_id'], 'passport_id': 0}}}})
                utils.message_pool.edit(text=f'🔍 доп. информация [id{ids["passport_id"]}|пользователя]:\n'
                                             f'| дата регистрации паспорта: {user_passport["reg_date"]}\n'
                                             f'| дата регистрации в беседе: {user_passport["join_date"]}\n'
                                             f'| добавил в беседу: @{user_passport["invited_by"]}',
                                        cmid=event.object.conversation_message_id,
                                        peer_id=event.object.peer_id,
                                        disable_mentions=True, keyboard=keyboard_two)
            if action == 'hide_passport':
                utils.message_pool.delete(peer_id=event.object.peer_id, cmid=event.object.conversation_message_id)
        if user_passport is not None:
            api.messages.sendMessageEventAnswer(
                event_id=event.object.event_id,
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                event_data=json.dumps(event.object.payload))
        else:
            api.messages.sendMessageEventAnswer(
                event_id=event.object.event_id,
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                event_data='{"type": "show_snackbar", "text": "у данного пользователя отсутствует паспорт."}')
            utils.message_pool.edit(text=f'у [id{ids["passport_id"]}|пользователя] отсутствует паспорт.',
                                    cmid=event.object.conversation_message_id,
                                    peer_id=event.object.peer_id,
                                    disable_mentions=True)
    else:
        answers = ['эта кнопочка не для тебя!', 'ты слишком любопытный, не думаешь?',
                   'ещё раз жмякнешь на кнопочку и... ничего не произойдет.']
        api.messages.sendMessageEventAnswer(
            event_id=event.object.event_id,
            user_id=event.object.user_id,
            peer_id=event.object.peer_id,
            event_data=f'{{"type": "show_snackbar", "text": "{random.choice(answers)}"}}')
