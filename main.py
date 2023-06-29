import requests
import random
import threading

proxy_list_url = "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"
proxies = []
proxy_index = 0

def fetch_proxy_list():
    global proxies
    response = requests.get(proxy_list_url)
    proxies = response.text.splitlines()

def get_next_proxy():
    global proxy_index
    if proxy_index >= len(proxies):
        proxy_index = 0
    proxy = proxies[proxy_index]
    proxy_index += 1
    return proxy

def send_request():
    while True:
        proxy = get_next_proxy()
        proxy_dict = {
            'http': proxy
        }
        try:
            response = requests.post(
                "https://example.com",
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:110.0) Gecko/20100101 Firefox/110.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br"
                },
                proxies=proxy_dict,
                data={
                    "example": "example",
                    "example": "example"
                }
            )
            if response.status_code == 200:
                print("Sent!")
            if response.status_code == 403:
                print("Failed!")
        except:
            pass

if __name__ == "__main__":
    fetch_proxy_list()
    threads = []
    num_threads = 200

    for _ in range(num_threads):
        thread = threading.Thread(target=send_request)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
