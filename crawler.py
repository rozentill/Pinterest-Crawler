#!/usr/bin/env python
#-*-coding:utf8-*-

import requests
import re
import  time
from lxml import html

class Crawler(object):

    def __init__(self, output_dir):

        self.link_prefix = "https://www.pinterest.com/search/pins/?q="
        self.link_host = "https://www.pinterest.com"
        self.link_postfix1 = "&rs=rs&eq=&etslf=1847&term_meta[]="
        self.link_postfix2 = "%7Crecentsearch%7Cundefined"
        # self.no = search_no
        self.output_dir = output_dir
        self.cookies = {}
        self.id = 0
    def set_keywords(self, *words):
        self.keywords = words

    def start(self):

        f = open(r'cookie.txt', 'r')
        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            self.cookies[name] = value  # 为字典cookies添加内容
        f.close()
        if len(self.keywords) == 1:
            url = self.link_prefix+self.keywords[0] +self.link_postfix1+self.keywords[0]+self.link_postfix2
        s = requests.session()

        myparams = {
            "data":'{"options":{"filter":"all","field_set_key":"board_picker","allow_stale":true,"from":"app"},"context":{}}',
            "_": "1503306350484"
        }

        myheaders ={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch, br",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control":"max-age=0",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
        }

        response = s.get(url,cookies = self.cookies, headers = myheaders,params = myparams)
        tree = html.fromstring(response.text)
        total_href = tree.xpath('//div[@class="pinWrapper none"]//a[@class = "pinLink pinImageWrapper"]/@href')
        total_img = tree.xpath('//div[@class="pinWrapper none"]//img/@src')

        no = len(total_href)

        txt = open(self.output_dir + 'caption.txt','a')

        for i in range(0,no):
            print "Now processing image "+ str(self.id)+".\n"
            #image saved
            img_url = total_img[i]
            img_ori_url = re.sub(r'236x', 'originals', img_url)
            img = s.get(img_ori_url)
            file_img = self.output_dir + str(self.id) + '.jpg'
            img_write = open(file_img, 'wb')
            img_write.write(img.content)
            img_write.close()

            #txt saved
            href_url = self.link_host + total_href[i]
            response_href = s.get(href_url, cookies=self.cookies, headers=myheaders)
            tree_href = html.fromstring(response_href.text)
            comment = tree_href.xpath('//div[@class = "_sx _sw _sy _so _5k _sq _ns _nt _nu _nv"]//span/text()')
            # print comment
            if len(comment)>=1:
                txt.write(str(self.id)+' '+ comment[0].encode('utf-8') + '\n')
            else:
                txt.write(str(self.id) + ' None\n')
            self.id += 1

        txt.close()
if __name__ == "__main__":

    pinterest = Crawler("result/")
    pinterest.set_keywords("obama")
    pinterest.start()





