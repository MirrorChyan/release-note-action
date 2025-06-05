import sys
import time
import urllib3
import requests
from datetime import datetime

urllib3.disable_warnings()


def log(msg: object) -> None:
    print(f"{datetime.now()} | {msg}")


def upload(rid: str, data: dict, headers: dict) -> bool:
    log("start upload")

    # step 1
    response_1 = requests.put(
        f"https://mirrorchyan.com/api/resources/{rid}/versions/release-note",
        headers=headers,
        data=data,
        verify=False,
    )
    log(f"step 1: {response_1.status_code}")

    if response_1.status_code != 200:
        log(f"step 1 failed: {response_1.status_code}, {response_1.text}")
        return False

    log("uploaded")
    return True


def main():
    _, rid, token, body_file = sys.argv

    headers = {
        "Authorization": token,
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }

    with open(body_file, "r") as file:
        data = file.read()

    log(data)

    done = False
    retries = 3
    for i in range(retries):
        if upload(rid, json.loads(data), headers):
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
    main()
