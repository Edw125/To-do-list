import aiohttp

from loguru import logger

from init_bot import SERVER_HOST

timeout = aiohttp.ClientTimeout(total=600)


@logger.catch
async def get_access_token(data: dict) -> None | dict:
    url = f"{SERVER_HOST}/api/v1/token/"
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=data, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()


@logger.catch
async def get_task_list(jwt_token: str) -> None | dict:
    url = f"{SERVER_HOST}/api/v1/tasks/"
    headers = {"Authorization": "JWT " + jwt_token}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()


@logger.catch
async def check_user_register(creds: dict) -> None | dict:
    url = f"{SERVER_HOST}/api/v1/users/check_tg_user/"
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=creds, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()


@logger.catch
async def update_user_data(creds: dict, jwt_token: str) -> None | dict:
    url = f"{SERVER_HOST}/api/v1/users/update/"
    headers = {"Authorization": "JWT " + jwt_token}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.patch(url, data=creds, headers=headers, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()


@logger.catch
async def query_delete_task(number: str, jwt_token: str) -> None | bool:
    url = f"{SERVER_HOST}/api/v1/tasks/{number}/"
    headers = {"Authorization": "JWT " + jwt_token}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.delete(url, headers=headers, timeout=10) as response:
            if response.status == 204:
                return True


@logger.catch
async def query_create_task(data: dict, jwt_token: str) -> None | dict:
    url = f"{SERVER_HOST}/api/v1/tasks/"
    headers = {"Authorization": "JWT " + jwt_token}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, data=data, headers=headers, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()


@logger.catch
async def query_update_task(data: dict, jwt_token: str) -> None | dict:
    if not data.get('id'):
        return
    url = f"{SERVER_HOST}/api/v1/tasks/{data.get('id')}/"
    headers = {"Authorization": "JWT " + jwt_token}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.patch(url, data=data, headers=headers, timeout=10) as response:
            if response.status == 200 or response.status == 201:
                return await response.json()
