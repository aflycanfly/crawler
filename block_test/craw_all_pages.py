import sys
import os
import requests
from bs4 import BeautifulSoup
from utils import url_manager
import re


if __name__ == "__main__":


    root_url = "http://www.crazyant.net/"
    #实例化一个url管理器
    urls = url_manager.UrlManager()
    #添加根url
    urls.add_new_url(root_url)
    #打开文件
    fout = open("./block_test/craw_all_pages.txt", "w", encoding="utf-8")
    while urls.has_new_url():
        cur_url = urls.get_url()
        r = requests.get(cur_url,timeout=10)
        if r.status_code != 200:
            raise Exception("request error status code:{}".format(r.status_code))
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find("title").text#获取title

        fout.write("%s\t%s\n"%(cur_url,title))
        fout.flush()#刷新缓存
        print("success: {} {} {}".format(cur_url,title,len(urls.new_urls)))#打印当前url title

        #获取当前页面的所有url
        links = soup.find_all("a")
        #获取所有的链接
        for link in links:
            href = link.get("href")
            if href is None:
                continue
            pattern = r"^http://www.crazyant.net/\d+.html$"
            if re.match(pattern, href):
                urls.add_new_url(href)#添加新的url