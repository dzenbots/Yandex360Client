from dataclasses import dataclass
from typing import Optional


@dataclass
class Ya360UserContact:
    alias: bool
    label: str
    main: bool
    synthetic: bool
    type: str
    value: str

    @staticmethod
    def from_json(data: dict):
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

    def to_json(self):
        result = dict()
        result['first'] = self.first
        result['last'] = self.last
        if self.middle is not None:
            result['middle'] = self.middle
        return result


@dataclass
class Ya360UserContactParams:
    type: str
    value: str
    label: Optional[str] = None

    def to_json(self):
        result = dict()
        result['type'] = self.type
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
