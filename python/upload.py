import sys
import asyncio
import aiohttp
import json
from datetime import datetime


def log(msg: object) -> None:
    print(f"{datetime.now()} | {msg}")


async def upload(session: aiohttp.ClientSession, rid: str, data: dict, headers: dict) -> bool:
    log("start upload")
    url = f"https://mirrorchyan.com/api/resources/{rid}/versions/release-note"

    try:
        # 发送 PUT 请求
        async with session.put(
            url,
            headers=headers,
            json=data,
            ssl=False  # 等同于 requests 的 verify=False
        ) as response:
            log(f"step 1: {response.status}")
            
            if response.status != 200:
                text = await response.text()
                log(f"step 1 failed: {response.status}, {text}")
                return False
            
            log("uploaded")
            return True
            
    except Exception as e:
        log(f"Request failed: {str(e)}")
        return False


async def main():
    _, rid, token, body_file = sys.argv

    headers = {
        "Authorization": token.strip(),
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }

    with open(body_file, "r") as file:
        data = json.load(file)

    log(data)

    done = False
    retries = 3
    async with aiohttp.ClientSession() as session:
        for i in range(retries):
            if await upload(session, rid, data, headers):
                done = True
                break
            elif i + 1 < retries:
                delay = (i + 1) * 15
                log(f"retry {i + 1} after {delay}s")
                await asyncio.sleep(delay)

    if not done:
        log("failed")
        sys.exit(1)

    log("done")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
