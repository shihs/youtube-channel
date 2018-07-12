# -*- coding: utf-8 -*-
# 使用 selenium 抓取 youtube 關鍵字搜尋頻道結果 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import urllib
import math
import csv


def get_youtube_channel(keyword):

    # 打開瀏覽器
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/results?search_query=" + urllib.quote(keyword) + "&sp=EgIQAkIECAESAA%253D%253D")
    
    # 搜尋結果數量
    count = driver.find_element_by_id("result-count").text.encode("utf-8")
    count = int(count.split(" ")[1])
    # 估計需要 scroll 的次數
    count = int(math.ceil((count/10)-2))
    # 捲動頁面
    for i in range(1, count):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")    
        time.sleep(1)
    
    time.sleep(5)
    
    # 儲存資料 list    
    data = []
    data.append(["channel", "url", "facebook", "subscriber"])
    # 已完整展開的頁面
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    # parse 頁面
    for i in soup.select("ytd-channel-renderer"):
        # 頻道頁面
        channel_url = "https://www.youtube.com" + i.select(".yt-simple-endpoint")[0]["href"].strip() + "/about"
        channel_name = i.select("span")[0].text.encode("big5", "ignore").strip()
        print channel_url 
        channel_driver = webdriver.Chrome()
        channel_driver.get(channel_url)
        channel_soup = BeautifulSoup(channel_driver.page_source, "html.parser")
        # facebook link
        try:
            channel_facebook = ""
            for link in channel_soup.select("#links-holder")[0].select("a"):
                
                if "facebook" in link["href"]:
                    channel_facebook = link["href"]
                    break
        except:
            channel_facebook = ""
        # subscribe count
        try:    
            channel_subscriber = channel_soup.select("#subscriber-count")[0].text.encode("utf-8")
            if channel_subscriber == "":
                channel_subscriber = "0" 
        except:
            channel_subscriber = "0"
        
        data.append([channel_name, channel_url, channel_facebook, channel_subscriber])
        
        
        channel_driver.close()
        time.sleep(.5)
        print 
        
    return data
    



def save_file(data):

    with open("test.csv", "wb") as f:
        w = csv.writer(f)
        w.writerows(data)



if __name__ == '__main__':
    data = get_youtube_channel("旅行")
    
    # 刪除「訂閱人數」，只保留數字
    for i in range(1, len(data)):
        print data[i][3]
        if data[i][3] != "0" or data[i][3] != 0:
            data[i][3] = data[i][3].split("：")[1]

    save_file(data)



