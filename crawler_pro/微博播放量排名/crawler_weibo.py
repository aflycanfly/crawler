import fake_useragent
import requests
import json
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import numpy as np
from datetime import datetime
import re


class Crawler:
    def __init__(self, cookie):
        self.headers = {
            'User-Agent': fake_useragent.UserAgent().random,
            'cookie': cookie
        }
        self.url = "https://weibo.com/ajax/statuses/searchProfile"

    def get_onepage(self, params):
        r = requests.get(url=self.url, params=params, headers=self.headers)
        r.encoding = 'utf-8'
        json_data = json.loads(r.text)
        return json_data

    def process_one_page(self, mydata):
        datas = []
        dist = {}
        for i in range(len(mydata["data"]["list"])):
            if mydata["data"]["list"][i]["text"].find("的微博视频") == -1:
                continue
            text_raw = mydata["data"]["list"][i]["text_raw"]
            title = text_raw.split('#', 1)[0]
            lable = ''.join(re.findall(r"#.*?#", text_raw))
            url = ''.join(re.findall(r'http://\S+', text_raw))
            created_at = mydata["data"]["list"][i]["created_at"]
            created_at = datetime.strptime(
                created_at, '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
            reposts_count = mydata["data"]["list"][i]["reposts_count"]
            comments_count = mydata["data"]["list"][i]["comments_count"]
            attitudes_count = mydata["data"]["list"][i]["attitudes_count"]
            online_users_number = mydata["data"]["list"][i]["page_info"]["media_info"]["online_users_number"]
            datas.append({
                "created_at": created_at,
                "title": title,
                "lable": lable,
                "url": url,
                "reposts_count": reposts_count,
                "comments_count": comments_count,
                "attitudes_count": attitudes_count,
                "online_users_number": online_users_number
            })
            
            
        return datas

    def craw_page(self, uid, number):
        params = {
            #  德国人Leo乐柏说 1104911015
            # 司徒建国Stu 2006222803
            'uid': uid,
            'page': number,
            'feature': 4,
            "starttime": 1609430400,
            "endtime": 1664553600
        }
        data_json = self.get_onepage(params)
        page_datas = self.process_one_page(data_json)
        return page_datas

    def save_to_excle(self, uid, excle_name):
        all_pages_datas = []
        for number in range(1, 15):
            all_pages_datas.extend(self.craw_page(uid, number))
        df = pd.DataFrame(all_pages_datas)
        # df 按照观看数排序
        df = df.sort_values(by="online_users_number", ascending=False)
        # df 转换为 excel
        df.to_excel("{}.xlsx".format(excle_name), index=False)


if __name__ == "__main__":
    '''
        6023864410 歪果仁研究协会
        5626136031 我是郭杰瑞
        5055109473 阿福Thomas
        5565691983 萌叔大卫老师
        5935300594 KatAndSid
        3771264361 功必扬 
        5854026101 Rachele瑞丽
        德国人Leo乐柏说 1104911015
        司徒建国Stu 2006222803
    '''
    cookie = 'SINAGLOBAL=6008923544490.623.1669600730018; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWh0Xsq1MAgxu2XAbnI-Sb55JpX5KMhUgL.Foqce0.4eK2X1K-2dJLoIEBLxK-L1h5L1-qLxKML1-BL1h5LxK-L1K2LB.BLxKnLB.qL1K5t; UOR=,,login.sina.com.cn; ULV=1678619453169:8:5:1:7351817887097.48.1678619452962:1678261498630; SCF=Ap2YMJwYeBXVWkX3383x4VI14durTT4lsVde7VL_sz4ywsxV7Jd7tJ4yjA4kDO5HEKhki79hdsJjELj9F_7Gozg.; SUB=_2A25JHBFUDeRhGeBI6FsY8S_IwjmIHXVqaAWcrDV8PUNbmtANLRjwkW9NRp7kGDhEQQd_w24UE_VdlRFzSuPNjSTi; ALF=1681911299; SSOLoginState=1679319300; PC_TOKEN=3bd4e2c9b2; XSRF-TOKEN=P7qjIF6DkD1zAyhSCJXxJmpz; WBPSESS=USfWtr-hzUv9dxm42OaQDLa7_1kqMNlxcjy8i3kHIdISf0sLPydmsc1APmCBGPvw_5NxjK2z5f-eonV3IUK80PzSFcZ7-cmhcDn04L8rX_S4civy6aXOPXoorETQ5gvHE12fbD4gkRSOeSbIAzu4Fw=='
    crawler = Crawler(cookie=cookie)
    uid = 2006222803
    name = "司徒建国Stu"
    crawler.save_to_excle(uid, name)
