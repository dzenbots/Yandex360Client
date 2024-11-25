from requests import Session


class Yandex360Client(Session):

    def __init__(self, client_id=None, client_secret=None):
        super(Yandex360Client, self).__init__()
        self._client_id = client_id
        self._client_secret = client_secret

    def get_client_id(self):
        return self._client_id

    def get_client_secret(self):
        return self._client_secret

