import enum
import string
from dataclasses import dataclass
from typing import Optional

from ..exceptions import Ya360Exception


@dataclass
class Ya360UserContact:
    alias: bool
    label: str
    main: bool
    synthetic: bool
    type: str
    value: str

    @staticmethod
    def from_json(data: dict) -> 'Ya360UserContact':
        return Ya360UserContact(
            alias=data.get('alias'),
            label=data.get('label'),
            main=data.get('main'),
            synthetic=data.get('synthetic'),
            type=data.get('type'),
            value=data.get('value')
        )


@dataclass
class Ya360UserName:
    first: str
    last: str
    middle: Optional[str] = None

    @staticmethod
    def from_json(data: dict):
        return Ya360UserName(
            first=data.get('first'),
            last=data.get('last'),
            middle=data.get('middle'),
        )

    def to_json(self) -> dict:
        result = dict()
        result['first'] = self.first
        result['last'] = self.last
        if self.middle is not None:
            result['middle'] = self.middle
        return result


class Ya360UserContactType(enum.Enum):
    email: str = 'email'
    phone_extension: str = 'phone_extension'
    phone: str = 'phone'
    site: str = 'site'
    icq: str = 'icq'
    twitter: str = 'twitter'
    skype: str = 'skype'


@dataclass
class Ya360UserContactParams:
    type: Ya360UserContactType
    value: str
    label: Optional[str] = None

    def to_json(self) -> dict:
        result = dict()
        result['type'] = self.type.value
        result['value'] = self.value
        if self.label is not None:
            result['label'] = self.label
        return result


@dataclass
class Ya360UserRequestParams:
    about: str = None
    birthday: str = None
    contacts: list[Ya360UserContactParams] = None
    departmentId: str = None
    displayName: str = None
    externalId: str = None
    gender: str = None
    isAdmin: bool = None
    isEnabled: bool = None
    language: str = None
    name: Ya360UserName = None
    password: str = None
    passwordChangeRequired: bool = None
    position: str = None
    timezone: str = None

    def to_json(self) -> dict:
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
            result['isAdmin'] = str(self.isAdmin)
        if self.isEnabled is not None:
            result['isEnabled'] = str(self.isEnabled)
        if self.language is not None:
            result['language'] = self.language
        if self.name is not None:
            result['name'] = self.name.to_json()
        if self.password is not None:
            result['password'] = self.password
        if self.passwordChangeRequired is not None:
            result['passwordChangeRequired'] = str(self.passwordChangeRequired)
        if self.position is not None:
            result['position'] = self.position
        if self.timezone is not None:
            result['timezone'] = self.timezone
        return result


@dataclass
class Ya360UserCreationParams:
    departmentId: str
    name: Ya360UserName
    nickname: str
    password: str
    about: str = None
    birthday: str = None
    contacts: list[Ya360UserContactParams] = None
    displayName: str = None
    externalId: str = None
    gender: str = None
    isAdmin: bool = None
    language: str = None
    passwordChangeRequired: bool = None
    position: str = None
    timezone: str = None

    def __init__(self,
                 departmentId: str,
                 name: Ya360UserName,
                 nickname: str = None,
                 password: str = None,
                 about: str = None,
                 birthday: str = None,
                 contacts: list[Ya360UserContactParams] = None,
                 displayName: str = None,
                 externalId: str = None,
                 gender: str = None,
                 isAdmin: bool = None,
                 language: str = None,
                 passwordChangeRequired: bool = None,
                 position: str = None,
                 timezone: str = None,
                 ):
        self.departmentId = departmentId
        self.name = name
        for symbol in nickname:
            if symbol not in self.allowed_nickname_symbols():
                raise Ya360Exception(
                    message=f'Invalid symbol \"{symbol}\" in new user nickname',
                )
        self.nickname = nickname
        for symbol in password:
            if symbol not in self.allowed_password_symbols():
                raise Ya360Exception(
                    message=f'Invalid symbol \"{symbol}\" in new user password',
                )
        self.password = password
        self.about = about
        self.birthday = birthday
        self.contacts = contacts
        self.displayName = displayName
        self.externalId = externalId
        self.gender = gender
        self.isAdmin = isAdmin
        self.language = language
        self.passwordChangeRequired = passwordChangeRequired
        self.position = position
        self.timezone = timezone

    def to_json(self) -> dict:
        result = dict()
        result['departmentId'] = self.departmentId
        result['name'] = self.name.to_json()
        result['nickname'] = self.nickname
        result['password'] = self.password
        if self.about is not None:
            result['about'] = self.about
        if self.birthday is not None:
            result['birthday'] = self.birthday
        if self.contacts is not None:
            result['contacts'] = [contact.to_json() for contact in self.contacts]
        if self.displayName is not None:
            result['displayName'] = self.displayName
        if self.externalId is not None:
            result['externalId'] = self.externalId
        if self.gender is not None:
            result['gender'] = self.gender
        if self.isAdmin is not None:
            result['isAdmin'] = str(self.isAdmin)
        if self.language is not None:
            result['language'] = self.language
        if self.passwordChangeRequired is not None:
            result['passwordChangeRequired'] = str(self.passwordChangeRequired)
        if self.position is not None:
            result['position'] = self.position
        if self.timezone is not None:
            result['timezone'] = self.timezone
        return result

    @staticmethod
    def allowed_password_symbols() -> str:
        return string.ascii_letters + string.digits + '!@#$%'

    @staticmethod
    def allowed_nickname_symbols() -> str:
        return string.ascii_letters + string.digits + '._'


