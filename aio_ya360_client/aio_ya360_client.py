import asyncio
import os.path
import ssl
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from typing import Union

import aiohttp
import certifi
from aiohttp import ClientSession
from environs import Env
from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


class Yandex360Exception(Exception):

    def __init__(self, message: str):
        self.message = message
        logger.info(message)
        super().__init__(self.message)


@dataclass
class Yandex360ClientSecret:
    client_id: str = ''
    client_secret: str = ''
    verification_code: str = ''

    @staticmethod
    def from_json(data: dict):
        verification_code: str = ''
        try:
            client_id = data['client_id']
            client_secret = data['client_secret']
        except:
            raise Yandex360Exception("Yandex360ClientSecret. Unable to parse json data.")
        try:
            verification_code = data['verification_code']
        except:
            pass
        return Yandex360ClientSecret(
            client_id=client_id,
            client_secret=client_secret,
            verification_code=verification_code
        )

    @staticmethod
    def from_config(config_file_name: str):
        verification_code: str = ''
        config_parser = ConfigParser()
        config_parser.read(config_file_name)
        try:
            client_id = config_parser.get('Yandex360ClientSecret', 'client_id')
            client_secret = config_parser.get('Yandex360ClientSecret', 'client_secret')
        except:
            raise Yandex360Exception("Yandex360ClientSecret. Unable to parse config data.")
        try:
            verification_code = config_parser.get('Yandex360ClientSecret', 'verification_code')
        except:
            pass
        return Yandex360ClientSecret(
            client_id=client_id,
            client_secret=client_secret,
            verification_code=verification_code
        )

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


@dataclass
class Yandex360TokenData:
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
            raise Yandex360Exception("Yandex360TokenData. Unable to parse json data.")
        return Yandex360TokenData(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            token_type=token_type
        )

    @staticmethod
    def from_config(config_file_name: str):
        config_parser = ConfigParser()
        config_parser.read(config_file_name)
        try:
            access_token = config_parser.get('Yandex360TokenData', 'access_token')
            expires_in = config_parser.get('Yandex360TokenData', 'expires_in')
            refresh_token = config_parser.get('Yandex360TokenData', 'refresh_token')
            token_type = config_parser.get('Yandex360TokenData', 'token_type')
        except:
            raise Yandex360Exception("Yandex360TokenData. Unable to parse config data.")
        return Yandex360TokenData(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            token_type=token_type
        )

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


@dataclass
class Yandex360Organization:
    id: int
    name: str
    email: str
    phone: str
    fax: str
    language: str
    subscriptionPlan: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360Organization(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            fax=data.get('fax'),
            language=data.get('language'),
            subscriptionPlan=data.get('subscriptionPlan')
        )


@dataclass
class UserContact:
    alias: bool
    label: str
    main: bool
    synthetic: bool
    type: str
    value: str

    @staticmethod
    def from_json(data: dict):
        return UserContact(
            alias=data.get('alias'),
            label=data.get('label'),
            main=data.get('main'),
            synthetic=data.get('synthetic'),
            type=data.get('type'),
            value=data.get('value')
        )


@dataclass
class UserName:
    first: str
    last: str
    middle: str

    @staticmethod
    def from_json(data: dict):
        return UserName(
            first=data.get('first'),
            last=data.get('last'),
            middle=data.get('middle'),
        )


@dataclass
class Yandex360User:
    about: str
    aliases: list[str]
    avatarId: str
    birthday: str
    contacts: list[UserContact]
    createdAt: str
    departmentID: str
    email: str
    externalId: str
    gender: str
    groups: list[str]
    id: str
    isAdmin: str
    isDismissed: str
    isEnabled: str
    isRobot: str
    language: str
    name: UserName
    nickname: str
    position: str
    timezone: str
    updatedAt: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360User(
            about=data.get('about'),
            aliases=data.get('aliases'),
            avatarId=data.get('avatarId'),
            birthday=data.get('birthday'),
            contacts=[UserContact.from_json(contact) for contact in data.get('contacts')],
            createdAt=data.get('createdAt'),
            departmentID=data.get('departmentID'),
            email=data.get('email'),
            externalId=data.get('externalId'),
            gender=data.get('gender'),
            groups=data.get('groups'),
            id=data.get('id'),
            isAdmin=data.get('isAdmin'),
            isDismissed=data.get('isDismissed'),
            isEnabled=data.get('isEnabled'),
            isRobot=data.get('isRobot'),
            language=data.get('language'),
            name=UserName.from_json(data.get('name')),
            nickname=data.get('nickname'),
            position=data.get('position'),
            timezone=data.get('timezone'),
            updatedAt=data.get('updatedAt'),
        )


