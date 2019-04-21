from chatterbot import ChatBot
import requests
import json
from config import *


# 图灵自动回复
def tuling(info):
    url = tuling_url + "?key=%s&info=%s" % (tuling_app_key, info)
    content = requests.get(url, headers=headers)
    answer = json.loads(content.text)
    return answer['text']





