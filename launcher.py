import asyncio
import json
from typing import Tuple
from better_proxy import Proxy
from pyrogram import Client
from utils.core import logger


def get_proxies_V2() -> json:
    proxies = None
    with open(file="proxies.json", encoding="utf-8-sig") as file:
        proxies = json.load(file)
        return proxies
    
async def get_proxy_with_client(accounts: list[str]) -> list[Tuple[Proxy, str]]:
    proxies = get_proxies_V2()

    proxy_with_client = []

    for account_name in accounts:
        proxy = proxies.get(account_name)
        if proxy:
            proxy = Proxy.from_str(proxy=proxy.strip())

            proxy_client_pair = (proxy, account_name)
            proxy_with_client.append(proxy_client_pair)
        else:
            logger.critical(f"Could not find proxy for session: {account_name.name}")
            exit(1)
    
    return proxy_with_client