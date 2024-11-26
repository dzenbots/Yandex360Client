import base64
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from typing import Union

from loguru import logger
from requests import Session

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


class Yandex360Exception(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


@dataclass
class Yandex360TokenData:
    access_token: str = None
    expires_in: str = None
    refresh_token: str = None
    token_type: str = None

    def from_json(self, data: dict):
        self.access_token = data['access_token']
        self.expires_in = data['expires_in']
        self.refresh_token = data['refresh_token']
        self.token_type = data['token_type']
        return self

    def from_config(self, config: ConfigParser):
        self.access_token = config.get('YANDEX360', 'ACCESS_TOKEN')
        self.expires_in = config.get('YANDEX360', 'EXPIRES_IN')
        self.refresh_token = config.get('YANDEX360', 'REFRESH_TOKEN')
        self.token_type = config.get('YANDEX360', 'TOKEN_TYPE')
        return self


class Yandex360Client(Session):
    _client_id: Union[str, None] = None
    _client_secret: Union[str, None] = None
    _verification_code: Union[str, None] = None
    _token_data: Yandex360TokenData = None

    def __init__(self,
                 client_id: Union[str, None] = None,
                 client_secret: Union[str, None] = None,
                 verification_code: Union[str, None] = None,
                 token_data: Yandex360TokenData = None
                 ):
        super(Yandex360Client, self).__init__()
        self._client_id = client_id
        self._client_secret = client_secret
        self._verification_code = verification_code
        self._token_data = token_data

    def get_oauth_token(self):
        if self._token_data is None:
            response = self.post(
                url='https://oauth.yandex.ru/token',
                headers={
                    'Content-type': 'application/x-www-form-urlencoded',
                },
                data={
                    'grant_type': 'authorization_code',
                    'code': self._verification_code,
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                }
            )
            if response.status_code != 200:
                message = f'{response.json().get('error_description')}'
                logger.info(message)
                raise Yandex360Exception(
                    message=message
                )
            self._token_data = Yandex360TokenData().from_json(response.json())
            return self._token_data.access_token is not None

    def update_access_token(self):
        if self._token_data is None:
            raise Yandex360Exception(message='Info about token is missing')
        response = self.post(
            url='https://oauth.yandex.ru/token',
            headers={
                'Content-type': 'application/x-www-form-urlencoded',
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self._token_data.refresh_token,
                'client_id': self._client_id,
                'client_secret': self._client_secret,
            }
        )
        if response.status_code != 200:
            message = f'{response.json().get("error_description")}'
            logger.info(message)
            raise Yandex360Exception(message=message)
        self._token_data = Yandex360TokenData().from_json(response.json())
        return self._token_data.access_token is not None

    def get_client_id(self):
        return self._client_id

    def get_client_secret(self):
        return self._client_secret

    def get_token_data(self):
        return self._token_data
