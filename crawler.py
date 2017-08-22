#!/usr/bin/env python
#-*-coding:utf8-*-

import requests
import re,os
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

    def set_params(self, *words):

        self.keywords = words

    def start(self):

        s = requests.session()
        url = ""
        if len(self.keywords) == 1:
            url = self.link_prefix+self.keywords[0]
        response = os.popen("phantomjs.exe pinterest.js " + url).read()

        tree = html.fromstring(response)
        total_pin = tree.xpath('//div[@class="_tw _2k"]//div[@class = "GrowthUnauthPin_brioPin"]')
        total_img = tree.xpath('//div[@class="_tw _2k"]//img/@src')
        no_img = len(total_img)

        txt = open(self.output_dir + 'caption.txt', 'a')

        for i in range(0, no_img):
            print "Now processing image " + str(self.id) + ".\n"
            # image saved
            img_url = total_img[i]
            img_ori_url = re.sub(r'236x', 'originals', img_url)
            img = s.get(img_ori_url)
            file_img = self.output_dir + str(self.id) + '.jpg'
            img_write = open(file_img, 'wb')
            img_write.write(img.content)
            img_write.close()

            # txt saved
            text = total_pin[i].xpath('.//p/text()')

            if len(text)>=1:
                txt.write(str(self.id)+' '+ text[0].encode('utf-8') + '\n')
            else:
                txt.write(str(self.id) + ' None\n')
            self.id += 1

        txt.close()

if __name__ == "__main__":

    pinterest = Crawler("result/")
    pinterest.set_params("obama")
    pinterest.start()





