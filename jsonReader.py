import json


def readLanguageJson(issimple=False, useBaiduTrans=False):
    ret = []
    if useBaiduTrans:
        filename = "res/language_baidu.json"
    else:
        if issimple:
            filename = "res/language.json"
        else:
            filename = "res/language_abb.json"

    with open(filename, 'r', encoding='utf-8') as fw:
        content = fw.read().strip().replace('\n', '').replace('  ', '').replace('},{', '}},{')
        data = content.split('},')
        for i in range(len(data)):
            loads = json.loads(data[i])
            ret.append(loads)
            # print('the result11 is :' + str(loads['LangCultureName']) + str(loads['DisplayName']))
    return ret
