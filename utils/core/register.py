import pyrogram

from utils.core import logger
from data import settingsV2


async def create_sessions():
    while True:
        session_name = input('\nВведите название сессии (для выхода нажмите Enter):\nWrite a session name and '
                             'press enter: ')
        if not session_name: 
            return

        session = pyrogram.Client(
            api_id=settingsV2.API_ID,
            api_hash=settingsV2.API_HASH,
            name=session_name,
            workdir=settingsV2.WORKDIR,
        )

        async with session:
            user_data = await session.get_me()

        logger.success(f'Успешно добавлена сессия {user_data.username} | {user_data.phone_number}\n'
                       f'Session successful added for {user_data.username} | {user_data.phone_number}')
