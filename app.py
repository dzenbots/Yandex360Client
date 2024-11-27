import os
from configparser import ConfigParser
from typing import Union

from environs import Env

from yandex360client import Yandex360Client
from yandex360client.yandex360client import Yandex360TokenData, Yandex360Exception

org_id: Union[int, None] = None
client: Union[Yandex360Client, None] = None


def main():
    global org_id
    global client
    env = Env()
    config = ConfigParser()
    env.read_env()
    if os.path.exists(env.str('CONFIG_FILE_NAME')):
        config.read(env.str('CONFIG_FILE_NAME'))
        client = Yandex360Client(
            client_id=env.str('CLIENT_ID'),
            client_secret=env.str('CLIENT_SECRET'),
            token_data=Yandex360TokenData().from_config(config=config)
        )
        try:
            client.refresh_access_token()
        except Yandex360Exception as e:
            print(e)
            return
    else:
        client = Yandex360Client(
            client_id=env.str('CLIENT_ID'),
            client_secret=env.str('CLIENT_SECRET'),
            verification_code=env.str('VERIFICATION_CODE'),
        )
        try:
            client.get_oauth_token()
        except Yandex360Exception as e:
            print(e)
            return
    if client is None:
        print('Unauthorized!')
        return
    token_data = client.get_token_data()
    if 'YANDEX360' not in config.sections():
        config.add_section('YANDEX360')
    config.set(section='YANDEX360', option='ACCESS_TOKEN', value=str(token_data.access_token))
    config.set(section='YANDEX360', option='REFRESH_TOKEN', value=str(token_data.refresh_token))
    config.set(section='YANDEX360', option='EXPIRES_IN', value=str(token_data.expires_in))
    config.set(section='YANDEX360', option='TOKEN_TYPE', value=str(token_data.token_type))
    with open(env.str('CONFIG_FILE_NAME'), 'w') as configfile:
        config.write(configfile)

    for organisation in client.get_organisations_list():
        print(organisation)

    for organisation in client.get_organisations_list():
        if organisation.get('name') == env.str('ORGANISATION_NAME'):
            org_id = organisation.get('id')

    for user in client.get_users_list(org_id=org_id):
        print(user)


if __name__ == "__main__":
    main()
