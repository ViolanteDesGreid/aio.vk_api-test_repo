from datetime import datetime as dt
import time


def handle(event, db, group_api, user_pool, chat_config):
    if db.find({'user_id': event.from_id}) is not None:
        group_api.messages.send(peer_id=event.peer_id, random_id=0,
                                message='вы уже имеете паспорт '
                                        'и являетесь гражданином нашей беседы.')
    else:
        user_info = group_api.users.get(user_ids=event.from_id)[0]
        user_conversation_info = [x for x in group_api.messages.getConversationMembers(
            peer_id=event.peer_id)['items'] if user_info['id'] == x['member_id']][0]
        join_date = dt.fromtimestamp(user_conversation_info['join_date'])

        object_id = db.add({
            'user_id': user_info['id'],
            'first_name': user_info['first_name'],
            'last_name': user_info['last_name'],
            'reg_date': time.strftime('%H:%M %d.%m.%y'),
            'join_date': join_date.strftime('%H:%M %d.%m.%y'),
            'invited_by': f'id{user_conversation_info["invited_by"]}',
            'role': 'гражданин беседы'
        })
        group_api.messages.send(peer_id=event.peer_id, random_id=0,
                                message='✨ поздравляем! 🔰\n'
                                        '| теперь вы являетесь гражданином нашей беседы.\n'
                                        '| подробнее о системе паспортов в статье ниже.',
                                attachment='article-206810547_87147_99f3ad8e89d2b1dad3')
        group_api.messages.send(chat_id=chat_config['group_archive_id'], random_id=0, message=f'#new_passport\n@id{event.from_id} registered a passport.\n\n#{object_id}')
        for user_object in user_pool.user_objects:
            if user_object['uid'] == chat_config['owner_id']:
                message_id = user_object['api'].messages.send(chat_id=chat_config['user_arсhive_id'], random_id=0, message=f'!role [id{event.from_id}|{user_info["first_name"]}] 0')
                user_object['api'].messages.delete(message_id=message_id, delete_for_all=True)
