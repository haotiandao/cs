import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
from requests.exceptions import Timeout
eventlet.monkey_patch()
channels = []
headers={'User-Agent': 'okhttp/3.12.10(Linux;Android9;V2049ABuild/TP1A.220624.014;wv)AppleWebKit/537.36(KHTML,likeGecko)Version/4.0Chrome/116.0.0.0MobileSafari/537.36'}
# 初始化计数器为0
counter = 0
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter
    
with open("ip_qianxin.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                channels.append((channel_name, channel_url))
    file.close()
    
def get_redirected_urls(url_list):
    session = requests.Session()
    if '#' not in url_list:
        response = session.head(url_list, allow_redirects=False, timeout=2)
        if response.status_code == 200 and 'Location' in response.headers:
            # 处理初始请求返回200但之后服务器又发出302重定向的情况
            redirected_url = response.headers['Location']
            print("1:----------------------------------------------------")
            print(f"Initial URL: {channel_url}, Redirected URL: {redirected_url}")

        elif response.status_code in [301, 302, 303, 307, 308]:
            # 处理直接重定向的情况
            redirected_url = response.headers['Location']
            print("2:----------------------------------------------------")
            print(f"Redirected URL: {redirected_url}")
        else:
            # 对于其他状态码，你可以选择打印或忽略
            print(f"Response Status Code: {response.status_code}")

for url in channels:
    channel_name, channel_url = url
    get_redirected_urls(channel_url)
    time.sleep(1)
