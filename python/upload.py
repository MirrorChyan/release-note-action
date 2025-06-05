import sys
import time
from aiohttp import ClientSession
from datetime import datetime
import asyncio


def log(msg: object) -> None:
    print(f"{datetime.now()} | {msg}")


async def upload(rid: str, data: dict, headers: dict) -> bool:
    log("start upload")

    # step 1
    async with ClientSession() as session:
        async with session.put(
            f"https://dev.mirrorchyan.com/api/resources/{rid}/versions/release-note",
            headers=headers,
            data=data,
        ) as response:

            log(f"step 1: {response.status}")

            if response.status != 200:
                log(f"step 1 failed: {response.status}, {await response.text()}")
                return False

            log("uploaded")
            return True


async def main():
    _, rid, token, body_file = sys.argv

    headers = {
        "Authorization": token,
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }

    with open(body_file, "r", encoding="utf-8") as file:
        data = json.loadsfile.read()

    log(data)

    done = False
    retries = 3
    for i in range(retries):
        if await upload(rid, data, headers):
            done = True
            break
        elif i + 1 < retries:
            delay = (i + 1) * 15
            log(f"retry {i + 1} after {delay}s")
            time.sleep(delay)

    if not done:
        log("failed")
        sys.exit(1)

    log("done")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
