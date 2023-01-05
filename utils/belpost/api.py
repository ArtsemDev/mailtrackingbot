from http import HTTPStatus

from aiohttp import ClientSession


async def check_belpost(track_number: str) -> dict:
    async with ClientSession(base_url='https://api.belpost.by') as session:
        response = await session.post(
            url='/api/v1/tracking',
            json={'number': track_number}
        )
        if response.status == HTTPStatus.OK:
            return await response.json()
