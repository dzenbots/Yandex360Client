import asyncio
import os
import ssl
from typing import Union, Optional

import aiohttp
import certifi
from aiohttp import ClientSession

from .request_params import Ya360RequestParams
from .secrets import Ya360ClientSecrets
from .token import TokenData
from ..exceptions import Ya360Exception


class AioYa360Client:
    base_url = 'https://api360.yandex.net/'
    _access_token: Optional[str] = None
    _client_secrets: Optional[Ya360ClientSecrets] = None
    _token_data: Optional[TokenData] = None
    _config_file_name: Optional[str] = None

    def __init__(self,
                 base_url: str = None,
                 client_secrets: Ya360ClientSecrets = None,
                 config_file_name: Optional[str] = 'aio_ya_360.ini',
                 ):
        if base_url is not None:
            self.base_url = base_url
        if client_secrets is not None:
            self._client_secrets = client_secrets
        self._config_file_name = config_file_name

    @property
    def access_token(self):
        if self._token_data is not None:
            return self._token_data.access_token

    async def start(self) -> Union[str, None]:
        if os.path.exists(path=self._config_file_name):
            self._client_secrets = Ya360ClientSecrets.from_config(self._config_file_name)
            self._token_data = TokenData.from_config(self._config_file_name)
        else:
            if self._client_secrets is None:
                raise Ya360Exception(message='No client secret provided.')
            else:
                self._client_secrets.save_to_config(self._config_file_name)
        resp = None
        async with ClientSession(
                connector=aiohttp.TCPConnector(
                    ssl=ssl.create_default_context(
                        cafile=certifi.where()
                    )
                )
        ) as _session:
            if self._token_data is None:
                if self._client_secrets.verification_code == '':
                    await _session.close()
                    raise Ya360Exception(
                        f"""
    
            AIOYa360Client.start_work. No verification code provided.
            Verification code is required. You can achieve it by authorizing at 'https://oauth.yandex.ru/authorize?response_type=code&client_id=<your Client ID>'
            Link for you is 'https://oauth.yandex.ru/authorize?response_type=code&client_id={self._client_secrets.client_id}'
    
            Receive the verification code and put it in `{self._config_file_name}` file next to client_id and client_secret.
    
                         """
                    )
                async with _session.post(
                        url='https://oauth.yandex.ru/token',
                        headers={
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        data={
                            'grant_type': 'authorization_code',
                            'code': self._client_secrets.verification_code,
                            'client_id': self._client_secrets.client_id,
                            'client_secret': self._client_secrets.client_secret,
                        }
                ) as response:
                    if response.status != 200:
                        raise Ya360Exception(
                            message=f"""
                AioYa360.start_session Invalid client secrets.
                API Error description: {await response.json()}
                            """
                        )
                    resp = await response.json()
            else:
                async with _session.post(
                        url='https://oauth.yandex.ru/token',
                        headers={
                            'Content-type': 'application/x-www-form-urlencoded',
                        },
                        data={
                            'grant_type': 'refresh_token',
                            'refresh_token': self._token_data.refresh_token,
                            'client_id': self._client_secrets.client_id,
                            'client_secret': self._client_secrets.client_secret,
                        }
                ) as response:
                    if response.status != 200:
                        raise Ya360Exception(
                            message=f"""
                AioYa360.start_session Invalid token data. Try to achieve new token by 
                1. Deleting {self._config_file_name} 
                2. Remove parameter `verification_code` from ClientSecrets
                3. Restart the program.
    
                API Error description: {await response.json()}
                            """
                        )
                    resp = await response.json()
        if resp is None:
            raise Ya360Exception(
                message='AioYa360.start_session Unable to work with current parameters'
            )
        self._token_data = TokenData.from_json(resp)
        self._token_data.save_to_config(config_file_name=self._config_file_name)
        if self._token_data.access_token is not None:
            self._access_token = self._token_data.access_token
        return self._access_token is not None

    async def fetch_get(self,
                        url: str,
                        params: Optional[Ya360RequestParams] = None
                        ) -> Optional[list[dict]]:

        async def inner_get(inner_url: str, inner_params: Optional[Ya360RequestParams] = None):

            async with ClientSession(
                    base_url=self.base_url,
                    connector=aiohttp.TCPConnector(
                        ssl=ssl.create_default_context(
                            cafile=certifi.where()
                        )
                    ),
                    headers={
                        'Authorization': f'OAuth {self.access_token}',
                    }
            ) as session:
                async with session.get(
                        url=inner_url,
                        params=inner_params.to_json() if inner_params is not None else None
                ) as resp:
                    if resp.status != 200:
                        raise Ya360Exception(
                            message=f"""
                Error in request to API.
                URL: {inner_url}
                Method: GET
                params: {inner_params.to_json() if inner_params is not None else ""}
                                """
                        )
                    return await resp.json()

        if params is not None:
            if params.page is not None and params.per_page is not None:
                pages = (await inner_get(inner_url=url, inner_params=params)).get('pages')
                try:
                    responses = await asyncio.gather(
                        *[
                            inner_get(
                                inner_url=url,
                                inner_params=Ya360RequestParams(
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
                except Ya360Exception:
                    return list()
                return list(responses)
            else:
                try:
                    response = await inner_get(inner_url=url, inner_params=params)
                except Ya360Exception:
                    return list()
                return [response]
        else:
            try:
                response = await inner_get(inner_url=url, inner_params=params)
            except Ya360Exception:
                return list()
            return [response]

    async def fetch_patch(self,
                          url: str,
                          params: dict
                          ) -> Optional[dict]:
        async with ClientSession(
                base_url=self.base_url,
                connector=aiohttp.TCPConnector(
                    ssl=ssl.create_default_context(
                        cafile=certifi.where()
                    )
                ),
                headers={
                    'Authorization': f'OAuth {self.access_token}',
                }
        ) as session:
            async with session.patch(
                    url=url,
                    params=params
            ) as resp:
                if resp.status != 200:
                    raise Ya360Exception(
                        message=f"""
            Error in request to API.
            URL: {url}
            Method: PATCH
            params: {params}
                            """
                    )
                return await resp.json()

    async def fetch_put(self,
                        url: str,
                        params: dict
                        ) -> Optional[dict]:
        async with ClientSession(
                base_url=self.base_url,
                connector=aiohttp.TCPConnector(
                    ssl=ssl.create_default_context(
                        cafile=certifi.where()
                    )
                ),
                headers={
                    'Authorization': f'OAuth {self.access_token}',
                }
        ) as session:
            async with session.put(
                    url=url,
                    params=params
            ) as resp:
                if resp.status != 200:
                    raise Ya360Exception(
                        message=f"""
            Error in request to API.
            URL: {url}
            Method: PUT
            params: {params}
                            """
                    )
                return await resp.json()

    async def fetch_delete(self,
                           url: str
                           ) -> Optional[dict]:
        async with ClientSession(
                base_url=self.base_url,
                connector=aiohttp.TCPConnector(
                    ssl=ssl.create_default_context(
                        cafile=certifi.where()
                    )
                ),
                headers={
                    'Authorization': f'OAuth {self.access_token}',
                }
        ) as session:
            async with session.delete(
                    url=url
            ) as resp:
                if resp.status != 200:
                    raise Ya360Exception(
                        message=f"""
            Error in request to API.
            URL: {url}
            Method: DELETE
                            """
                    )
                return await resp.json()

    async def fetch_post(self,
                         url: str,
                         params: dict
                         ) -> Optional[dict]:
        async with ClientSession(
                base_url=self.base_url,
                connector=aiohttp.TCPConnector(
                    ssl=ssl.create_default_context(
                        cafile=certifi.where()
                    )
                ),
                headers={
                    'Authorization': f'OAuth {self.access_token}',
                }
        ) as session:
            async with session.post(
                    url=url,
                    json=params
            ) as resp:
                if resp.status != 200:
                    print(await resp.json())
                    raise Ya360Exception(
                        message=f"""
            Error in request to API.
            URL: {url}
            Method: POST
            params: {params}
                            """
                    )
                return await resp.json()
