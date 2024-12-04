import asyncio
import enum
import os.path
import secrets
import ssl
import string
import sys
from configparser import ConfigParser
from dataclasses import dataclass
from typing import Union, Optional

import aiohttp
import certifi
from aiohttp import ClientSession
from environs import Env
from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


class Yandex360OrderType(enum.Enum):
    by_id = 'id'
    by_name = 'name'


@dataclass
class Yandex360QueryParams:
    page: Optional[int] = None
    per_page: Optional[int] = None
    parentID: Optional[str] = None
    pageToken: Optional[str] = None
    pageSize: Optional[int] = None
    orderBy: Union[Optional[Yandex360OrderType], None] = None

    def to_json(self) -> dict:
        result = dict()
        if self.page is not None:
            result['page'] = self.page
        if self.per_page is not None:
            result['perPage'] = self.per_page
        if self.parentID is not None:
            result['parentID'] = self.parentID
        if self.orderBy is not None:
            result['orderBy'] = self.orderBy.value
        if self.pageToken is not None:
            result['pageToken'] = self.pageToken
        if self.pageSize is not None:
            result['pageSize'] = self.pageSize
        return result


class Yandex360Exception(Exception):

    def __init__(self, message: str):
        self.message = message
        logger.info(message)
        super().__init__(self.message)


@dataclass
class Yandex360ClientSecret:
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
            raise Yandex360Exception("Yandex360ClientSecret. Unable to parse json data.")
        if data.get('verification_code') is not None:
            verification_code = data['verification_code']
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
        if 'Yandex360TokenData' in config_parser.sections():
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
class Yandex360UserContact:
    alias: bool
    label: str
    main: bool
    synthetic: bool
    type: str
    value: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360UserContact(
            alias=data.get('alias'),
            label=data.get('label'),
            main=data.get('main'),
            synthetic=data.get('synthetic'),
            type=data.get('type'),
            value=data.get('value')
        )


@dataclass
class Yandex360UserName:
    first: str
    last: str
    middle: Optional[str] = None

    @staticmethod
    def from_json(data: dict):
        return Yandex360UserName(
            first=data.get('first'),
            last=data.get('last'),
            middle=data.get('middle'),
        )

    def to_json(self):
        result = dict()
        result['first'] = self.first
        result['last'] = self.last
        if self.middle is not None:
            result['middle'] = self.middle
        return result


@dataclass
class Yandex360User:
    about: str
    aliases: list[str]
    avatarId: str
    birthday: str
    contacts: list[Yandex360UserContact]
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
    name: Yandex360UserName
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
            contacts=[Yandex360UserContact.from_json(contact) for contact in data.get('contacts')],
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
            name=Yandex360UserName.from_json(data.get('name')),
            nickname=data.get('nickname'),
            position=data.get('position'),
            timezone=data.get('timezone'),
            updatedAt=data.get('updatedAt'),
        )


class Yandex360GroupMemberGroupMemberType(enum.Enum):
    user = 'user'
    group = 'group'
    department = 'department'


@dataclass
class Yandex360GroupMember:
    id: str
    type: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360GroupMember(
            id=data.get('id'),
            type=Yandex360GroupMemberGroupMemberType.group.value if data.get(
                'type') == 'group' else Yandex360GroupMemberGroupMemberType.department.value if data.get(
                'type') == 'department' else Yandex360GroupMemberGroupMemberType.user.value
        )


@dataclass
class Yandex360Group:
    adminIds: list[str]
    aliases: list[str]
    authorId: str
    createdAt: str
    description: str
    email: str
    externalId: str
    id: str
    label: str
    memberOf: list[str]
    members: list[Yandex360GroupMember]
    membersCount: str
    name: str
    removed: bool
    type: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360Group(
            adminIds=data.get('adminIds'),
            aliases=data.get('aliases'),
            authorId=data.get('authorId'),
            createdAt=data.get('createdAt'),
            description=data.get('description'),
            email=data.get('email'),
            externalId=data.get('externalId'),
            id=data.get('id'),
            label=data.get('label'),
            memberOf=data.get('memberOf'),
            members=[Yandex360GroupMember.from_json(member) for member in data.get('members')],
            membersCount=data.get('membersCount'),
            name=data.get('name'),
            removed=data.get('removed'),
            type=data.get('type'),
        )


@dataclass
class Yandex360ShortDepartment:
    id: str
    membersCount: str
    name: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360ShortDepartment(
            id=data.get('id'),
            membersCount=data.get('membersCount'),
            name=data.get('name'),
        )


