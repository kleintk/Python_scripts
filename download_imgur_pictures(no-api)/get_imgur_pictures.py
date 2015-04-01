#!/usr/bin/python3

import requests
import shutil
import random
import hashlib
import time
import re
import sys
import math
import imghdr
import os


savepath = ""


def download_save_picture(imageurl, savepath, imagename):
    r = requests.get(imageurl, stream=True)
    with open(savepath + imagename, 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
    with open(savepath + imagename, 'rb') as in_file:
        if (imghdr.what(in_file) == 'gif'):
            os.rename(savepath + imagename, savepath + imagename[:32]+'.gif')
    del r


def generate_random_imagename():
    h = hashlib.md5()
    s = str(time.time()) + str(random.randint(0,99999))
    h.update(s.encode())
    return h.hexdigest() + ".jpg"


def find_all_imagelinks_in_imgurpage(url):
    r = requests.get(url)
    #inhalts_string = r.text.split('<div id="imagelist"')[1]
    #inhalts_string = inhalts_string.split('<div class="clear"></div>')[0]
    inhalts_string = r.text
    linkre = re.compile('//i.imgur.com/(.*)b.jpg')
    alle_linksre = re.findall(linkre, inhalts_string)
    alle_links = []
    for i in alle_linksre:
        alle_links.append("http://i.imgur.com/" + i + ".jpg")
    return alle_links


# main
if __name__ == "__main__":
    if (len(sys.argv) <= 2) or (len(sys.argv) >= 4):
        print("useage:\n" + sys.argv[0] + " url number_of_pics\n" + sys.argv[0] + " http://www.imgur.com/r/funny 75")
        sys.exit()
    
    if (len(sys.argv) == 3):
        url = sys.argv[1]
        imagequantity = int(sys.argv[2])
        pagequantity = math.ceil(imagequantity/60)
        
        links = find_all_imagelinks_in_imgurpage(url)
        for i in range(1, pagequantity):
            linkstmp = find_all_imagelinks_in_imgurpage(url+"/new/page/"+str(i)+"/hit?scrolled")
            links = links + linkstmp
        links = links[:imagequantity]
        print("[ ] downloading files:")
        for imageurl in links:
            download_save_picture(imageurl, savepath, generate_random_imagename() )
            #print(imageurl)
            print("+", end="", flush=True)
        print("\n[x] downloading files completed")


