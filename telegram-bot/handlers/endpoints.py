import aiohttp

from loguru import logger

timeout = aiohttp.ClientTimeout(total=600)


@logger.catch
async def check_user_register(data):
    url = ""
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=data, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()
