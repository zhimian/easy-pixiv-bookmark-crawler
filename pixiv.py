import requests
import threading
from bs4 import BeautifulSoup

# you may need a proxy :)
proxies = {
    'http': 'http://localhost:8001',
    'https': 'http://localhost:8001'
}

thread_num = 5      # default thread number

pid = 68889147      # pixiv artwork id
start = 1           # start page,include itself
end = 11            # end page,include itself
# 一页50人

# output file path
file_path = "./pid/%s.txt" % (pid)

# logined pixiv account's cookie
cookie = ""



url_prefix = "https://www.pixiv.net/bookmark_detail.php?illust_id=%s&p=" % str(pid)

header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "cookie": cookie,
    "dnt": "1",
    "referer": "https://www.pixiv.net/bookmark_detail.php",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}


def split_integer(m, n):
    assert n > 0
    quotient = int(m / n)
    remainder = m % n
    if remainder > 0:
        return [quotient] * (n - remainder) + [quotient + 1] * remainder
    if remainder < 0:
        return [quotient - 1] * -remainder + [quotient] * (n + remainder)
    return [quotient] * n


def fetch(start, end, num):
    string = ""
    for i in range(start, end):
        url = url_prefix + str(i)
        response1 = session.get(url, headers=header, proxies=proxies)
        soup = BeautifulSoup(response1.text, "lxml")
        ul = soup.find('ul', class_="bookmark-items")
        for li in ul.children:
            string += li.span.string + "," + \
                li.a["data-user_id"] + "," + li.a["data-user_name"] + "\n"
        print("page:%d" % i)
    with lock:
        merge[num] = string


merge = {}
threads = []
lock = threading.Lock()

f = open(file_path, "w", encoding='utf-8')
session = requests.session()

if end < start:
    print("end page shouldn't less than start page!!")
    exit()
works = split_integer(end-start+1, thread_num)
#print(works)

s = t = 1
for i in range(0, thread_num):
    s = t
    t = s + works[i]
    #print(s, t)
    th = threading.Thread(target=fetch, args=(s, t, i))
    th.start()
    threads.append(th)

for th in threads:
    th.join()

for i in range(0, thread_num):
    f.write(merge[i])
f.close()
print("Compelte!")

