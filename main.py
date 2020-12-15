# This is a sample Python script.
import requests
import threading
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 업비트 공지 Api
url = "https://api-manager.upbit.com/api/v1/notices?page=1&per_page=1&thread_name=general"
response = requests.get(url).json()
prevNotice = response["data"]["list"][0]["title"]
print(prevNotice)

# 업비트 주문 Api 관련
access_key = "chQbtJe49WewX7tetGlov530aKlCPZPe9FjwkRj9"
secret_key = "om4xx0INRaF5klX93INVsSZu6bTl647OFuBeNr1U"
server_url = "https://api.upbit.com"


def NoticeTimer():
    try:
        global prevNotice
        newNotice = requests.get(url=url).json()["data"]["list"][0]["title"]
        if prevNotice != newNotice:
            prevNotice = newNotice
            print("New Notice : " + newNotice)
            if "[거래] 원화 마켓 디지털 자산 추가" in newNotice:
                coinName = newNotice.split(" ")[7].replace(")", "")
                print("코인 이름 : " + coinName)
                BuyCoin(coinName)
    finally:
        threading.Timer(0.5, NoticeTimer).start()


def BuyCoin(coinName):
    query = {
        'market': 'BTC-' + coinName,
        'side': 'bid',
        'price': '0.0025',
        'ord_type': 'price'
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(res.json())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    NoticeTimer()
