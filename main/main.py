from group_longpoll import *
from database import *

if __name__ == "__main__":
    config = {
        'user_access_tokens': ['-',
                               '-'],

        'group_access_token': '-',

        'group_id': 206810547,

        'chat_config': {'owner_id': 283293933, 'user_arсhive_id': 401, 'group_archive_id': 3},

        'db': DataBase('mongodb://localhost:27017/vk', 'vk', 'passports'),
        }

    VkGroupLongpoll(**config).start()
