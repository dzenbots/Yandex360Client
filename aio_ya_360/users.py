from dataclasses import dataclass
from typing import Optional

from .base import AioYa360Client, Ya360UserContact, Ya360UserName, Ya360Url, Ya360RequestParams, Ya360UserRequestParams
from .exceptions import Ya360Exception


@dataclass
class Ya360User:
    about: str
    aliases: list[str]
    avatarId: str
    birthday: str
    contacts: list[Ya360UserContact]
    createdAt: str
    departmentId: str
    email: str
    externalId: str
    gender: str
    groups: list[str]
    id: str
    isAdmin: bool
    isDismissed: str
    isEnabled: bool
    isRobot: bool
    language: str
    name: Ya360UserName
    nickname: str
    position: str
    timezone: str
    updatedAt: str

    @staticmethod
    def from_json(data: dict):
        return Ya360User(
            about=data.get('about'),
            aliases=data.get('aliases'),
            avatarId=data.get('avatarId'),
            birthday=data.get('birthday'),
            contacts=[Ya360UserContact.from_json(contact) for contact in data.get('contacts')],
            createdAt=data.get('createdAt'),
            departmentId=data.get('departmentID'),
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
            name=Ya360UserName.from_json(data.get('name')),
            nickname=data.get('nickname'),
            position=data.get('position'),
            timezone=data.get('timezone'),
            updatedAt=data.get('updatedAt'),
        )

    @staticmethod
    async def from_api(client: AioYa360Client, org_id: str, user_ids: Optional[list[str]] = None) -> Optional[list]:
        if user_ids is not None:
            return [
                Ya360User.from_json(
                    (await client.fetch_get(
                        url=Ya360Url.user(
                            org_id=org_id,
                            user_id=user_id
                        ),
                    ))[0]
                ) for user_id in user_ids
            ]
        else:
            users_list = []
            try:
                resp = await client.fetch_get(
                    url=Ya360Url.users_list(org_id=org_id),
                    params=Ya360RequestParams(
                        page=0,
                        per_page=10
                    )
                )
            except Ya360Exception:
                return None
            for response in resp:
                for user in response.get('users'):
                    users_list.append(Ya360User.from_json(user))
            return users_list

    @staticmethod
    async def edit_info(client: AioYa360Client, org_id: str, user_id: str, params: Ya360UserRequestParams):
        try:
            response = await client.fetch_patch(
                    url=Ya360Url.user(org_id=org_id, user_id=user_id),
                    params=params.to_json()
            )
            return Ya360User.from_json(response)
        except Ya360Exception:
            return None