@dataclass
class Ya360User2fa:
    has2fa: bool
    hasSecurityPhone: bool
    userId: str

    @staticmethod
    def from_json(data: dict) -> 'Ya360User2fa':
        return Ya360User2fa(
            has2fa=bool(data['has2fa']),
            hasSecurityPhone=bool(data['hasSecurityPhone']),
            userId=data['userId'],
        )


@dataclass
class Ya360DepartmentParams:
    name: str = None
    parentId: str = None
    label: str = None
    description: str = None
    externalId: str = None
    headId: str = None

    def __init__(self,
                 name: Optional[str] = None,
                 parentId: Optional[str] = None,
                 label: Optional[str] = None,
                 description: Optional[str] = None,
                 externalId: Optional[str] = None,
                 headId: Optional[str] = None):
        self.name = name
        self.parentId = parentId
        self.label = label
        self.description = description
        self.externalId = externalId
        self.headId = headId

    def to_json(self) -> dict:
        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.parentId is not None:
            result['parentId'] = self.parentId
        if self.label is not None:
            result['label'] = self.label
        if self.description is not None:
            result['description'] = self.description
        if self.externalId is not None:
            result['externalId'] = self.externalId
        if self.headId is not None:
            result['headId'] = self.headId
        return result


class Ya360GroupMemberGroupMemberType(enum.Enum):
    user = 'user'
    group = 'group'
    department = 'department'


@dataclass
class Ya360GroupMember:
    id: str
    type: str

    @staticmethod
    def from_json(data: dict):
        return Ya360GroupMember(
            id=data.get('id'),
            type=Ya360GroupMemberGroupMemberType.group.value if data.get(
                'type') == 'group' else Ya360GroupMemberGroupMemberType.department.value if data.get(
                'type') == 'department' else Ya360GroupMemberGroupMemberType.user.value
        )

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'type': self.type,
        }


@dataclass
class Ya360GroupParams:
    name: str = None
    adminsIds: list[str] = None
    description: str = None
    externalId: str = None
    label: str = None
    members: list[Ya360GroupMember] = None

    def __init__(self,
                 name: str = None,
                 adminsIds: Optional[list[str]] = None,
                 description: Optional[str] = None,
                 externalId: Optional[str] = None,
                 label: Optional[str] = None,
                 members: Optional[list[Ya360GroupMember]] = None):
        if name is None or label is None:
            raise Ya360Exception(
                message=f'Invalid parameters: name {name} or label {label}',
            )
        self.name = name
        self.adminsIds = adminsIds
        self.description = description
        self.externalId = externalId
        self.label = label
        self.members = members

    def to_json(self) -> dict:
        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.adminsIds is not None:
            result['adminsIds'] = self.adminsIds
        if self.description is not None:
            result['description'] = self.description
        if self.externalId is not None:
            result['externalId'] = self.externalId
        if self.label is not None:
            result['label'] = self.label
        if self.members is not None:
            result['members'] = [member.to_json() for member in self.members]
        return result


@dataclass
class Ya360ShortDepartment:
    id: str = None
    name: str = None
    membersCount: str = None

    def from_json(self, data: dict) -> 'Ya360ShortDepartment':
        if data.get('id') is not None:
            self.id = data['id']
        if data.get('name') is not None:
            self.name = data['name']
        if data.get('membersCount') is not None:
            self.membersCount = data['membersCount']


@dataclass
class Ya360ShortGroup:
    id: str = None
    name: str = None
    membersCount: str = None

    @staticmethod
    def from_json(data: dict) -> 'Ya360ShortGroup':
        return Ya360ShortGroup(
            id=data['id'] if data.get('id') is not None else None,
            name=data['name'] if data.get('name') is not None else None,
            membersCount=data['membersCount'] if data.get('membersCount') is not None else None,
        )


@dataclass
class Ya360ShortUser:
    avatarId: str = None
    departmentId: str = None
    email: str = None
    gender: str = None
    id: str = None
    name: Ya360UserName = None
    nickname: str = None
    position: str = None

    @staticmethod
    def from_json(data: dict):
        return Ya360ShortUser(
            avatarId=data.get('avatarId'),
            departmentId=data.get('departmentId'),
            email=data.get('email'),
            gender=data.get('gender'),
            id=data.get('id'),
            name=Ya360UserName.from_json(data.get('name')),
            nickname=data.get('nickname'),
            position=data.get('position'),
        )


@dataclass
class Ya360ShortGroupMembers:
    departments: list[Ya360ShortDepartment] = None
    groups: list[Ya360ShortGroup] = None
    users: list[Ya360ShortUser] = None

    @staticmethod
    def from_json(data: dict) -> 'Ya360ShortGroupMembers':
        departments = None
        groups = None
        users = None
        if data.get('departments') is not None:
            departments = data.get('departments')
        if data.get('groups') is not None:
            groups = data.get('groups')
        if data.get('users') is not None:
            users = data.get('users')
        return Ya360ShortGroupMembers(
            departments=[Ya360ShortDepartment.from_json(department) for department in departments],
            groups=[Ya360ShortGroup.from_json(group) for group in groups],
            users=[Ya360ShortUser.from_json(user) for user in users],
        )
