from dataclasses import dataclass
from typing import Union, Optional

from . import AioYa360Client
from .base import Ya360RequestParams
from .base import Ya360Url
from .exceptions import Ya360Exception


@dataclass
class Ya360Organization:
    id: str
    name: str
    email: str
    phone: str
    fax: str
    language: str
    subscriptionPlan: str

    @staticmethod
    def from_json(data: dict) -> 'Ya360Organization':
        return Ya360Organization(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            fax=data.get('fax'),
            language=data.get('language'),
            subscriptionPlan=data.get('subscriptionPlan')
        )

    @staticmethod
    async def from_api(client: AioYa360Client
                       ) -> Optional[list['Ya360Organization']]:
        await client.start()
        organization_list = []
        next_page_token = ''
        while True:
            try:
                resp = await client.fetch_get(
                    url=Ya360Url.organizations_list(),
                    params=Ya360RequestParams(
                        pageToken=next_page_token,
                        pageSize=10
                    )
                )
            except Ya360Exception:
                return None
            for response in resp:
                for organization in response.get('organizations'):
                    organization_list.append(Ya360Organization.from_json(organization))
                next_page_token = response.get('nextPageToken')
            if next_page_token == '':
                break
        return organization_list
