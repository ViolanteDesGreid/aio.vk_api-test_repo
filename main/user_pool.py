import vk_api


class VkUsers:
    def __init__(self, access_tokens: list):
        super().__init__()
        self.access_tokens = access_tokens
        self.user_objects = []

    def auth(self, first=False, access_token=''):
        if first:
            for _ in range(0, len(self.access_tokens)):
                vk_session = vk_api.VkApi(token=self.access_tokens.pop(0))
                self.user_objects.append({'vk_session': vk_session, 'api': vk_session.get_api(),
                                          'uid': vk_session.method('users.get')[0]['id']})
        else:
            self.user_objects.append(vk_api.VkApi(token=access_token))

    def add_token(self, access_token: str):
        self.auth(access_token=access_token)

    def method(self, method, params=None, change=True):
        result = self.user_objects[0]['vk_session'].method(method=method, values=params)
        if change is True:
            self.user_objects.append(self.user_objects.pop(0))
        return result
