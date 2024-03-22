import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
from bs4 import BeautifulSoup
from queue import Queue
import threading

# 判断首位是否为数字，是返回真
def is_first_digit(s):
    return s[0].isdigit() if s else False
    
lock = threading.Lock()
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
urls = [
    "http://tonkiang.us/hoteliptv.php?page=1&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=2&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=3&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=4&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=5&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=6&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=7&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=8&s=凤凰",
    "http://tonkiang.us/hoteliptv.php?page=1&s=翡翠",
    "http://tonkiang.us/hoteliptv.php?page=1&s=汕头",
    "http://tonkiang.us/hoteliptv.php?page=2&s=汕头",
    "http://tonkiang.us/hoteliptv.php?page=1&s=IPTV",
    "http://tonkiang.us/hoteliptv.php?page=2&s=IPTV",
    "http://tonkiang.us/hoteliptv.php?page=3&s=IPTV",
    "http://tonkiang.us/hoteliptv.php?page=4&s=IPTV",
    "http://tonkiang.us/hoteliptv.php?page=5&s=IPTV",
    "http://tonkiang.us/hoteliptv.php?page=6&s=IPTV",
    "http://tonkiang.us/hoteliptv.php?page=1&s=电信",
    "http://tonkiang.us/hoteliptv.php?page=2&s=电信",
    "http://tonkiang.us/hoteliptv.php?page=3&s=电信",
    "http://tonkiang.us/hoteliptv.php?page=4&s=电信",
    "http://tonkiang.us/hoteliptv.php?page=5&s=电信",
    "http://tonkiang.us/hoteliptv.php?page=1&s=TVB",
    "http://tonkiang.us/hoteliptv.php?page=2&s=TVB",
    "http://tonkiang.us/hoteliptv.php?page=3&s=TVB",
    "http://tonkiang.us/hoteliptv.php?page=4&s=TVB"
    ]
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)  # 10秒后超时
    # 设置脚本执行超时
    driver.set_script_timeout(50)  # 5秒后超时
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(20)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()
    print(increment_counter())    #方便看看是否有执行啊
    # 查找所有符合指定格式的网址
    pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    # urls = list(set(urls_all))  # 去重得到唯一的URL列表
    urls_y = set(urls_all)  # 去重得到唯一的URL列表
    for urlv in urls_y:
        resultslist.append(f"{urlv}")

resultslist = set(resultslist)    # 去重得到唯一的URL列表

with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
    
sorted_list = sorted(resultslist)

