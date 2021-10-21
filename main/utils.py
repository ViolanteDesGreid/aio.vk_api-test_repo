import time
import threading

from vk_api.keyboard import VkKeyboard


class VkUtils:
    def __init__(self, api):
        self.api = api
        self.message_pool = self.GroupMessagesPool(self.api)
        threading.Thread(target=self.message_pool.deleter, name='MessagePoolDeleter').start()

    def find_ids(self, event):
        string, ids = event['text'], []
        while -1 not in [one := string.find('['), two := string.find('|'),
                         three := string.find(']')] and one < two < three:
            if string[one + 1:two].startswith('club') is not True:
                ids.append(self.api.users.get(user_ids=string[one + 1:two])[0]['id'])
            else:
                ids.append(string[one + 1:two].replace('club', '-'))
            string = ' '.join([x for x in string.split(' ') if x != string[one:three + 1]])
        while -1 not in [one := string.find('http'), two := string.find('vk.com/')] and one < two:
            for word in string.split():
                if -1 not in [one := word.find('http'), two := word.find('vk.com/')] and one < two:
                    if word[two + 7:].startswith('club') is not True:
                        try:
                            ids.append(self.api.users.get(user_ids=word[two + 7:])[0]['id'])
                        except vk_api.ApiError:
                            try:
                                ids.append(self.api.groups.getById(group_id=word[two + 7:])[0]['id'] * -1)
                            except Exception as err:
                                print(err)
                    else:
                        ids.append(word[two + 7:].replace('club', '-'))
                    string = ' '.join(x for x in string.split() if x != word)
        try:
            if len(fwd_messages := event['fwd_messages']) != 0:
                for fwd_message in fwd_messages:
                    ids.append(fwd_message['from_id'])
            if (reply_message := event.get('reply_message')) is not None:
                ids.append(reply_message['from_id'])
        except TypeError:
            pass
        return ids

    @staticmethod
    def get_callback_keyboard(*args):
        keyboard = VkKeyboard(one_time=False, inline=True)
        for x in range(0, len(args)):
            row = args[x]
            if len(row) <= 3:
                for button_key in row:
                    keyboard.add_callback_button(**row[button_key])
            else:
                for z in range(0, 3):
                    keyboard.add_callback_button(**row[list(row.keys())[z]])
            if x+1 != len(args):
                keyboard.add_line()
            else:
                pass

        return keyboard.get_keyboard()

    class GroupMessagesPool:
        def __init__(self, api):
            self.api = api
            self.message_objects = []
            self.deletion_time = 1

        def send(self, peer_id, random_id=0, expire_ttl=0, message=None, delete_after=False, **kwargs):
            if delete_after is True:
                response = self.api.messages.send(peer_ids=peer_id, random_id=random_id,
                                                  expire_ttl=expire_ttl, message=message, **kwargs)
                self.message_objects.append({'peer_id': response[0]['peer_id'], 'time': time.time(),
                                             'cmid': response[0]['conversation_message_id']})
            elif delete_after is not True:
                self.api.messages.send(peer_ids=peer_id, random_id=random_id,
                                       expire_ttl=expire_ttl, message=message, **kwargs)

        def edit(self, text, peer_id, cmid=0, message_id=0, **kwargs):
            if cmid != 0 and message_id == 0:
                self.api.messages.edit(message=text, peer_id=peer_id, conversation_message_id=cmid, **kwargs)
            if cmid == 0 and message_id != 0:
                self.api.messages.edit(message=text, peer_id=peer_id, message_id=message_id, **kwargs)

        def remove_cmid_from_queue(self, cmid):
            for message_object in self.message_objects:
                if message_object['cmid'] == cmid:
                    self.message_objects.remove(message_object)

        def delete(self, peer_id, cmid):
            self.remove_cmid_from_queue(cmid=cmid)
            self.api.messages.delete(peer_id=peer_id, conversation_message_ids=cmid, delete_for_all=True)

        def deleter(self):
            while True:
                time.sleep(1)
                for message in self.message_objects:
                    if float((time.time() - message['time']) / 60) >= float(self.deletion_time):
                        self.message_objects.remove(message)
                        self.api.messages.delete(delete_for_all=True, peer_id=message['peer_id'],
                                                 conversation_message_ids=message['cmid'])
