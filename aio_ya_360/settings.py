from typing import Optional

from . import AioYa360Client, Ya360SenderInfo
from .base import Ya360Url
from .exceptions import Ya360Exception


class Ya360Settings:

    @staticmethod
    async def get_sender_info(client: AioYa360Client,
                              org_id: str,
                              user_id: str) -> Optional[Ya360SenderInfo]:
        try:
            return Ya360SenderInfo.from_json(
                data=(await client.fetch_get(
                    url=Ya360Url.sender_info(
                        org_id=org_id,
                        user_id=user_id,
                    )
                ))[0]
            )
        except Ya360Exception:
            return None

    @staticmethod
    async def edit_sender_info(client: AioYa360Client,
                               org_id: str,
                               user_id: str,
                               sender_info: Ya360SenderInfo) -> Optional[Ya360SenderInfo]:
        try:
            return Ya360SenderInfo.from_json(
                data=(await client.fetch_post(
                    url=Ya360Url.sender_info(
                        org_id=org_id,
                        user_id=user_id,
                    ),
                    params=sender_info.to_json()
                ))
            )
        except Ya360Exception:
            return None
