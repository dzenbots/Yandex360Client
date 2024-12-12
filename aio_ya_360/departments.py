from dataclasses import dataclass
from typing import Optional

from . import AioYa360Client
from .base import Ya360Url, Ya360RequestParams
from .exceptions import Ya360Exception


@dataclass
class Ya360Department:
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
    def from_json(data: dict) -> 'Ya360Department':
        return Ya360Department(
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

    @staticmethod
    async def from_api(client: AioYa360Client,
                       org_id: str,
                       department_ids: Optional[list[str]] = None,
                       params: Optional[Ya360RequestParams] = None
                       ) -> Optional[list['Ya360Department']]:
        if department_ids is not None:
            return [
                Ya360Department.from_json(
                    (await client.fetch_get(
                        url=Ya360Url.department(
                            org_id=org_id,
                            department_id=department_id
                        ),
                    ))[0]
                ) for department_id in department_ids
            ]
        else:
            departments_list = []
            try:
                resp = await client.fetch_get(
                    url=Ya360Url.department_list(org_id=org_id),
                    params=params if params is not None else Ya360RequestParams()
                )
            except Ya360Exception:
                return None
            for response in resp:
                for user in response.get('departments'):
                    departments_list.append(Ya360Department.from_json(user))
            return departments_list