@dataclass
class Yandex360ShortGroup:
    id: str
    membersCount: str
    name: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360ShortGroup(
            id=data.get('id'),
            membersCount=data.get('membersCount'),
            name=data.get('name'),
        )


@dataclass
class Yandex360ShortUser:
    avatarId: str
    departmentId: str
    email: str
    gender: str
    id: str
    name: Yandex360UserName
    nickname: str
    position: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360ShortUser(
            avatarId=data.get('avatarId'),
            departmentId=data.get('departmentId'),
            email=data.get('email'),
            gender=data.get('gender'),
            id=data.get('id'),
            name=Yandex360UserName.from_json(data=data.get('name')),
            nickname=data.get('nickname'),
            position=data.get('position'),
        )


@dataclass
class Yandex360GroupMembers:
    departments: list[Yandex360ShortDepartment]
    groups: list[Yandex360ShortGroup]
    users: list[Yandex360ShortUser]

    @staticmethod
    def from_json(data: dict):
        return Yandex360GroupMembers(
            departments=[Yandex360ShortDepartment.from_json(department) for department in data.get('departments')],
            groups=[Yandex360ShortGroup.from_json(group) for group in data.get('groups')],
            users=[Yandex360ShortUser.from_json(user) for user in data.get('users')],
        )


@dataclass
class Yandex360Department:
    aliases: list[str]
    createdAt: str
    description: str
    email: str
    externalId: str
    headId: str
    id: str
    label: str
    membersCount: str
    name: str
    parentId: str

    @staticmethod
    def from_json(data: dict):
        return Yandex360Department(
            aliases=data.get('aliases'),
            createdAt=data.get('createdAt'),
            description=data.get('description'),
            email=data.get('email'),
            externalId=data.get('externalId'),
            headId=data.get('headId'),
            id=data.get('id'),
            label=data.get('label'),
            membersCount=data.get('membersCount'),
            name=data.get('name'),
            parentId=data.get('parentId'),
        )


class Yandex360UserContactType(enum.Enum):
    email = 'email'
    phone_extension = 'phone_extension'
    phone = 'phone'
    site = 'site'
    icq = 'icq'
    twitter = 'twitter'
    skype = 'skype'


@dataclass
class Yandex360UserContactParams:
    type: Yandex360UserContactType
    value: str
    label: Optional[str] = None

    def to_json(self):
        result = dict()
        result['type'] = self.type.value
        result['value'] = self.value
        if self.label is not None:
            result['label'] = self.label
        return result


@dataclass
class Yandex360UserEditQueryParams:
    about: Optional[str] = None
    birthday: Optional[str] = None
    contacts: Optional[list[Yandex360UserContactParams]] = None
    departmentId: Optional[str] = None
    displayName: Optional[str] = None
    externalId: Optional[str] = None
    gender: Optional[str] = None
    isAdmin: Optional[bool] = None
    isEnabled: Optional[bool] = None
    language: Optional[str] = None
    name: Optional[Yandex360UserName] = None
    password: Optional[str] = None
    passwordChangeRequired: Optional[bool] = None
    position: Optional[str] = None
    timezone: Optional[str] = None

    def to_json(self):
        result = dict()
        if self.about is not None:
            result['about'] = self.about
        if self.birthday is not None:
            result['birthday'] = self.birthday
        if self.contacts is not None:
            result['contacts'] = [contact.to_json() for contact in self.contacts]
        if self.departmentId is not None:
            result['departmentId'] = self.departmentId
        if self.displayName is not None:
            result['displayName'] = self.displayName
        if self.externalId is not None:
            result['externalId'] = self.externalId
        if self.gender is not None:
            result['gender'] = self.gender
        if self.isAdmin is not None:
            result['isAdmin'] = self.isAdmin
        if self.isEnabled is not None:
            result['isEnabled'] = self.isEnabled
        if self.language is not None:
            result['language'] = self.language
        if self.name is not None:
            result['name'] = self.name.to_json()
        if self.password is not None:
            result['password'] = self.password
        if self.passwordChangeRequired is not None:
            result['passwordChangeRequired'] = self.passwordChangeRequired
        if self.position is not None:
            result['position'] = self.position
        if self.timezone is not None:
            result['timezone'] = self.timezone
        return result


