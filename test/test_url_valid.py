import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.exceptions import InsecureRequestWarning
import requests


urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
PROXY = {
    "http":  "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}

URLS:list[dict] = []
URL_STATUS:list[dict] = []
LOCK = threading.Lock()


def check_with_old_ssl(url):
    ctx = create_urllib3_context()
    ctx.load_default_certs()
    ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT

    with urllib3.PoolManager(ssl_context=ctx) as http:
        r = http.request("GET", url,headers=headers)
        return r.status

def check_url_smart(url, timeout=5):
    global headers
    print(f'check:{url}')

    # 直连
    try:
        r = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers=headers,
            verify=False
        )
        if r.status_code :
            return {
                "url": url,
                "ok": True,
                "via": "direct",
                "status": r.status_code
            }
        direct_error = f"status_{r.status_code}"

    except requests.RequestException as e:
        direct_error = str(e)
        if "UNSAFE_LEGACY_RENEGOTIATION_DISABLED" in direct_error:
            status = check_with_old_ssl(url)
            if status < 400:
                return {
                    "url": url,
                    "ok": True,
                    "via": "direct",
                    "status": status
                }


    # 2. 代理
    try:
        r = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers=headers,
            proxies=PROXY,
            verify=False
        )
        return {
            "url": url,
            "ok": r.status_code,
            "via": "proxy",
            "status": r.status_code,
            "direct_error": direct_error
        }

    except requests.RequestException as e:
        return {
            "url": url,
            "ok": False,
            "via": "proxy",
            "error": str(e),
            "direct_error": direct_error
        }

def worker(item:dict):
    item_t = item.copy()
    result_lst = []
    for i in range(3):
        result = check_url_smart(item_t['l'])
        print(result)
        result_lst.append(result)


    item_t['ok'] = any(i.get('ok') is True for i in result_lst)
    item_t['via'] = 'direct' if any(i.get('via') == 'direct' for i in result_lst) else 'proxy'

    # 仅写共享数据时加锁
    with LOCK:
        URL_STATUS.append(item_t)


def check_urls(urls, max_workers=10) -> None:
    start = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, url) for url in urls]

        for _ in as_completed(futures):
            pass

    print(f"Finished {len(urls)} URLs in {time.time() - start:.2f}s")

def load_urls(json_value:dict) -> None:
    global URLS
    for title_key in json_value['TitleList']:
        lst = json_value[title_key]['list']
        for i in lst:
            if i['y'] == 1:
                URLS.append(i)
    print(f'load urls success:{len(URLS)}')

def analysis():
    print(f'All: {len(URLS)}')
    print(f'Has Checked:{len(URL_STATUS)}')
    ERR = []
    for item in URL_STATUS:
        if item['ok'] == False:
            ERR.append(item)
    if len(ERR):
        print(len(ERR))
        for url in ERR:
            print(url)
        print('-'*51)
        print('Please Check it on yourself.')
    else:
        print('No Error')


def main() -> None:
    global URLS
    print('Load from file')
    try:
        with open('../src/webindexdb.json','r',encoding='utf-8') as f:
            j:dict = json.loads(f.read())
    except:
        print('Load file Error')
        return None
    print('Load Json File successful')

    load_urls(j)

    assert len(URLS) > 0

    check_urls(URLS)

    analysis()


if __name__ == '__main__':
    main()