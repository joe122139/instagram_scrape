import asyncio
from pyppeteer import launch
import random
import time
import io,sys,os
import filecmp

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


div_class="_aagv"
target_user = ["hinako_sano","hime._.gram","risa_s_lisa","chacch1","risa_s_lisa","bijo_navi","shakira","kasumi_arimura.official"]
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


user = "abc@hotmail.com"
pwd = "pwd"

async def login(page,user,pwd):
    await page.goto(url)
    time.sleep(1)
    await page.screenshot({'path':'example.png'})
    await page.type('#loginForm > div > div:nth-child(1) > div > label > input', user)
    await page.type('#loginForm > div > div:nth-child(2) > div > label > input', pwd)
    await page.click('#loginForm > div > div:nth-child(3) > button')

    time.sleep(5)
    await page.screenshot({'path':'example2.png'})
    [button] = await page.xpath("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div")
    await button.click()
    time.sleep(3)
    await page.screenshot({'path':'example3.png'})

    return

async def download_img(page, links,path,interval):
    for it in links:
        filename = links[it][0]
        dst ="./%s/%s.png"%(path,filename)

        if not os.path.exists(dst):
            viewSource = await page.goto(it)
            with open(dst,mode="wb") as f:
                f.write(await viewSource.buffer())
            time.sleep(interval)
        else:
            print("file %s exist"%(dst))


async def to_target_user_page(page, user):
    url1 = url+user
    await page.goto(url1)
    time.sleep(2)
    await page.screenshot({'path':'%s.png'%(user)})
    
    return 


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.setUserAgent(user_agent)

    await login(page,user,pwd)
    await to_target_user_page(page,target_user[0])

    num = 0
    os.makedirs("./%s"%(target_user[0]), exist_ok=True)
    from collections import defaultdict
    import hashlib
    link_dict = defaultdict(list)

    while True:
    #for num in range(0,20):
        await page.evaluate('window.scrollBy(0, window.innerHeight)')
        time.sleep(2.5)
        scn_name='%s_scroll_%d.png'%(target_user[0],num)
        await page.screenshot({'path':scn_name})
        #check end

        if(num>=2):
            scn_name_pre='%s_scroll_%d.png'%(target_user[0],num-1)
            scn_name_prepre='%s_scroll_%d.png'%(target_user[0],num-2)
            if filecmp.cmp(scn_name,scn_name_pre) and filecmp.cmp(scn_name,scn_name_prepre):
                print("scrolling to the bottom")
                break

#        with open("log_%s_%d.html"%(target_user[0],num),mode="w", encoding="utf-8") as f:
#            f.write(await page.content())
        elms = await page.JJ("._aagv > img")

        for elm in elms:
            link = await page.evaluate('elm => elm.getAttribute("src")',elm)
            txt = await page.evaluate('elm => elm.getAttribute("alt")',elm)
            if txt is None:
                txt = link
            hash_txt = hashlib.sha1(txt.encode("utf-8")).hexdigest()

            if link not in link_dict:
                link_dict[link].append(hash_txt)
        num+=1


    print(num,link_dict)
    await download_img(page, link_dict, target_user[0],0.5)


#    with open("log_%s_final.html"%(target_user[0]),mode="w", encoding="utf-8") as f:
#        f.write(await page.content())
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

