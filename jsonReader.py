import json
import os
import sys
# 获取打包后可执行文件的路径
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
def readLanguageJson(issimple=False, useBaiduTrans=False):
    ret = []
    if useBaiduTrans:
        filename = "res/language_baidu.json"
    else:
        if issimple:
            filename = "res/language.json"
        else:
            filename = "res/language_abb.json"

    with open(os.path.join(base_path, filename), 'r', encoding='utf-8') as fw:
        content = fw.read().strip().replace('\n', '').replace('  ', '').replace('},{', '}},{')
        data = content.split('},')
        for i in range(len(data)):
            loads = json.loads(data[i])
            ret.append(loads)
            # print('the result11 is :' + str(loads['LangCultureName']) + str(loads['DisplayName']))
    return ret

def convertLanguageJsonToTran(issimple=False, useBaiduTrans=False, tarlg=''):
    ret = ""
    if useBaiduTrans:
        filename = "res/language_baidu.json"
    else:
        if issimple:
            filename = "res/language.json"
        else:
            filename = "res/language_abb.json"

    tarlg = tarlg.replace('Hans', 'CN')
    tarlg = tarlg.replace('Hant', 'TW')

    with open(os.path.join(base_path, filename), 'r', encoding='utf-8') as fw:
        content = fw.read().strip().replace('\n', '').replace('  ', '').replace('},{', '}},{')
        data = content.split('},')
        for i in range(len(data)):
            loads = json.loads(data[i])
            if str(loads['LangCultureName']).__contains__(tarlg):
                ret = str(loads['LangCultureName'])
                break

    print('the ret is :' + ret)
    return ret
