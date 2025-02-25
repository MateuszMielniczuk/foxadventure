#!/usr/bin/python3

# script to update list of passengers to csv file
# get list of passengers from bokun API and update csv file


import base64
import hmac
import os
from datetime import datetime
from hashlib import sha1

import httpx
from dotenv import load_dotenv

# get list of passengers from Bokun API
load_dotenv()
url = "https://api.bokun.io"
path = "/activity.json/active-ids"
date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

http_method = "GET"

access_key = os.getenv("bokun_access_key")
if not access_key:
    raise ValueError("Access key cannot be null")
secret_key = os.getenv("bokun_secret_key")
if not secret_key:
    raise ValueError("Secret key cannot be null")

concaten_str = date_now + access_key + http_method + path


signature = hmac.new(
    bytes(secret_key, "utf-8"),
    msg=bytes(concaten_str, "utf-8"),
    digestmod=sha1,
)

signature_base64 = base64.b64encode(signature.digest()).decode()
print(concaten_str)
print(secret_key)
print(signature_base64)

response = httpx.request(
    method="GET",
    url=url + path,
    timeout=5,
    headers={
        "accept": "application/json",
        "X-Bokun-Date": date_now,
        "X-Bokun-AccessKey": access_key,
        "X-Bokun-Signature": signature_base64,
    },
)

print(response.status_code)
print(response.json())
