import wx
import telnetlib
import sys
import threading
import win32com.client
import os
import webbrowser
from time import sleep
from chatbot import tuling
from config import BOT, default_server
from get_audio import get_audio
import keda_API


bot_use = BOT

class MyPanel(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title,style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU |wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        try:
            image_file = './111.png'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))
            image_width = to_bmp_image.GetWidth()
            image_height = to_bmp_image.GetHeight()
        except IOError:
            print ('Image file %s not found' % image_file)
            raise SystemExit

        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.Button(self.bitmap, -1, label="服务器", pos=(680, 165), size=(130, 33),)
        self.serverAddressLabel.SetForegroundColour('blue')
        self.userNameLabel = wx.Button(self.bitmap, -1, label="用户名", pos=(680, 230), size=(130, 33))
        self.userNameLabel.SetForegroundColour('blue')
        self.serverAddress = wx.TextCtrl(self.bitmap, -1, value=default_server,
                                     pos=(820, 165), size=(150, 30), style=wx.TE_PROCESS_ENTER)
        self.serverAddress.SetForegroundColour('blue')
        self.userName = wx.TextCtrl(self.bitmap, -1, pos=(820, 230), size=(150, 30), style=wx.TE_PROCESS_ENTER)
        self.userName.SetForegroundColour('blue')
        self.loginButton = wx.Button(self.bitmap, -1, label='登录', pos=(690, 300), size=(120, 45))

        self.loginButton.SetForegroundColour('blue')
       # self.loginButton.SetBackgroundColour('green')
        self.exitButton = wx.Button(self.bitmap, -1, label='退出', pos=(840, 300), size=(120, 45))
        self.exitButton.SetForegroundColour('red')
       # panel.SetSizer(sizer)
       # panel.Fit()
    # 绑定登录方法
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
    # 绑定退出方法
        self.exitButton.Bind(wx.EVT_BUTTON, self.exit)
    # 服务器输入框Tab事件
        self.serverAddress.SetFocus()
        self.Bind(wx.EVT_TEXT_ENTER, self.usn_focus, self.serverAddress)
    # 用户名回车登录
        self.Bind(wx.EVT_TEXT_ENTER, self.login, self.userName)
        self.Show()





    # 回车调到用户名输入栏
    def usn_focus(self, event):
        self.userName.SetFocus()

    def login(self, event):
        # 登录处理
        try:
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            con.open(serverAddress[0], port=int(serverAddress[1]), timeout=10)
            response = con.read_some()
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='当前用户：'+str(self.userName.GetLineText(0)), size=(1360, 900))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (95, 20))

    def exit(self, event):
       # wx.Exit()
       self.Close()

    # 显示错误信息对话框
    def showDialog(self, title, content, size):
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()


