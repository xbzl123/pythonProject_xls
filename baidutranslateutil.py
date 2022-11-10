import requests
import random
import json
from hashlib import md5

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path


def set_key(appid, appkey, config):
    config['appid'] = appid
    config['appkey'] = appkey
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False)


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def display_language_table():
    with open('lang_tb', 'r', encoding='utf-8') as file:
        lang_tb = file.read()
    print(lang_tb)


def set_language(*args):
    langs = args[0].split('-')
    if len(langs) != 2:
        print('Invalid Languages! Please Try Again!')
    else:
        config["from_lang"] = langs[0]
        config['to_lang'] = langs[1]
        with open('config.json', 'w') as file:
            json.dump(config, file, ensure_ascii=False)


def display_history():
    with open('history.json', 'r', encoding='utf-8') as file:
        history = json.load(file)
    for his in history["history"]:
        fromLang = his['from']
        toLang = his['to']
        origin = his["trans_result"][0]['src']
        trans = his["trans_result"][0]['dst']
        print(f'From:\33[35m{fromLang}\33[0m')
        print(f'To:\33[36m{toLang}\33[0m')
        print(f'Origin:\33[32m{origin}\33[0m')
        print(f'Translation:\33[34m{trans}\33[0m')
        print('\n')

def clear_history():
    with open('history.json', 'r', encoding='utf-8') as file:
        history = json.load(file)
        history["history"].clear()

    with open('history.json', 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

    print('\33[32mHistory has been cleared!\33[0m')


hashed_function = {
    "lang": set_language,
    "langtb": display_language_table,

    "disp": display_history,
    "clr": clear_history,

}

if __name__ == '__main__':
    appid = '20190906000332471'
    appkey = 'X4wgwMaf7bVZIqBz9Kv7'
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + 'query' +
                    str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': 'query', 'from': 'en',
               'to': 'zh', 'salt': salt, 'sign': sign}

    try:
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
    except:
        print(
            "\033[0;31;40mSomething has gone Wrong! Probably due to your NetWork Status.\033[0m")

    try:
        fromLang = result['from']
        toLang = result['to']
        trans = result["trans_result"][0]['dst']
        print(f'From:\33[35m{fromLang}\33[0m')
        print(f'To:\33[36m{toLang}\33[0m')
        print(f'Translation:\33[32m{trans}\33[0m')
    except:
        print(
            '\033[0;31;40mSomething has gone Wrong! Please check your config file!\033[0m')
