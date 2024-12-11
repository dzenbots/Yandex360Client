import os
from configparser import ConfigParser
from dataclasses import dataclass

from aio_ya_360.exceptions import Ya360Exception


@dataclass
class TokenData:
    access_token: str = None
    expires_in: str = None
    refresh_token: str = None
    token_type: str = None

    @staticmethod
    def from_json(data: dict):
        try:
            access_token = data['access_token']
            expires_in = data['expires_in']
            refresh_token = data['refresh_token']
            token_type = data['token_type']
        except:
            raise Ya360Exception("TokenData. Unable to parse json data.")
        return TokenData(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            token_type=token_type
        )

    @staticmethod
    def from_config(config_file_name: str):
        config_parser = ConfigParser()
        if os.path.exists(config_file_name):
            config_parser.read(config_file_name)
            if 'Yandex360TokenData' in config_parser.sections():
                try:
                    access_token = config_parser.get('Yandex360TokenData', 'access_token')
                    expires_in = config_parser.get('Yandex360TokenData', 'expires_in')
                    refresh_token = config_parser.get('Yandex360TokenData', 'refresh_token')
                    token_type = config_parser.get('Yandex360TokenData', 'token_type')
                except:
                    raise Ya360Exception(f"TokenData. Unable to parse token data from {config_file_name}")
                return TokenData(
                    access_token=access_token,
                    expires_in=expires_in,
                    refresh_token=refresh_token,
                    token_type=token_type
                )
        else:
            return None

    def save_to_config(self, config_file_name: str):
        config_parser = ConfigParser()
        config_parser.read(config_file_name)
        if 'Yandex360TokenData' not in config_parser.sections():
            config_parser.add_section('Yandex360TokenData')
        config_parser.set(section='Yandex360TokenData', option='access_token', value=str(self.access_token))
        config_parser.set(section='Yandex360TokenData', option='refresh_token', value=str(self.refresh_token))
        config_parser.set(section='Yandex360TokenData', option='expires_in', value=str(self.expires_in))
        config_parser.set(section='Yandex360TokenData', option='token_type', value=str(self.token_type))
        with open(config_file_name, 'w') as configfile:
            config_parser.write(configfile)
