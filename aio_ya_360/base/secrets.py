import os
from configparser import ConfigParser
from dataclasses import dataclass
from typing import Optional

from aio_ya_360.exceptions import Ya360Exception


@dataclass
class Ya360ClientSecrets:
    client_id: str = ''
    client_secret: str = ''
    verification_code: Optional[str] = ''

    @staticmethod
    def from_json(data: dict):
        verification_code: str = ''
        try:
            client_id = data['client_id']
            client_secret = data['client_secret']
        except:
            raise Ya360Exception("Yandex360ClientSecret. Unable to parse json data.")
        if data.get('verification_code') is not None:
            verification_code = data['verification_code']
        return Ya360ClientSecrets(
            client_id=client_id,
            client_secret=client_secret,
            verification_code=verification_code
        )

    @staticmethod
    def from_config(config_file_name: str):
        verification_code: str = ''
        config_parser = ConfigParser()
        if os.path.exists(config_file_name):
            config_parser.read(config_file_name)

            try:
                client_id = config_parser.get('Yandex360ClientSecret', 'client_id')
                client_secret = config_parser.get('Yandex360ClientSecret', 'client_secret')
            except:
                raise Ya360Exception(f"ClientSecret. Unable to parse client secrets from {config_file_name}.")
            try:
                verification_code = config_parser.get('Yandex360ClientSecret', 'verification_code')
            except:
                pass
            return Ya360ClientSecrets(
                client_id=client_id,
                client_secret=client_secret,
                verification_code=verification_code
            )
        return None

    def save_to_config(self, config_file_name: str):
        config_parser = ConfigParser()
        config_parser.read(config_file_name)
        if 'Yandex360ClientSecret' not in config_parser.sections():
            config_parser.add_section('Yandex360ClientSecret')
        config_parser.set(section='Yandex360ClientSecret', option='client_id', value=str(self.client_id))
        config_parser.set(section='Yandex360ClientSecret', option='client_secret', value=str(self.client_secret))
        config_parser.set(section='Yandex360ClientSecret', option='verification_code',
                          value=str(self.verification_code))
        with open(config_file_name, 'w') as configfile:
            config_parser.write(configfile)
