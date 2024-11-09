import os
import glob
import asyncio

from itertools import cycle

from pyrogram import Client
from better_proxy import Proxy

from bot.config import settings
from bot.core.tapper import run_tapper
from bot.utils.logger import logger
from bot.utils.payload import check_payload_server
from bot.utils.proxy_utils_v2 import create_tg_client_proxy_pairs

start_text = """
██████╗ ██╗     ██╗   ██╗███╗   ███╗████████╗ ██████╗ ██████╗  ██████╗ ████████╗
██╔══██╗██║     ██║   ██║████╗ ████║╚══██╔══╝██╔════╝ ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║     ██║   ██║██╔████╔██║   ██║   ██║  ███╗██████╔╝██║   ██║   ██║   
██╔══██╗██║     ██║   ██║██║╚██╔╝██║   ██║   ██║   ██║██╔══██╗██║   ██║   ██║   
██████╔╝███████╗╚██████╔╝██║ ╚═╝ ██║   ██║   ╚██████╔╝██████╔╝╚██████╔╝   ██║   
╚═════╝ ╚══════╝ ╚═════╝ ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝   
"""


def get_session_names() -> list[str]:
    session_names = sorted(glob.glob("sessions/*.session"))
    session_names = [
        os.path.splitext(os.path.basename(file))[0] for file in session_names
    ]

    return session_names


def get_proxies() -> list[Proxy]:
    proxies = []
    if settings.USE_PROXY_FROM_FILE:
        with open(file="bot/config/proxies.txt", encoding="utf-8-sig") as file:
            for line in file:
                if "type://" in line:
                    continue
                try:
                    proxies.append(Proxy.from_str(proxy=line.strip()))
                except ValueError as e:
                    print(f"{e} - {line}")
    return proxies


def get_tg_clients() -> list[Client]:

    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")

    if not settings.API_ID or not settings.API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    tg_clients = [
        Client(
            name=session_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            workdir="sessions/",
            plugins=dict(root="bot/plugins"),
        )
        for session_name in session_names
    ]

    return tg_clients

async def run_tasks():
    tg_clients = get_tg_clients()
    client_proxy_list = create_tg_client_proxy_pairs(tg_clients)
    loop = asyncio.get_event_loop()

    if settings.USE_CUSTOM_PAYLOAD_SERVER and not await check_payload_server(settings.CUSTOM_PAYLOAD_SERVER_URL, full_test=True):
        logger.warning(
            f"The payload server on {settings.CUSTOM_PAYLOAD_SERVER_URL} is unavailable or not running. "
            f"<y>Without it, the bot will not play games for passes.</y> \n"
            f"<r>Read info</r>: https://github.com/HiddenCodeDevs/BlumTelegramBot/blob/main/PAYLOAD-SERVER.MD"
        )

    tasks = [
        loop.create_task(
            run_tapper(
                tg_client=pair[0],
                proxy=pair[1]
            )
        )
        for pair in client_proxy_list
    ]

    await asyncio.gather(*tasks)