class ChatFrame(wx.Frame):
    """
    聊天窗口
    """
    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title, style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU |wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.SetSize(size)
        self.Center()


        try:
            image_file = './37.jpg'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))
            image_width = to_bmp_image.GetWidth()
            image_height = to_bmp_image.GetHeight()
        except IOError:
            print ('Image file %s not found' % image_file)
            raise SystemExit

        self.chatFrame = wx.TextCtrl(self.bitmap, pos=(520, 49), size=(588, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.chatFrame.SetForegroundColour('blue')
        self.chatFrame.SetBackgroundColour('white')
        self.message = wx.TextCtrl(self.bitmap, pos=(520, 485), size=(588, 136), style=wx.TE_PROCESS_ENTER)
        self.sayButton = wx.Button(self.bitmap, label="语音识别", pos=(970, 365), size=(138,55),style=wx.STAY_ON_TOP)
        self.sayButton.SetForegroundColour('blue')
        self.sayButton.SetBackgroundColour('white')
        self.screenshotButton = wx.Button(self.bitmap, label="屏幕截图", pos=(520, 425), size=(138, 55))
        self.screenshotButton.SetForegroundColour('blue')
        self.screenshotButton.SetBackgroundColour('white')
        self.searchButton = wx.Button(self.bitmap, label="百度搜索", pos=(970, 425), size=(138, 55))
        self.searchButton.SetForegroundColour('blue')
        self.searchButton.SetBackgroundColour('white')
        self.songButton = wx.Button(self.bitmap, label="播放音乐", pos=(820, 425), size=(138, 55))
        self.songButton.SetForegroundColour('blue')
        self.songButton.SetBackgroundColour('white')
        self.sendButton = wx.Button(self.bitmap, label="发送消息", pos=(820, 625), size=(138, 55))
        self.sendButton.SetForegroundColour('black')
        self.sendButton.SetBackgroundColour('white')
        self.usersButton = wx.Button(self.bitmap, label="在线用户", pos=(670, 425), size=(138, 55))
        self.usersButton.SetForegroundColour('blue')
        self.usersButton.SetBackgroundColour('white')
        self.closeButton = wx.Button(self.bitmap, label="退出系统", pos=(970, 625), size=(138, 55))
        self.closeButton.SetForegroundColour('red')
        self.closeButton.SetBackgroundColour('white')
        self.runButton = wx.Button(self.bitmap, label="启动机器人", pos=(520, 365), size=(138, 55))
        self.runButton.SetForegroundColour('blue')
        self.runButton.SetBackgroundColour('white')
        self.weatherButton = wx.Button(self.bitmap, label="天气查询", pos=(670, 365), size=(138, 55))
        self.weatherButton.SetForegroundColour('blue')
        self.weatherButton.SetBackgroundColour('white')
        self.translateButton = wx.Button(self.bitmap, label="中英互译", pos=(820, 365), size=(138, 55))
        self.translateButton.SetForegroundColour('blue')
        self.translateButton.SetBackgroundColour('white')
        
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)  # 发送按钮绑定发送消息方法
        self.message.SetFocus()  # 输入框回车焦点
        self.sayButton.Bind(wx.EVT_BUTTON, self.say)  # SAY按钮按下
        self.Bind(wx.EVT_TEXT_ENTER, self.send, self.message)  # 回车发送消息
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)  # Users按钮绑定获取在线用户数量方法
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)  # 关闭按钮绑定关闭方法
        self.screenshotButton.Bind(wx.EVT_BUTTON, self.screenshot)
        self.songButton.Bind(wx.EVT_BUTTON, self.song)
        self.searchButton.Bind(wx.EVT_BUTTON, self.search)
        self.runButton.Bind(wx.EVT_BUTTON, self.run)
        self.translateButton.Bind(wx.EVT_BUTTON, self.translate)
        self.weatherButton.Bind(wx.EVT_BUTTON, self.weather)
        treceive = threading.Thread(target=self.receive)  # 接收信息线程
        treceive.start()
        #self.ShowFullScreen(True)  # 全屏
        self.Show()


    def say(self, event):
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak('请说话')
        get_audio("E:/Python_Doc/voice_say/say_voice.wav" )
        sys.stdout.write("you ask>> ")
        text = keda_API.XF_text("E:/Python_Doc/voice_say/say_voice.wav", 16000)
        #con.write(('say ' + text + '\n').encode("utf-8"))

        self.message.AppendText(text)
        self.send(self)



    def send(self, event):
        # 发送消息
        message = str(self.message.GetLineText(0)).strip()
        con.write(('say ' + message + '\n').encode("utf-8"))
        self.message.Clear()
        # 机器人回复
        if bot_use == "TuLing":
            answer = tuling(message)
            #con.write(('tuling_say '+time.strftime("%Y-%m-%d %H:%M:%S")+'\n').encode("utf-8"))
            con.write(('tuling_say '+answer + '\n').encode("utf-8"))
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(answer)
        elif bot_use == "User":
            return

        return

    def run(self, event):

        global bot_use
        bot_use = "TuLing"
        self.message.Clear()
        con.write(( 'noone_say 华软机器人小E为您服务' + '\n').encode("utf-8"))
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak('华软机器人小E为您服务')
        return

    def lookUsers(self, event):
        # 查看当前在线用户
        con.write(b'look\n')

    def weather(self, event):

        con.write(( 'noone_say 请输入您要查询哪个城市的天气预报' + '\n').encode("utf-8"))
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak('请输入您要查询哪个城市的天气预报')

    def translate(self, event):

        con.write(( 'noone_say 请输入您要翻译的内容' + '\n').encode("utf-8"))
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak('请输入您要翻译的内容')

    def screenshot(self, event):

        os.system(r"start C:\Windows\system32\SnippingTool.exe")

    def search(self, event):
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak("百度一下，你就知道")
        con.write(('noone_say ' + '百度一下，你就知道' + '\n').encode("utf-8"))
        self.message.Clear()
        webbrowser.open('https://www.baidu.com/')


    def song(self, event):
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak('正在为您播放音乐')
       # con.write('正在为您播放钟无艳' + '\n').encode("utf-8")
        #filename = 'E:/MP3精品2/'+message[2:]+'.mp3'
        os.popen('D:/Chatbot—小E/Vk.mp3')
        return


    def close(self, event):
        # 关闭窗口
       # tremove_voice = threading.Thread(target=remove_voice)
        #tremove_voice.start()
        # thread.start_new_thread(remove_voice, ())
        con.write(b'logout\n')
        #os.system("taskkill /F /IM  KuGou.exe")
        con.close()
        self.Close()

    def receive(self):
        # 接受服务器的消息
        while True:
            sleep(1)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)

if __name__ == '__main__':

    app = wx.App()
    con = telnetlib.Telnet()
    MyPanel(None, -1, title="相约@华软", size=(1360, 730))
    app.MainLoop()
