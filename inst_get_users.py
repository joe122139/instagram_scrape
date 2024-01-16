import asyncio
from pyppeteer import launch
import random
import time
import io,sys,os
import filecmp
import copy
import hashlib
from collections import defaultdict
from pyquery import PyQuery as pq
from inst_scrape import to_target_user_page,login, get_user_post_links
import re


#target_user = ["weekly_spa_","gr_youngjump_official"]
target_user = ["gr_youngjump_official"]
target_user = ["weekly_spa_"]
target_user = ["shupure_official"]
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


user = "joe122139@hotmail.com"
#user = "joe122139@gmail.com"
pwd = "Joezjb17!!"
#pwd = "Joezjb17!"

async def get_user_home_link(page,home_user):
    from collections import defaultdict
    import hashlib
    user_sets = defaultdict(list)

    #for num in range(0,max_scroll):
    cnt =0
    need_update = 0
    time.sleep(random.uniform(0,0.3)+1)

    while True:
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        print("scrolling ", cnt, "retrying",need_update)
        time.sleep(random.uniform(0,0.5)+5)
        #scn_name='%s_scroll_%d.png'%(target_user[0],cnt)
        #await page.screenshot({'path':scn_name})
        need_update+=1

        #els = await page.JJ("div[class^='_aabd _aa8k  _al3l'] a")
        els = await page.JJ("div ._aagv img")
        for el in els:
            user_descr = await page.evaluate('el => el.getAttribute("alt")', el)
            #users = re.findall(r'@(\S+)', user_descr)
            if user_descr is None:
                break
            users = re.findall(r'@([\w.-]*[^.,\\n)(])', user_descr)
            print(users)
            for user in users:
                user = user.strip()
                if user not in user_sets and home_user not in user:
                    user_sets[user] = user
                    need_update = 0
        if cnt%10==0:
            print(user_sets)
        cnt+=1
        if need_update >3:
            break
    
    return user_sets


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.setUserAgent(user_agent)

    await login(page,user,pwd)

    for t_user in target_user:
        await to_target_user_page(page,t_user,2)
    #
        user_sets = await get_user_home_link(page,t_user)
        with open("%s_user_links.txt"%(t_user),"w", encoding='utf-8') as f:
            for it in user_sets:
                print(it, file=f)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

