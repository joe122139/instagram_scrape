import asyncio
from pyppeteer import launch
import random
import time
import io,sys,os
import filecmp
import copy
import hashlib
from collections import defaultdict
from collections import OrderedDict
from pyquery import PyQuery as pq
from inst_scrape import to_target_user_page,login, get_user_post_links
import re


#target_user = ["weekly_spa_","gr_youngjump_official"]
target_user = ["gr_youngjump_official"]
target_user = ["weekly_spa_"]
target_user = ["shupure_official"]
user_list = ["gr_youngjump_official","weekly_spa_","shupure_official"]
url = 'http://www.instagram.com/'

user_agent =random.choice([
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
             ])


user = "user"
pwd = "pwd"

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.setUserAgent(user_agent)

    await login(page,user,pwd)

    #for t_user in target_user:
    user_dict = OrderedDict()
    name_list = []
    for user_name in user_list:
        with open("%s_user_links.txt"%(user_name),"r", encoding="utf-8") as f:
            name_list = f.readlines()
    
        for line in name_list:
            if line not in user_dict:
                user_dict[line.strip()] = [0,0]
    


    


    user_cnt=0
    for user_name in user_dict:
        await to_target_user_page(page,user_name,2)
        time.sleep(7+random.random())
        dic = pq(await page.content())

        #elms = await page.JJ("._ac2a")
        elms  = dic('._ac2a')
        info = [0,0]
        for i,el in enumerate(elms.items()):
            if i<2:
                info[i] = int(el.text().replace(',',''))
                user_dict[user_name] = info
                #titles = await page.evaluate('el => el.getAttribute("title")', el)
        user_cnt+=1

    with open("all_user_list_w_post_followers.txt", "w", encoding='utf-8') as f:
        for it in user_dict:
            print(it," %d %d"%(user_dict[it][0], user_dict[it][1]), file=f)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

