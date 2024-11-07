import asyncio
import http
import json
import time
import urllib
import webbrowser

import requests
import execjs
from mitmproxy import flow, ctx
from selenium.webdriver.chrome.service import Service
from pyppeteer import launch


url = "https://fanyi.baidu.com/"
url1 = "https://fanyi.baidu.com/?aldtype=85#en/zh/test"
url2 = 'https://fanyi.baidu.com/mtpe/user/getInfo?_='


async def main():
    browser = await launch(headless=True, dumpio=True, autoClose=False,
                           args=['--no-sandbox', '--window-size=1920,1080', '--disable-infobars'])   # 进入有头模式
    page = await browser.newPage()          # 打开新的标签页
    # await page.setViewport({'width': 1920, 'height': 1080})      # 页面大小一致

    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    # await page.screenshot({'path': './1.jpg'})   # 截图保存路径
    await page.goto(url) # 访问主页
    time.sleep(5)
    await page.reload()

    page_text = await page.content()   # 获取网页源码
    print(page_text)
    time.sleep(1)
    cookies = await page.cookies()
    for c in cookies:
        print(c['name']+':'+ c['value'])


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

def startBaiduTranslate(tarLan ='',msg ='我想回家',proxy = ''):
    # with open('res/sign.js', 'r', encoding='utf-8') as f:  # js文件
    #     sign = execjs.compile(f.read()).call("get", msg)
    # data = {
    #     "from": "auto",  # 要翻译的语种
    #     "to": tarLan,  # 翻译成的语种
    #     "query": msg,  # 要翻译的内容
    #     'transtype': 'translang',
    #     "simple_means_flag": "3",
    #     "sign": sign,
    #     "token": "b0739d656edf6192395f7f2648bdbbd5",
    #     "domain": "common"
    # }
    print(round(time.time() * 1000))
    proxies_wrap = {'http': proxy}

    try:
        r = requests.get(url=url2+str(round(time.time() * 1000)), headers=headers, proxies=proxies_wrap)
        print(r.headers['cookie'])
    except Exception as e:
        print(e.args[0])
    # finally:
        # return json['trans_result']['data'][0]['dst']
from selenium import webdriver


