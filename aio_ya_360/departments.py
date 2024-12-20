from dataclasses import dataclass
from typing import Optional

from . import AioYa360Client
from .base import Ya360Url, Ya360RequestParams, Ya360DepartmentParams
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
                    url=Ya360Url.departments(org_id=org_id),
                    params=params if params is not None else Ya360RequestParams()
                )
            except Ya360Exception:
                return None
            for response in resp:
                for user in response.get('departments'):
                    departments_list.append(Ya360Department.from_json(user))
            return departments_list

    @staticmethod
    async def create_department(client: AioYa360Client,
                                org_id: str,
                                params: Ya360DepartmentParams
                                ) -> Optional['Ya360Department']:
        if params.name is None or params.name == "" or params.label is None or params.label == "" or params.parentId is None or params.parentId == "":
            raise Ya360Exception('Name or label or parentId for new department is empty')
        try:
            return Ya360Department.from_json(
                await client.fetch_post(
                    url=Ya360Url.departments(org_id=org_id),
                    params=params.to_json()
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def delete_department(client: AioYa360Client,
                                org_id: str,
                                department_id: str
                                ) -> Optional[bool]:
        try:
            return (await client.fetch_delete(
                url=Ya360Url.department(org_id=org_id, department_id=department_id)
            )).get('removed')
        except Ya360Exception:
            return False

    @staticmethod
    async def edit_department(client: AioYa360Client,
                              org_id: str,
                              department_id: str,
                              params: Ya360DepartmentParams
                              ) -> Optional['Ya360Department']:
        try:
            return Ya360Department.from_json(
                await client.fetch_patch(
                    url=Ya360Url.department(org_id=org_id,
                                            department_id=department_id),
                    params=params.to_json()
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def add_alias(client: AioYa360Client,
                        org_id: str,
                        department_id: str,
                        alias: str) -> Optional['Ya360Department']:
        try:
            return Ya360Department.from_json(
                await client.fetch_patch(
                    url=Ya360Url.department_aliases(org_id=org_id,
                                                    department_id=department_id),
                    params={
                        'alias': alias
                    }
                )
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def delete_alias(client: AioYa360Client,
                           org_id: str,
                           department_id: str,
                           alias: str) -> Optional[bool]:
        try:
            return (await client.fetch_delete(
                url=Ya360Url.department_alias(org_id=org_id, department_id=department_id, alias=alias)
            )).get('removed')
        except Ya360Exception:
            return False
