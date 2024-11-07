import urllib
from urllib.parse import urlencode
from urllib.request import Request

import ahttp
import execjs
import requests
from urllib import request
from http import cookiejar

# 跳过SSL验证证书
import ssl

from selenium import webdriver

urls1 = [f"https://movie.douban.com/top250?start={i * 25}" for i in range(2)]
urls = [
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://fakedomain/',
    'http://kennethreitz.com'
]

def startBaiduTranslate(Hm_lpvt=0,ab_sr=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        # 'Cookie': 'BIDUPSID=BCCEA8600D3C7380FC306E959A5DE68B; PSTM=1638268702; BAIDUID=BCCEA8600D3C7380FC306E959A5DE68B; BAIDU_WISE_UID=wapp_1652749904767_535; BAIDUID_BFESS=BCCEA8600D3C7380B0021AE1A65B974A:FG=1; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1670988214; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=' + Hm_lpvt + '; ab_sr=' + ab_sr
        'Cookie': 'BIDUPSID=BCCEA8600D3C7380FC306E959A5DE68B; PSTM=1638268702; BAIDU_WISE_UID=wapp_1652749904767_535; BAIDUID_BFESS=BCCEA8600D3C7380B0021AE1A65B974A:FG=1; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; newlogin=1; sensorsdata2015jssdkcross={"distinct_id":"184bcfe4c6d6df-0748e631977d21-26021e51-2073600-184bcfe4c6ea65","first_id":"","props":{},"$device_id":"184bcfe4c6d6df-0748e631977d21-26021e51-2073600-184bcfe4c6ea65"}; __bid_n=184c3133670ea40f854207; td_cookie=3049385954; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1670988214; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1671000881'
    }
    msg = 'test'
    with open('res/sign.js', 'r', encoding='utf-8') as f:  # js文件
        sign = execjs.compile(f.read()).call("get", msg)
    data = {
        "from": "auto",  # 要翻译的语种
        "to": "zh",  # 翻译成的语种
        "query": msg,  # 要翻译的内容
        'transtype': 'translang',
        "simple_means_flag": "3",
        "sign": sign,
        "token": "b0739d656edf6192395f7f2648bdbbd5",
        "domain": "common"
    }
    request = Request('https://fanyi.baidu.com', headers=headers)
    try:
        response = urllib.request.urlopen(request)
        print('the result :' + response.read().decode("utf-8"))
    except Exception as e:
        print(e.args[0])
if __name__ == '__main__':
    # reqs = [ahttp.post(i) for i in urls]
    # resqs = ahttp.run(reqs, order=True, pool=3)  # 按顺序排序，pool线程池可以设置最大并发数

    # sess = ahttp.Session()  # 和使用ahttp构造请求list请求相比，使用session请求速度更快，而且共享cookies，因为session创建的是一个持久的链接
    # reqs = [sess.post(i) for i in urls]
    # resqs = ahttp.run(reqs, order=True, pool=3)  # 按顺序排序，pool线程池可以设置最大并发数
    # print('全部', resqs)
    # print('第1个', resqs[0])

    url = 'https://fanyi.baidu.com/sug'
    wd = input('enter something of English:')
    data = {
        'kw': wd
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    response = requests.post(url=url, data=data, headers=headers)

    obj_json = response.json()
    print(obj_json)

    # url = "https://www.baidu.com"
    # payload = {"key1": "value1", "key2": "value2"}
    # r = requests.get(url, params=payload)
    # print(r.text)


    # # 设置忽略SSL验证
    # ssl._create_default_https_context = ssl._create_unverified_context
    #
    # # 声明一个CookieJar对象实例来保存cookie
    # cookie = cookiejar.CookieJar()
    # # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    # handler = request.HTTPCookieProcessor(cookie)
    # # 通过CookieHandler创建opener
    # opener = request.build_opener(handler)
    # # 此处的open方法打开网页
    # response = opener.open('http://www.baidu.com')
    # # 打印cookie信息
    # for item in cookie:
    #     print('Name = %s' % item.name)
    #     print('Value = %s' % item.value)


    # opt = webdriver.ChromeOptions()  # 创建Chrome参数对象
    #
    # opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    #
    # # opt.headless = True  # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
    #
    # driver = webdriver.Chrome(options=opt)  # 创建Chrome无界面对象
    #
    # cookie_dict = {}
    # url = "https://fanyi.baidu.com/#en/zh/we"
    # driver.get(url)
    # # 获取cookie列表
    # cookie_list = driver.get_cookies()
    # # 格式化打印cookie
    # Hm_lpvt = 0
    # ab_sr = ''
    # for cookie in cookie_list:
    #     cookie_dict[cookie['name']] = cookie['value']
    #     if cookie['name'] == 'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574':
    #         Hm_lpvt = cookie['value']
    #     elif cookie['name'] == 'ab_sr':
    #         ab_sr = cookie['value']
    #     print(cookie['name']+"="+cookie['value']+"\n")
    # startBaiduTranslate(Hm_lpvt, ab_sr)









