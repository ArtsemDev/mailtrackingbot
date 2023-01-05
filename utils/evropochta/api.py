from http import HTTPStatus

from aiohttp import ClientSession
from fake_useragent import UserAgent


async def check_evropochta(track_number: str) -> dict:
    async with ClientSession(base_url='https://evropochta.by') as session:
        response = await session.get(
            url='/api/track.json/',
            params={'number': track_number},
            headers={'User-Agent': UserAgent().random}
        )
        if response.status == HTTPStatus.OK:
            return await response.json()