def get_cookie():
    data = {'username': 'xxx',
            'password': 'xxx'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', }
    session = requests.session()
    cookie_jar = session.post(url=url1, headers=headers).cookies
    cookie_t = requests.utils.dict_from_cookiejar(cookie_jar)
    return cookie_t

def getcookie1():
  Hostreferer = {
    #'Host':'***',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
  }
  #urllib或requests在打开https站点是会验证证书。 简单的处理办法是在get方法中加入verify参数，并设为False
  html = requests.get(url, headers=Hostreferer, verify=False)
  #获取cookie:DZSW_WSYYT_SESSIonID
  if html.status_code == 200:
    print(html.cookies)
    for cookie in html.cookies:
      print(cookie)


def job(url):
    injected_javascript = '''
    // overwrite the `languages` property to use a custom getter
    Object.defineProperty(navigator, "languages", {
      get: function() {
        return ["zh-CN","zh","zh-TW","en-US","en"];
      }
    });
    // Overwrite the `plugins` property to use a custom getter.
    Object.defineProperty(navigator, 'plugins', {
      get: () => [1, 2, 3, 4, 5],
    });
    // Pass the Webdriver test
    Object.defineProperty(navigator, 'webdriver', {
      get: () => false,
    });
    // Pass the Chrome Test.
    // We can mock this in as much depth as we need for the test.
    window.navigator.chrome = {
      runtime: {},
      // etc.
    };
    // Pass the Permissions Test.
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
      parameters.name === 'notifications' ?
        Promise.resolve({ state: Notification.permission }) :
        originalQuery(parameters)
    );
    '''
    # Only process 200 responses of HTML content.
    if not flow.response.status_code == 200:
        return
    # Inject a script tag containing the JavaScript.
    html = flow.response.text
    html = html.replace('<head>', '<head><script>%s</script>' % injected_javascript)
    flow.response.text = str(html)
    ctx.log.info('>>>> js代码插入成功 <<<<')

    # 只要url链接以target开头，则将网页内容替换为目前网址
    if flow.url.startswith(url):
        flow.response.text = flow.url
        print(flow.url)
    print(url)


if __name__ == '__main__':
    # job(url)
    # asyncio.get_event_loop().run_until_complete(main())  # 调用
    # startBaiduTranslate()
    # webbrowser_open = webbrowser.open(url1)
    # webbrowser_open.get(url1)
    # print(webbrowser_open)

    # opt = webdriver.ChromeOptions()  # 创建Chrome参数对象
    #
    # opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    #
    # opt.headless = True  # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
    #
    # t = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    #
    # driver = webdriver.Chrome(options=opt)  # 创建Chrome无界面对象
    # driver.get(url)
    # # requests库，构造会话
    # session = requests.Session()
    # # 获取cookies
    # cookies = driver.get_cookies()
    # # 填充
    # for cookie in cookies:
    #     session.cookies.set(cookie['name'], cookie['value'])
    #     print(cookie['name']+':'+ cookie['value'])

    # opt = webdriver.ChromeOptions()  # 创建Chrome参数对象
    #
    # opt.headless = True  # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
    #
    # driver = webdriver.Chrome(options=opt)  # 创建Chrome无界面对象
    # get = driver.get(url=url)
    # time.sleep(1)
    # driver.refresh()
    # time.sleep(4)
    #
    # cookie_list = driver.get_cookies()
    # # 格式化打印cookie
    # test = "123"
    # test1 = 'ss'
    #
    # # url = "https://fanyi.baidu.com/v2transapi"
    # ab_sr = ''
    # PSTM = ''
    # Hm_lvt = ''
    # Hm_lpvt = ''
    # BAIDUID_BFESS = ''
    # BAIDUID = ''
    #
    # cookie_tmp = ''
    # for cookie in cookie_list:
    #     cookie_tmp += cookie['name'] + '=' + cookie['value']+';'
    #     print(cookie['name'] + '=' + cookie['value']+';')
    #     if cookie['name'] == 'ab_sr':
    #         ab_sr = cookie['value']
    #     elif cookie['name'] == 'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=':
    #         Hm_lpvt = cookie['value']
    #     elif cookie['name'] == 'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574':
    #         Hm_lvt = cookie['value']
    #     elif cookie['name'] == 'BAIDUID_BFESS':
    #         BAIDUID_BFESS = cookie['value']
    #     elif cookie['name'] == 'BAIDUID':
    #         BAIDUID = cookie['value']
    #
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    #     'Cookie': 'BIDUPSID=BCCEA8600D3C7380FC306E959A5DE68B; PSTM='+Hm_lvt+'; BAIDUID='+BAIDUID+'; BAIDU_WISE_UID=wapp_1652749904767_535; BAIDUID_BFESS='+BAIDUID_BFESS+'; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574='+Hm_lvt+'; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574='+Hm_lpvt+'; ab_sr='+ab_sr
    #     # 'Cookie': 'BIDUPSID=BCCEA8600D3C7380FC306E959A5DE68B; PSTM=1638268702; BAIDUID=BCCEA8600D3C7380B0021AE1A65B974A:FG=1; BAIDU_WISE_UID=wapp_1652749904767_535; BAIDUID_BFESS=BCCEA8600D3C7380B0021AE1A65B974A:FG=1; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1667461778,1667552150; ab_sr=1.0.1_YjEwNjU1NjRlMjFiZDhiZjVkYTQwYzg4ODlhYzU2MWFiMWEyOWMyNWMzYjUxMzY3Yjk1MTI1NDJhNWY4ZjQwNWY2NGU5OWY4MzIzZTgzNjFiMzQyN2I1M2ZkYWU3MGFkNDNmNTFkMjY2YWM0NDE4NTI5Y2JmNWRkYjk2YjRlZDZkYmYzMGZhMTUxNTk2Y2ZjZDVlY2FhNjlmYzk5YWRkMA==; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1667555673',
    # }
    #
    # print(headers)
    # msg = 'test'
    # with open('res/sign.js', 'r', encoding='utf-8') as f:  # js文件
    #     sign = execjs.compile(f.read()).call("get", msg)
    # data = {
    #     "from": "auto",  # 要翻译的语种
    #     "to": "zh",  # 翻译成的语种
    #     "query": msg,  # 要翻译的内容
    #     'transtype': 'translang',
    #     "simple_means_flag": "3",
    #     "sign": sign,
    #     "token": "b0739d656edf6192395f7f2648bdbbd5",
    #     "domain": "common"
    # }
    # try:
    #     r = requests.post(url=url, headers=headers, data=data,)
    #     if r.status_code == 200:
    #         json = r.json()  # 获取json文件内容
    #         print(json)
    # except Exception as e:
    #     print(e.args[0])

    # time.sleep(10)
    # driver.close()
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    # 构造登录请求
    req = urllib.request.Request(url1, headers=headers)
    # 构造cookie
    cookie = http.cookiejar.CookieJar()
    # 由cookie构造opener
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    # 发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
    resp = opener.open(req)
    print(resp)
    # 登录后才能访问的网页
    url = "https://fanyi.baidu.com/v2transapi"

    msg = 'test'
    with open('res/sign.js', 'r', encoding='utf-8') as f:  # js文件
        sign = execjs.compile(f.read()).call("get", msg)
    data = {
        "from": "auto",  # 要翻译的语种
        "to": 'zh',  # 翻译成的语种
        "query": msg,  # 要翻译的内容
        'transtype': 'translang',
        "simple_means_flag": "3",
        "sign": sign,
        "token": "b0739d656edf6192395f7f2648bdbbd5",
        "domain": "common"
    }
    # 构造访问请求
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, headers=headers, data=post_data)
    print(req)
    resp = opener.open(req)
    print(resp.read().decode('utf-8'))
