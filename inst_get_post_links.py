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
from inst_scrape import get_user_post_links,to_target_user_page,login

target_user = ["lucawanglu","risa_s_lisa","chacch1","hinako_sano","reina.sano017","kasumi_arimura.official","hime._.gram","chacch1","risa_s_lisa","bijo_navi","shakira","kasumi_arimura.official"]
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


#user = "joe122139@hotmail.com"
user = "joe122139@gmail.com"
#pwd = "Joezjb17!!"
pwd = "Joezjb17!"

#target_user = ["ikechan0920","mogmog_yukappy","yui___2g","katoyuridayo","akarin__rin"]
target_user = ["yui___2g","akarin__rin"]

async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.setUserAgent(user_agent)

    await login(page,user,pwd)

    for t_user in target_user:
        await to_target_user_page(page,t_user,2)

        os.makedirs("./%s"%(t_user), exist_ok=True)

        #while True:
        path = "./%s/post_links.txt"%(t_user)
        if not os.path.exists(path):
            post_links = await get_user_post_links(browser, page,t_user,max_scroll=5)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

