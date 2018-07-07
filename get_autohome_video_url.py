import re
import time

import requests
from lxml import etree
from mytools import Mytools
import json

class Autohome:
    def __init__(self):
        # self.url = 'https://v.autohome.com.cn/u/19996353/#pvareaid=3454181'
        self.url = ['https://v.autohome.com.cn/user/pagedata/?userid=19996353&ordertype=1&pageIndex={}'.format(x) for x in range(1, 4)]
        self.base_url = 'https://v.autohome.com.cn'
        self.api_url = 'http://p-vp.autohome.com.cn/api/gpi?mid='
        self.headers = {
             'Accept': 'text/html, */*; q=0.01',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'zh',
             'Connection': 'keep-alive',
             'Content-Length': '0',
             'Cookie': '__ah_uuid=22D31507-F905-4134-9C51-0A6A82FF8FAD; fvlid=1530942885670cElC17gDLs; sessionip=222.210.137.75; sessionid=66276C68-AFE4-42F3-92C0-C9719D4D90F2%7C%7C2018-07-07+13%3A54%3A46.262%7C%7C0; area=510199; ahpau=1; isplaycontinue=1; sessionuid=66276C68-AFE4-42F3-92C0-C9719D4D90F2%7C%7C2018-07-07+13%3A54%3A46.262%7C%7C0; __utma=1.376309702.1530944720.1530944720.1530944720.1; __utmc=1; __utmz=1.1530944720.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); sessionvid=7601C786-5699-49CA-9FD2-54E72939E289; ahpvno=33; pvidchain=3454186,3454186,3454186,3454186,3454186,3454186,3454181,3454181,3454181,3454181; ref=0%7C0%7C0%7C0%7C2018-07-07+18%3A14%3A49.504%7C2018-07-07+13%3A54%3A46.262',
             'DNT': '1',
             'Host': 'v.autohome.com.cn',
             'Origin': 'https',
             'Referer': 'https',
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
             'X-Requested-With': 'XMLHttpRequest'}


    def get_page(self):
        for url in self.url:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                html = response.text
                html = etree.HTML(html)
                page_links = html.xpath('/html/body/ul/li/div[1]/a/@href')
                for link in page_links:
                    # time.sleep(2)
                    response = requests.get(self.base_url+link, headers=self.headers)
                    #currplayvid
                    if response.status_code == 200:
                        text = response.text
                        title = etree.HTML(text).xpath('/html/body/div[2]/div[1]/div[3]/h1/text()')
                        currplayvid = re.findall('var currplayvid = "(.*?)"', text)
                        if currplayvid  is not None:
                            video_json_url = self.api_url + currplayvid[0]
                            #json>result>media>qualities[3]
                            video_json = requests.get(video_json_url).text
                            video_json = json.loads(video_json, encoding='utf-8')

                            yield {
                                'video1080': video_json['result']['media']['qualities'][3]['copy'],
                                'videosd': video_json['result']['media']['qualities'][1]['copy'],
                                # 'title': video_json['result']['media']['info']['title']
                                'title': title[0]

                                   }



if __name__ == '__main__':
    a = Autohome()
    test = a.get_page()
    print(type(test))
    for i in test:
        print(i)

