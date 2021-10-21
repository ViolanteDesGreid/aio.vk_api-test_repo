def handle(event, utils):
    uid, uids = 0, utils.find_ids(event)
    if len(event.text.split()) == 2 and event.text.split()[1] in ['help', 'помощь']:
        utils.message_pool.send(peer_id=event.peer_id,
                                attachment='article-206810547_87147_99f3ad8e89d2b1dad3')
    else:
        if len(uids) == 0:
            uid = event.from_id
        elif len(uids) >= 1:
            uid = uids[0]
        keyboard = utils.get_callback_keyboard(
            {'b1': {'label': 'просмотреть паспорт.', 'color': 'positive', 'payload':
             {'type': 'show_snackbar', 'text': 'вы раскрыли паспорт для детального ознакомления.',
              'next_action': 'show_first_page', 'ids': {'caller_id': event.from_id, 'passport_id': uid}}}})
        utils.message_pool.send(peer_id=event.peer_id, keyboard=keyboard, message='&#12288;', delete_after=True)
