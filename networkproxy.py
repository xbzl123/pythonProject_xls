import urllib
from urllib.parse import urlencode
from urllib.request import Request

import requests

head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
    "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
}
proxy = '122.70.157.11:808'
proxies = {
    'http': 'http://' + proxy
}
url = 'https://translate.google.cn/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q=中国'
# url = 'https://www.baidu.com'
# requests.adapters.DEFAULT_RETRIES = 3
s = requests.session()

headers = {
    'cookie': 'XSRF-TOKEN=eyJpdiI6Ikk4cFdwcGlqMVVPRHM4MFc5Vk1ROWc9PSIsInZhbHVlIjoiUHRHbjZwSTZFTUkrTFRNZVJXczZsV2xZZnN1WEhmM1puakN5WWFsM0RUODhJRUZJYVA3XC9GZ1QyOUR5R0VqaXRmdDJIR0wyV2lBdXlFcTlxXC9HWFVqZz09IiwibWFjIjoiNTlkODY2MGM0YzJlZDQxMTI5ZmIwMmE0NWI5YzkzY2Q4NDg3MjhiODg4NDAxN2Q5NmYzYTE3MmUxZWQzZjk4MiJ9; laravel_session=eyJpdiI6ImFob1k3NWw1U2pBcWhKU3JLdEpDQkE9PSIsInZhbHVlIjoidnNNcXpKSHRmQkYyMGp2NTF4eUhTVVwvSmtidnAwMDV5eGdUWWVhZ2syTUlXaVdQV1JEUldYcG5lXC9mdUtnRkl2akNMR2ZKMkY2NFlWYTFOM2NPRm1uQT09IiwibWFjIjoiYTJhODkwMTJjZjI3NzJiOTE1YWY5MWJkYTNiYTNlMjZjNjI1YjgzZmJlYzhkMTU4Mjk1OWQ5MWEzMGU5OTM5NSJ9; _ga=GA1.2.674295962.1536391451; _gid=GA1.2.1388999250.1536391451; _gat_UA-2009749-51=1; Markets09122018PageView=1; Markets09122018WebinarClosed=true',
    'dnt': '1',
    'x-xsrf-token': 'eyJpdiI6Ikk4cFdwcGlqMVVPRHM4MFc5Vk1ROWc9PSIsInZhbHVlIjoiUHRHbjZwSTZFTUkrTFRNZVJXczZsV2xZZnN1WEhmM1puakN5WWFsM0RUODhJRUZJYVA3XC9GZ1QyOUR5R0VqaXRmdDJIR0wyV2lBdXlFcTlxXC9HWFVqZz09IiwibWFjIjoiNTlkODY2MGM0YzJlZDQxMTI5ZmIwMmE0NWI5YzkzY2Q4NDg3MjhiODg4NDAxN2Q5NmYzYTE3MmUxZWQzZjk4MiJ9',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'accept': 'application/json',
    'referer': 'https://www.barchart.com/stocks/signals/top-bottom/top?viewName=main',
    'authority': 'www.barchart.com',
    'accept-encoding': 'gzip, deflate, br',
}

params = {
    'lists': 'stocks.signals.top.current.us',
    'orderDir': 'asc',
    'fields': 'symbol,symbolName,lastPrice,priceChange,percentChange,opinion,opinionPrevious,opinionLastWeek,opinionLastMonth,symbolCode,symbolType,hasOptions',
    'meta': 'field.shortName,field.type,field.description',
    'hasOptions': 'true',
    'page': '1',
    'limit': '100',
    'raw': '1',
}

payload = {
    'authors': [],
    'coAuthors': [],
    'externalContentTypes': [],
    'fieldOfStudy': "computer-science",
    'page': 1,
    'pageSize': 10,
    'performTitleMatch': True,
    'publicationTypes': [],
    'queryString': "frama-c",
    'requireViewablePdf': False,
    'sort': "relevance",
    'useRankerService': False,
    'venues': []
}

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    # 'Cookie': 'BIDUPSID=BCCEA8600D3C7380FC306E959A5DE68B; PSTM=1638268702; BAIDUID=BCCEA8600D3C7380FC306E959A5DE68B; BAIDU_WISE_UID=wapp_1652749904767_535; BAIDUID_BFESS=BCCEA8600D3C7380B0021AE1A65B974A:FG=1; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1670988214; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=' + Hm_lpvt + '; ab_sr=' + ab_sr
    'Cookie': 'BIDUPSID=BCCEA8600D3C7380FC306E959A5DE68B; PSTM=1638268702; BAIDU_WISE_UID=wapp_1652749904767_535; BAIDUID_BFESS=BCCEA8600D3C7380B0021AE1A65B974A:FG=1; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; newlogin=1; sensorsdata2015jssdkcross={"distinct_id":"184bcfe4c6d6df-0748e631977d21-26021e51-2073600-184bcfe4c6ea65","first_id":"","props":{},"$device_id":"184bcfe4c6d6df-0748e631977d21-26021e51-2073600-184bcfe4c6ea65"}; __bid_n=184c3133670ea40f854207; td_cookie=3049385954; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1670988214; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1670998517; ab_sr=1.0.1_NjliNDQzMDRhZGMxYTQxNTc2NGI1N2M5ZDBhYTk1YmJjNTMzNmNiZmVhZDQ5NTBhNTM3OGI4NDY0NWExODg0YzBkYjViNDBmM2Y3YzNkOTg4ZmRlYzMwNzkwNmE3MDY3NTJlNzUwYWRiZDFmZmZhN2NmYjg4N2U3MTI5OThiOTVlNmI1N2ZjNjRlMzRmNTA3OGZjY2FhYjE3ZTFlYTkwYQ==',
}

if __name__ == '__main__':
    request = Request('https://fanyi.baidu.com/#en/zh/we' + urlencode(params), headers=headers1)
    try:
        response = urllib.request.urlopen(request)
        print('the result :'+response.read().decode("utf-8"))
    except Exception as e:
        print(e.args[0])

# get = s.get(url, proxies=proxies)