class AIOYa360Client:
    config_file_name: str
    _client_secret: Yandex360ClientSecret = None
    _token_data: Yandex360TokenData = None
    _session: Union[ClientSession, None] = None

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
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def fetch_get(self, url: str, params: Yandex360QueryParams = Yandex360QueryParams()) -> dict:

        async with self._session.get(
                url=url,
                params=params.to_json()
        ) as resp:
            if resp.status != 200:
                raise Yandex360Exception(
                    message=(await resp.json()).get('error_description')
                )
            return await resp.json()

    async def fetch_get_pages(self, url: str, params: Yandex360QueryParams = Yandex360QueryParams()) -> tuple:
        try:
            response = await self.fetch_get(
                url=url,
                params=params,
            )
        except Yandex360Exception:
            return tuple()
        pages = response.get('pages')
        try:
            responses = await asyncio.gather(
                *[
                    self.fetch_get(
                        url=url,
                        params=Yandex360QueryParams(
                            page=page,
                            per_page=params.per_page,
                            orderBy=params.orderBy,
                            pageSize=params.pageSize,
                            pageToken=params.pageToken,
                            parentID=params.parentID,
                        )
                    ) for page in range(1, pages + 1)
                ],
                return_exceptions=True
            )
        except Yandex360Exception:
            return tuple()
        return responses

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
                    
                    Receive the verification code and put it in `{config_file_name}` file next to client_id and client_secret.
                    
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
            try:
                response = await self.fetch_get(
                    url=self.base_url + '/directory/v1/org',
                    params=Yandex360QueryParams(
                        pageSize=10,
                        pageToken=next_page_token,
                    )
                )
            except Yandex360Exception:
                return organization_list
            for organization in response.get('organizations'):
                organization_list.append(Yandex360Organization.from_json(organization))
            next_page_token = response.get('nextPageToken')
            if next_page_token == '':
                break
        return organization_list

    async def get_users_list(self, org_id: int) -> list[Yandex360User]:
        user_list = []
        try:
            responses = await self.fetch_get_pages(
                url=self.base_url + f'/directory/v1/org/{org_id}/users',
            )
        except Yandex360Exception:
            return list()
        for response in responses:
            for user in response.get('users'):
                ya_user = Yandex360User.from_json(user)
                if ya_user not in user_list:
                    user_list.append(ya_user)
        return user_list

    async def get_current_user(self, org_id: int, user_id: str) -> Yandex360User:
        return Yandex360User.from_json(
            await self.fetch_get(
                url=self.base_url + f'/directory/v1/org/{org_id}/users/{user_id}',
            )
        )

    async def get_groups_list(self, org_id: int) -> list[Yandex360Group]:
        groups_list = []
        try:
            responses = await self.fetch_get_pages(
                url=self.base_url + f'/directory/v1/org/{org_id}/groups'
            )
        except Yandex360Exception:
            return list()
        for response in responses:
            for group in response.get('groups'):
                ya_group = Yandex360Group.from_json(group)
                if ya_group not in groups_list:
                    groups_list.append(ya_group)
            return groups_list

    async def get_current_group(self, org_id: str, group_id: str) -> Yandex360Group:
        return Yandex360Group.from_json(
            await self.fetch_get(
                url=self.base_url + f'/directory/v1/org/{org_id}/groups/{group_id}',
            )
        )

    async def get_group_members(self, org_id: str, group_id: str) -> Yandex360GroupMembers:
        return Yandex360GroupMembers.from_json(
            await self.fetch_get(
                url=self.base_url + f'/directory/v1/org/{org_id}/groups/{group_id}/members',
            )
        )

    async def get_departments_list(self,
                                   org_id: str,
                                   order_by: Yandex360OrderType = Yandex360OrderType.by_id,
                                   parent_id: str = None,
                                   ) -> list[Yandex360Department]:
        departments_list = []
        try:
            responses = await self.fetch_get_pages(
                url=self.base_url + f'/directory/v1/org/{org_id}/departments',
                params=Yandex360QueryParams(
                    orderBy=order_by,
                    parentID=parent_id
                )
            )
        except Yandex360Exception:
            return list()
        for response in responses:
            for department in response.get('departments'):
                ya_department = Yandex360Department.from_json(department)
                if ya_department not in departments_list:
                    departments_list.append(ya_department)
            return departments_list

    async def get_current_department(self, org_id: str, department_id: str) -> Yandex360Department:
        return Yandex360Department.from_json(
            await self.fetch_get(
                url=self.base_url + f'/directory/v1/org/{org_id}/departments/{department_id}'
            )
        )

    async def edit_user(self, org_id: str, user_id: str,
                        params: Optional[Yandex360UserEditQueryParams] = None):
        async with self._session.patch(
                url=self.base_url + f'/directory/v1/org/{org_id}/users/{user_id}',
                json=params.to_json() if params is not None else None
        ) as response:
            if response.status != 200:
                raise Yandex360Exception(
                    message=(await response.json())
                )
            return Yandex360User.from_json(
                data=await response.json()
            )
