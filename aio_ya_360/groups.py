import enum
from dataclasses import dataclass
from typing import Optional

from . import AioYa360Client
from .base import Ya360Url, Ya360RequestParams, Ya360GroupParams
from .base.shared_classes import Ya360GroupMember
from .exceptions import Ya360Exception


@dataclass
class Ya360Group:
    adminIds: list[str] = None
    aliases: list[str] = None
    authorId: str = None
    createdAt: str = None
    description: str = None
    email: str = None
    externalId: str = None
    id: str = None
    label: str = None
    memberOf: list[str] = None
    members: list[Ya360GroupMember] = None
    membersCount: str = None
    name: str = None
    removed: bool = None
    type: str = None

    @staticmethod
    def from_json(data: dict) -> 'Ya360Group':
        return Ya360Group(
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
            members=[Ya360GroupMember.from_json(member) for member in data.get('members')],
            membersCount=data.get('membersCount'),
            name=data.get('name'),
            removed=data.get('removed'),
            type=data.get('type'),
        )

    @staticmethod
    async def from_api(client: AioYa360Client,
                       org_id: str,
                       group_ids: Optional[list[str]] = None) -> Optional[list['Ya360Group']]:
        if group_ids is not None:
            return [
                Ya360Group.from_json(
                    (await client.fetch_get(
                        url=Ya360Url.group(
                            org_id=org_id,
                            group_id=group_id
                        ),
                    ))[0]
                ) for group_id in group_ids
            ]
        else:
            groups_list = []
            try:
                resp = await client.fetch_get(
                    url=Ya360Url.groups(org_id=org_id),
                    params=Ya360RequestParams(
                        page=0,
                        per_page=10
                    )
                )
            except Ya360Exception:
                return None
            for response in resp:
                for user in response.get('groups'):
                    groups_list.append(Ya360Group.from_json(user))
            return groups_list

    @staticmethod
    async def member_of_groups(client: AioYa360Client,
                               org_id: str,
                               user_id: str) -> Optional[list['Ya360Group']]:
        groups: list[Ya360Group] = await Ya360Group.from_api(client=client, org_id=org_id)
        current_groups: list[str] = []
        for group in groups:
            if user_id in [member.id for member in group.members]:
                current_groups.append(group.id)
        return (
            await Ya360Group.from_api(
                client=client,
                org_id=org_id,
                group_ids=current_groups
            )
        )

    @staticmethod
    async def create_group(client: AioYa360Client,
                           org_id: str,
                           params: Ya360GroupParams
                           ) -> Optional['Ya360Group']:
        try:
            return Ya360Group.from_json(
                await client.fetch_post(
                    url=Ya360Url.groups(
                        org_id=org_id,
                    ),
                    params=params.to_json()
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def delete_group(client: AioYa360Client,
                           org_id: str,
                           group_id: str) -> Optional[bool]:
        try:
            return (await client.fetch_delete(
                url=Ya360Url.group(org_id=org_id, group_id=group_id)
            )).get('removed')
        except Ya360Exception:
            return False

    @staticmethod
    async def edit_group(client: AioYa360Client,
                         org_id: str,
                         group_id: str,
                         params: Ya360GroupParams
                         ) -> Optional['Ya360Group']:
        try:
            return Ya360Group.from_json(
                await client.fetch_patch(
                    url=Ya360Url.group(
                        org_id=org_id,
                        group_id=group_id,
                    ),
                    params=params.to_json()
                )
            )
        except Ya360Exception:
            return None