class AIOYa360Client:
    config_file_name: str
    _client_secret: Yandex360ClientSecret = None
    _token_data: Yandex360TokenData = None
    _session: Union[ClientSession, None]

    base_url: str = 'https://api360.yandex.net'

    def __init__(self,
                 client_secret: Yandex360ClientSecret = None,
                 token_data: Yandex360TokenData = None,
                 config_file_name: str = 'config.ini'
                 ):
        if os.path.exists(config_file_name):
            try:
                self._client_secret = Yandex360ClientSecret.from_config(config_file_name)
                self._token_data = Yandex360TokenData.from_config(config_file_name)
            except:
                pass
        else:
            if client_secret is None:
                raise Yandex360Exception('AIOYa360Client. Unable to create AIOYa360Client')
            self.config_file_name = config_file_name
            self._client_secret = client_secret
            self._token_data = token_data
            if self._client_secret is None:
                raise Yandex360Exception(message='No client secret provided.')
            else:
                self._client_secret.save_to_config(config_file_name)

    async def close_session(self):
        await self._session.close()
        self._session = None

    async def start_work(self, config_file_name: str = 'config.ini') -> bool:
        self._session = ClientSession(
            connector=aiohttp.TCPConnector(
                ssl=ssl.create_default_context(
                    cafile=certifi.where()
                )
            )
        )
        resp = None
        if self._token_data is None:
            if self._client_secret.verification_code == '':
                await self.close_session()
                raise Yandex360Exception(
                    f"""
                    
                    AIOYa360Client.start_work. No verification code provided.
                    Verification code is required. You can achieve it by authorizing at 'https://oauth.yandex.ru/authorize?response_type=code&client_id=<your Client ID>'
                    Link for you is 'https://oauth.yandex.ru/authorize?response_type=code&client_id={self._client_secret.client_id}'
                    
                    Receive the verification code and put it in `.env` file next to client_id and client_secret.
                    
                    """
                )
            async with self._session.post(
                    url='https://oauth.yandex.ru/token',
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    data={
                        'grant_type': 'authorization_code',
                        'code': self._client_secret.verification_code,
                        'client_id': self._client_secret.client_id,
                        'client_secret': self._client_secret.client_secret,
                    }
            ) as response:
                if response.status != 200:
                    raise Yandex360Exception(
                        message=(await response.json()).get('error_description')
                    )
                resp = await response.json()
        else:
            async with self._session.post(
                    url='https://oauth.yandex.ru/token',
                    headers={
                        'Content-type': 'application/x-www-form-urlencoded',
                    },
                    data={
                        'grant_type': 'refresh_token',
                        'refresh_token': self._token_data.refresh_token,
                        'client_id': self._client_secret.client_id,
                        'client_secret': self._client_secret.client_secret,
                    }
            ) as response:
                if response.status != 200:
                    raise Yandex360Exception(
                        message=(await response.json()).get('error_description')
                    )
                resp = await response.json()
        if resp is None:
            raise Yandex360Exception(
                message='Unable to work with current parameters'
            )
        self._token_data = Yandex360TokenData.from_json(resp)
        self._token_data.save_to_config(config_file_name=config_file_name)
        self._session.headers.update(
            {
                'Authorization': f'OAuth {self._token_data.access_token}',
            }
        )
        return self._token_data.access_token is not None

    async def get_organizations_list(self) -> list[Yandex360Organization]:
        organization_list = []
        next_page_token = ''
        while True:
            async with self._session.get(
                    url=self.base_url + '/directory/v1/org',
                    params={
                        'pageSize': 10,
                        'pageToken': next_page_token
                    }
            ) as response:
                if response.status != 200:
                    raise Yandex360Exception(
                        message=(await response.json()).get('error_description')
                    )
                for organization in (await response.json()).get('organizations'):
                    organization_list.append(Yandex360Organization.from_json(organization))
                next_page_token = (await response.json()).get('nextPageToken')
            if next_page_token == '':
                break
        return organization_list

    async def get_users_list(self, org_id: int) -> list[Yandex360User]:

        async def fetch(session: ClientSession, page_num: int):
            async with session.get(
                    url=self.base_url + f'/directory/v1/org/{org_id}/users',
                    params={
                        'page': page_num,
                        'perPage': 10,
                    }
            ) as resp:
                if resp.status != 200:
                    raise Yandex360Exception(
                        message=(await resp.json()).get('error_description')
                    )
                return await resp.json()

        user_list = []
        page = 0
        per_page = 10
        response = await fetch(self._session, 0)
        pages = response.get('pages')
        responses = await asyncio.gather(
            *[
                fetch(self._session, page) for page in range(0, pages)
            ],
            return_exceptions=True
        )
        for response in responses:
            for user in response.get('users'):
                user_list.append(Yandex360User.from_json(user))
        return user_list


async def main():
    env = Env()
    env.read_env()
    client = AIOYa360Client(
        client_secret=Yandex360ClientSecret.from_json(
            data={
                'client_id': env.str('CLIENT_ID'),
                'client_secret': env.str('CLIENT_SECRET'),
                'verification_code': env.str('VERIFICATION_CODE')
            }
        )
    )
    try:
        await client.start_work(config_file_name=env.str('CONFIG_FILE_NAME'))
        organizations = await client.get_organizations_list()
        for organization in organizations:
            print(organization)
        users = await client.get_users_list(org_id=env.int('ORGANISATION_ID'))
        for user in users:
            print(user)
    except Yandex360Exception:
        await client.close_session()
    await client.close_session()


if __name__ == "__main__":
    asyncio.run(main())