def worker(thread_url,counter_id):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=selenium{counter_id}")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时
        driver.set_page_load_timeout(60)  # 10秒后超时
     
        # 设置脚本执行超时
        driver.set_script_timeout(50)  # 5秒后超时
        # 使用WebDriver访问网页
        if is_odd_or_even(random.randint(1, 200)):
            page_url= f"http://tonkiang.us/9dlist2.php?s={thread_url}"
        else:
            page_url= f"http://foodieguide.com/iptvsearch/alllist.php?s={thread_url}"
        
        print(page_url)
        driver.get(page_url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tables_div = soup.find("div", class_="tables")
        results = (
            tables_div.find_all("div", class_="result")
            if tables_div
            else []
        )
        if not any(
            result.find("div", class_="m3u8") for result in results
        ):
            #break
            print("Err-------------------------------------------------------------------------------------------------------")
        for result in results:
            #print(result)
            m3u8_div = result.find("div", class_="m3u8")
            url_int = m3u8_div.text.strip() if m3u8_div else None
            #取频道名称
            m3u8_name_div = result.find("div", class_="channel")
            url_name = m3u8_name_div.text.strip() if m3u8_div else None
            #－－－－－
            #print("-------------------------------------------------------------------------------------------------------")
            name =f"{url_name}"
            if len(name) == 0:
                name = "Err画中画"
            #print(name)
            urlsp =f"{url_int}"
            if len(urlsp) == 0:
                urlsp = "rtp://127.0.0.1"             
            print(f"{url_name}\t{url_int}")
            #print("-------------------------------------------------------------------------------------------------------")
            urlsp = urlsp.replace("http://67.211.73.118:9901", "")
            name = name.replace("cctv", "CCTV")
            name = name.replace("中央", "CCTV")
            name = name.replace("央视", "CCTV")
            name = name.replace("高清", "")
            name = name.replace("超高", "")
            name = name.replace("HD", "")
            name = name.replace("标清", "")
            name = name.replace("频道", "")
            name = name.replace("-", "")
            name = name.replace(" ", "")
            name = name.replace("PLUS", "+")
            name = name.replace("＋", "+")
            name = name.replace("(", "")
            name = name.replace(")", "")
            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
            name = name.replace("CCTV1综合", "CCTV1")
            name = name.replace("CCTV2财经", "CCTV2")
            name = name.replace("CCTV3综艺", "CCTV3")
            name = name.replace("CCTV4国际", "CCTV4")
            name = name.replace("CCTV4中文国际", "CCTV4")
            name = name.replace("CCTV4欧洲", "CCTV4")
            name = name.replace("CCTV5体育", "CCTV5")
            name = name.replace("CCTV6电影", "CCTV6")
            name = name.replace("CCTV7军事", "CCTV7")
            name = name.replace("CCTV7军农", "CCTV7")
            name = name.replace("CCTV7农业", "CCTV7")
            name = name.replace("CCTV7国防军事", "CCTV7")
            name = name.replace("CCTV8电视剧", "CCTV8")
            name = name.replace("CCTV9记录", "CCTV9")
            name = name.replace("CCTV9纪录", "CCTV9")
            name = name.replace("CCTV10科教", "CCTV10")
            name = name.replace("CCTV11戏曲", "CCTV11")
            name = name.replace("CCTV12社会与法", "CCTV12")
            name = name.replace("CCTV13新闻", "CCTV13")
            name = name.replace("CCTV新闻", "CCTV13")
            name = name.replace("CCTV14少儿", "CCTV14")
            name = name.replace("CCTV15音乐", "CCTV15")
            name = name.replace("CCTV16奥林匹克", "CCTV16")
            name = name.replace("CCTV17农业农村", "CCTV17")
            name = name.replace("CCTV17农业", "CCTV17")
            name = name.replace("CCTV5+体育赛视", "CCTV5+")
            name = name.replace("CCTV5+体育赛事", "CCTV5+")
            name = name.replace("CCTV5+体育", "CCTV5+")
            name = name.replace("CMIPTV", "")
            name = name.replace("内蒙卫视", "内蒙古卫视")
            name = name.replace("CCTVCCTV", "CCTV")
            if "http" in urlsp:
                # 获取锁
                lock.acquire()
                infoList.append(f"{name},{urlsp}")
                # 释放锁
                lock.release()
        print(f"=========================>>> Thread {thread_url} save ok")
    except Exception as e:
        print(f"=========================>>> Thread {thread_url} caught an exception: {e}")
    finally:
        # 确保线程结束时关闭WebDriver实例
        driver.quit() 
        print(f"=========================>>> Thread {thread_url}  quiting")
        # 标记任务完成
        time.sleep(0)

# 创建一个线程池，限制最大线程数为3
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 提交任务到线程池，并传入参数
    counter = increment_counter()
    for i in sorted_list:  # 假设有5个任务需要执行
        executor.submit(worker, i ,counter)

infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("myitv.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        print(info)
    file.close()

# 收集其他人接口数据源
urls = [
    "https://raw.githubusercontent.com/taijichadao/tv/main/itvlist.txt",
    "http://api.mcqq.cn/tvbox/zhibo.php",
    "http://tvbox.nx66.bf:99/tvbox/zhibo.php",
    "http://mywlkj.ddns.net:754/tv.php",
    "https://raw.gitcode.com/lionzang/TV/raw/main/channel.txt"
    ]

file_contents = []
for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(60)  # 10秒后超时
    # 设置脚本执行超时
    driver.set_script_timeout(50)  # 5秒后超时
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(5)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()
    # print(page_content)    #方便看看是否有执行啊
    file_contents.append(page_content)
    
with open("iptv_all.txt", "w", encoding="utf-8") as output:
    output.write('\n'.join(file_contents))
    output.close()
print("---------------------------------------------------------")
results = []
with open("iptv_all.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                name =(f"{channel_name}")
                name = name.replace("「新疆」", "")
                name = name.replace("「代理」", "")
                name = name.replace("「IPV6」", "")
                name = name.replace("「移动」", "")
                name = name.replace("「官方」", "")
                name = name.replace("「电信」", "")
                name = name.replace("「联通」", "")
                name = name.replace("「河北有线」", "")
                name = name.replace("「北方广电」", "")
                name = name.replace("「辽宁联通」", "")
                name = name.replace("1920*1080", "")
                print(f"{name},{channel_url}")
                urlright = channel_url[:4]
                if urlright == 'http':
                    if "[" not in channel_url:
                        if '画中画' not in channel_name and '单音' not in channel_name and '直播' not in channel_name and '测试' not in channel_name and '主视' not in channel_name:
                            check_name = f"{name}"
                            if not is_first_digit(check_name):
                                results.append(f"{name},{channel_url}")

results = set(results)  # 去重得到唯一的URL列表
results = sorted(results)
with open("iptv_new_all.txt", 'w', encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")
        # print(result)
    file.close()
