from dataclasses import dataclass
from typing import Optional

from . import AioYa360Client, Ya360Exception
from .base import Ya360GroupMember, Ya360Url, Ya360RequestParams


@dataclass
class Ya360Group:
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
    members: list[Ya360GroupMember]
    membersCount: str
    name: str
    removed: bool
    type: str

    @staticmethod
    def from_json(data: dict):
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
    async def from_api(client: AioYa360Client, org_id: str, group_ids: Optional[list[str]] = None) -> Optional[list]:
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
                    url=Ya360Url.groups_list(org_id=org_id),
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
    async def member_of_groups(client: AioYa360Client, org_id: str, user_id: str) -> Optional[list]:
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

