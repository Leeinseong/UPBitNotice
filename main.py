# This is a sample Python script.
import requests
import threading
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import time
import datetime
import codecs
# 업비트 공지 Api
url = "http://api-manager.upbit.com/api/v1/notices?page=1&per_page=1&thread_name=general"
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
        print(datetime.datetime.now())
        if prevNotice != newNotice:

            # 파일출력
            now = datetime.datetime.now();
            fileName = str(now.year) + str(now.month) + str(now.day) + ".txt"
            print(fileName)
            f = codecs.open(fileName, 'a', 'utf-8')
            f.write(newNotice + "\n")
            f.close()

            prevNotice = newNotice
            #Case 1. [거래] 원화 마켓 디지털 자산 추가 (휴먼스케이프 HUM)
            #Case 2. [이벤트] 프로메테우스(PROM) 원화마켓 오픈 이벤트 : TOP 트레이딩 이벤트 /
            #Case 3. [거래]원화마켓 신규 상장 (샌드박스 SAND)            //Case 1. [거래] 원화 마켓 디지털 자산 추가 (휴먼스케이프 HUM)
            if "원화 마켓 디지털 자산 추가" in newNotice:
                coinName = newNotice.split(" ")[6].replace(")", "")
                print("코인 이름 : " + coinName)
                BuyCoin(coinName)
            if "원화마켓 오픈 이벤트" in newNotice:
                if( ("당첨 안내" not in newNotice) & ("종료" not in newNotice)):
                    coinName = newNotice.split(" ")[1].split("(")[1].replace(")", "")
                    print("코인 이름 : " + coinName)
                    BuyCoin(coinName)
            if "원화마켓 신규 상장" in newNotice:
                coinName = newNotice.split(" ")[5].replace(")", "")
                print("코인 이름 : " + coinName)
                BuyCoin(coinName)
    except requests.exceptions.ConnectionError:
        print("Connection refused by the server..")
        print(datetime.datetime.now())
        time.sleep(5)
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
