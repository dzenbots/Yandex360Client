from dataclasses import dataclass
from typing import Optional

from .base import AioYa360Client, Ya360UserContact, Ya360UserName, Ya360Url, Ya360RequestParams, Ya360UserRequestParams, \
    Ya360UserContactParams, Ya360UserCreationParams, Ya360User2fa
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
    def from_json(data: dict) -> 'Ya360User':
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
    async def from_api(client: AioYa360Client,
                       org_id: str,
                       user_ids: Optional[list[str]] = None
                       ) -> Optional[list['Ya360User']]:
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
                    url=Ya360Url.users(org_id=org_id),
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
    async def edit_info(client: AioYa360Client,
                        org_id: str,
                        user_id: str,
                        params: Ya360UserRequestParams
                        ) -> Optional['Ya360User']:
        try:
            return Ya360User.from_json(
                await client.fetch_patch(
                    url=Ya360Url.user(org_id=org_id, user_id=user_id),
                    params=params.to_json()
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def edit_user_contacts(client: AioYa360Client,
                                 org_id: str,
                                 user_id: str,
                                 contacts: list[Ya360UserContactParams]
                                 ) -> Optional['Ya360User']:
        try:
            return Ya360User.from_json(
                await client.fetch_put(
                    url=Ya360Url.user_contacts(org_id=org_id, user_id=user_id),
                    params={
                        'contacts': [
                            contact.to_json() for contact in contacts
                        ]
                    }
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def delete_user_contacts(client: AioYa360Client,
                                   org_id: str,
                                   user_id: str
                                   ) -> bool:
        try:
            await client.fetch_delete(
                url=Ya360Url.user_contacts(org_id=org_id, user_id=user_id)
            )
        except Ya360Exception:
            return False
        return True

    @staticmethod
    async def add_user(client: AioYa360Client,
                       org_id: str,
                       params: Ya360UserCreationParams
                       ) -> Optional['Ya360User']:
        if params.nickname in [
            user.nickname for user in await Ya360User.from_api(
                client=client,
                org_id=org_id
            )
        ]:
            raise Ya360Exception(
                message=f'User with nickname {params.nickname} is already exists'
            )
        try:
            return Ya360User.from_json(
                await client.fetch_post(
                    url=Ya360Url.users(org_id=org_id),
                    params=params.to_json()
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def user_2fa_status(client: AioYa360Client, org_id: str, user_id: str) -> Ya360User2fa:
        return Ya360User2fa.from_json(
            (await client.fetch_get(
                url=Ya360Url.user_2fa(org_id=org_id, user_id=user_id),
            ))[0]
        )

    @staticmethod
    async def user_2fa_reset(client: AioYa360Client, org_id: str, user_id: str) -> bool:
        try:
            await client.fetch_delete(
                url=Ya360Url.user_2fa(org_id=org_id, user_id=user_id)
            )
        except Ya360Exception:
            return False
        return True

    @staticmethod
    async def user_add_alias(client: AioYa360Client,
                             org_id: str,
                             user_id: str,
                             alias: str) -> Optional['Ya360User']:
        try:
            return Ya360User.from_json(
                await client.fetch_post(
                    url=Ya360Url.user_aliases(org_id=org_id, user_id=user_id),
                    params={
                        'alias': alias
                    }
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def user_delete_alias(client: AioYa360Client,
                                org_id: str,
                                user_id: str,
                                alias: str) -> Optional['Ya360User']:
        try:
            return Ya360User.from_json(
                await client.fetch_delete(
                    url=Ya360Url.user_aliases(org_id=org_id, user_id=user_id, alias=alias)
                )
            )
        except Ya360Exception:
            return None
