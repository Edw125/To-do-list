import aiohttp

from loguru import logger

timeout = aiohttp.ClientTimeout(total=600)


@logger.catch
async def get_access_token(data):
    url = "http://127.0.0.1:8000/api/v1/token/"
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=data, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()
