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
import sys
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


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

async def login(page,user,pwd):
    await page.goto(url)
    time.sleep(random.uniform(0,0.3)+2)
    #asyncio.sleep(2)

    await page.type('#loginForm > div > div:nth-child(1) > div > label > input', user)
    await page.type('#loginForm > div > div:nth-child(2) > div > label > input', pwd)
    await page.click('#loginForm > div > div:nth-child(3) > button')
    time.sleep(random.uniform(0,0.3)+5)
    #asyncio.sleep(5)
#    [button] = await page.xpath("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div")
#    await button.click()
#    time.sleep(random.uniform(0,0.3)+3)
#    await page.screenshot({'path':'example3.png'})

    return


async def next_img(page, button,cnt):
    if button is None:
        if cnt==0:
            print("single image detected")
            time.sleep(2)
        print("cannot find the button")
        return -1
    else:
        await button.click()  # indirectly cause a navigation
        time.sleep(0.1)
        return cnt+1

async def download_img_from_link(browser,user, name_prefix, link,cnt):
    #print(link,cnt)
    img_name = name_prefix+"%d"%(cnt) 
    dst ="./%s/%s.png"%(user,img_name)
    if not os.path.exists(dst):
        dl_page = await browser.newPage()
        viewSource = await dl_page.goto(link)
        with open(dst,mode="wb") as f:
            f.write(await viewSource.buffer())
        time.sleep(random.uniform(0,0.3)+2)
        #asyncio.sleep(1)
        await dl_page.close()
#    aagv = dict('div ._aamm  div ._aagv img')
#    for i in aagv:
#        print(pq(i).attr('src'))
        #print(aagv[-1].attr['src'])

async def download_a_post(browser,page,user,post_link,interval, image_links):
    target_link = url+user+post_link
    post_link_ = post_link.replace("/","")
    post_link_ = post_link_.strip()
    if post_link.find("reel")!=-1:
        return image_links

    print("current:",post_link_)
    await page.goto(target_link)
    cnt = 0
    while cnt>=0:
        time.sleep(random.uniform(0,0.3)+4)
        #asyncio.sleep(4)
        #d = pq(await page.content())
        elms = await page.JJ('div ._aagv img')
        for i,elm in enumerate(elms):
            link = await page.evaluate('elm => elm.getAttribute("src")',elm)
            if cnt==0 and i==0:
                image_links.append(link)
                await download_img_from_link(browser,user,post_link_,link,cnt)
                break
            elif cnt!=0 and i==1:
                image_links.append(link)
                await download_img_from_link(browser,user,post_link_,link,cnt)
                break

        button=await page.querySelector("button[aria-label='Next']") 
        cnt = await next_img(page, button,cnt)

        #else:
        #    print("file %s exist"%(dst))
    return image_links


async def to_target_user_page(page, user,interval):
    url1 = url+user
    await page.goto(url1)

#    await asyncio.gather(page.goto(url1),page.waitForNavigation())
    await page.screenshot({'path':'%s.png'%(user)})
    
    return 

async def scroll_n(page, n):
    for i in range(0,n+1):
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        time.sleep(random.uniform(0,0.3)+3)

async def get_user_post_links(browser, page, user, max_scroll=5):
    post_links = defaultdict(list)

    #for num in range(0,max_scroll):
    cnt =0
    need_update = 0
    image_links=[]
    while True:
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        print("scrolling ", cnt, "retrying",need_update)
        time.sleep(random.uniform(0,0.3)+5)
        #scn_name='%s_scroll_%d.png'%(target_user[0],cnt)
        #await page.screenshot({'path':scn_name})
        need_update+=1

        els = await page.JJ("div[class^='_aabd _aa8k  _al3l'] a")
        for el in els:
            link = await page.evaluate('el => el.getAttribute("href")', el)
            if link not in post_links:
                post_links[link] = link
                #image_links = await download_a_post(browser,page,target_user[0],link,5,image_links)
                need_update = 0
        cnt+=1
        if need_update >3:
            break
    
    if user:
        with open("./%s/post_links.txt"%(user),"w") as f:
            for i in post_links:
                print(i, file=f)

    return post_links

async def get_links_from_txt(path):
    lines=[]
    with open(path) as f:
        lines = f.readlines()
    
    return lines
    
#target_user = ["ikechan0920","akarin__rin","chacch1","hinako_sano","reina.sano017","kasumi_arimura.official","lucawanglu","hime._.gram","risa_s_lisa","chacch1","risa_s_lisa","bijo_navi","shakira","kasumi_arimura.official"]
target_user = ["ikechan0920","mogmog_yukappy","katoyuridayo","akarin__rin"]

async def main(arg):
    browser = await launch(headless=arg.headless)
    #browser = await launch({'headless':arg.headless, 'args': ["--proxy-server=173.177.85.227:80"]})
    page = await browser.newPage()
    await page.setUserAgent(user_agent)

    t_user = arg.user
    path = "./%s/post_links.txt"%(t_user)
    if(arg.islogin):
        await login(page,user,pwd)
    else:
        if not os.path.exists(path):
            await login(page,user,pwd)

    await to_target_user_page(page,t_user,2)
    num = 0
    os.makedirs("./%s"%(t_user), exist_ok=True)
    image_links =[]

    #while True:
    if not os.path.exists(path):
        post_links = await get_user_post_links(browser, page,t_user,max_scroll=5)
    else:
        post_links = await get_links_from_txt(path)

    for link in post_links:
        image_links = await download_a_post(browser,page,t_user,link,5,image_links)


    await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--user",type=str)
    parser.add_argument("--headless",type=int)
    parser.add_argument("--islogin",type=int, default=0)
    args = parser.parse_args()


    asyncio.get_event_loop().run_until_complete(main(args))
