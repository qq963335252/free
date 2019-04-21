# 默认输入的服务器地址，测试时候使用，避免登录总是输入地址麻烦
default_server = "127.0.0.1:1"

# 定义服务器端口，一个端口一个房间
PORT = range(1, 3)

# 图灵Tuling机器人还是ChatBot聊天机器人选择
BOTS = ["TuLing", "User"]
BOT = BOTS[1]

# 浏览器请求头文件
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', }
headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)Chrome/62.0.3202.94 Safari/537.36'}

# 图灵密匙，自动回复地址，选择的key不同，tuling机器人的回答也各不相同
tuling_app_key1 = "e5ccc9c7c8834ec3b08940e290ff1559"
tuling_app_key = "4bc32d41c10be18627438ae45eb839ac"
#tuling_app_key = "a4c3fff4277a4e9784a27e28d6c3f7b7"
tuling_url = "http://www.tuling123.com/openapi/api"




