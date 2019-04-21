import wx
import telnetlib
from time import sleep
# import _thread as thread
from chatbot import chatbot, tuling, play_mp3, remove_voice
from config import BOT, default_server, VOICE_SWITCH
from recorder import *
import threading
from get_audio import get_audio
import keda_API
import sys
import win32com.client
import os
import pygame
import mp3play
import time
import webbrowser
import minimu
import image

bot_use = BOT




'''class MyPanel(wx.Frame):
    """
    登录窗口
    """
    def __init__(self, parent, id, title, size):
        # 初始化，添加控件并绑定事件
        wx.Frame.__init__(self, parent, id, title)
        
        self.SetSize(size)
        self.Center()

        self.serverAddressLabel = wx.StaticText(self, label="Server Address", pos=(450, 600), size=(120, 25))
        self.userNameLabel = wx.StaticText(self, label="UserName", pos=(45, 90), size=(120, 25))
        self.serverAddress = wx.TextCtrl(self, value=default_server,
                                         pos=(120, 37), size=(150, 25), style=wx.TE_PROCESS_ENTER)
        self.userName = wx.TextCtrl(self, pos=(120, 87), size=(150, 25), style=wx.TE_PROCESS_ENTER)
        self.loginButton = wx.Button(self, label='Login', pos=(50, 145), size=(90, 30))
        self.exitButton = wx.Button(self, label='Exit', pos=(180, 145), size=(90, 30))
        # 绑定登录方法
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        # 绑定退出方法
        self.exitButton.Bind(wx.EVT_BUTTON, self.exit)
        # 服务器输入框Tab事件
        self.serverAddress.SetFocus()
        self.Bind(wx.EVT_TEXT_ENTER, self.usn_focus, self.serverAddress)
        # 用户名回车登录
        self.Bind(wx.EVT_TEXT_ENTER, self.login, self.userName)

        self.Show()'''

class MyPanel(wx.Frame):
    def __init__(self, parent, id, title, size):
        wx.Frame.__init__(self, parent, id, title,style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU |wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        #panel = wx.Panel(self, -1)
        #sizer = wx.GridSizer(rows=3, cols=3, hgap=5, vgap=5)
        #self.panel = wx.Panel(self)
        #self.panel.Bind(wx.EVT_ERASE_BACKGROUND,self.OnEraseBack)
        try:
            image_file = 'C:/Users/pc/Desktop/111.png'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))
            image_width = to_bmp_image.GetWidth()
            image_height = to_bmp_image.GetHeight()
            #set_title = '%s %d x %d' % (image_file, to_bmp_image.GetWidth(), to_bmp_image.GetHeight())
        # parent.SetTitle(set_title)
        except IOError:
            print ('Image file %s not found' % image_file)
            raise SystemExit
        #创建一个按钮
        #self.button = wx.Button(self.bitmap, -1, label='Test', pos=(10,10))
        #self.SetTransparent(200)
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
    def OnEraseBack(self,event):

        '''dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("C:/Users/pc/Pictures/psbCAVG3EMZ.jpg")
        dc.DrawBitmap(bmp, 0, 0)'''

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
            image_file = 'C:/Users/pc/Desktop/37.jpg'
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))
            image_width = to_bmp_image.GetWidth()
            image_height = to_bmp_image.GetHeight()
            #set_title = '%s %d x %d' % (image_file, to_bmp_image.GetWidth(), to_bmp_image.GetHeight())
        # parent.SetTitle(set_title)
        except IOError:
            print ('Image file %s not found' % image_file)
            raise SystemExit
        #font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        #font.SetPointSize(9)
        self.chatFrame = wx.TextCtrl(self.bitmap, pos=(520, 49), size=(588, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.chatFrame.SetForegroundColour('blue')
        self.chatFrame.SetBackgroundColour('white')
        self.message = wx.TextCtrl(self.bitmap, pos=(520, 425), size=(588, 136), style=wx.TE_PROCESS_ENTER)
       # self.message.SetInsertionPoint(0)
        #设置richText控件的文本样式
        #self.message.SetStyle(2,6,wx.TextAttr("white","black"))
       # points=self.message.GetFont().GetPointSize()
        #创建一个字体样式
       # f=wx.Font(points+3,wx.ROMAN,wx.ITALIC,wx.BOLD,True)
        #用创建的字体样式设置文本样式
       # self.message.SetStyle(8,14,wx.TextAttr("blue",wx.NullColor,f))
        #self.message.SetStyle(44, 47, wx.TextAttr("RED", "YELLOW"))
        #self.SetTransparent(200)
        self.sayButton = wx.Button(self.bitmap, label="语音识别", pos=(520, 365), size=(138,55),style=wx.STAY_ON_TOP)
        self.sayButton.SetForegroundColour('blue')
        self.sayButton.SetBackgroundColour('white')
        self.screenshotButton = wx.Button(self.bitmap, label="屏幕截图", pos=(670, 365), size=(138, 55))
        self.screenshotButton.SetForegroundColour('blue')
        self.screenshotButton.SetBackgroundColour('white')
        self.searchButton = wx.Button(self.bitmap, label="百度搜索", pos=(820, 365), size=(138, 55))
        self.searchButton.SetForegroundColour('blue')
        self.searchButton.SetBackgroundColour('white')
        self.songButton = wx.Button(self.bitmap, label="播放音乐", pos=(970, 365), size=(138, 55))
        self.songButton.SetForegroundColour('blue')
        self.songButton.SetBackgroundColour('white')
        self.sendButton = wx.Button(self.bitmap, label="发送消息", pos=(820, 565), size=(138, 55))
        self.sendButton.SetForegroundColour('black')
        self.sendButton.SetBackgroundColour('white')
        self.usersButton = wx.Button(self.bitmap, label="在线用户", pos=(670, 565), size=(138, 55))
        self.usersButton.SetForegroundColour('black')
        self.usersButton.SetBackgroundColour('white')
        self.closeButton = wx.Button(self.bitmap, label="退出系统", pos=(970, 565), size=(138, 55))
        self.closeButton.SetForegroundColour('red')
        self.closeButton.SetBackgroundColour('white')
        self.runButton = wx.Button(self.bitmap, label="启动机器人", pos=(520, 565), size=(138, 55))
        self.runButton.SetForegroundColour('black')
        self.runButton.SetBackgroundColour('white')
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)  # 发送按钮绑定发送消息方法
        self.message.SetFocus()  # 输入框回车焦点
        self.sayButton.Bind(wx.EVT_BUTTON, self.say)  # SAY按钮按下
        #self.sayButton.Bind(wx.EVT_LEFT_UP, self.sayUp)  # Say按钮弹起
        self.Bind(wx.EVT_TEXT_ENTER, self.send, self.message)  # 回车发送消息
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)  # Users按钮绑定获取在线用户数量方法
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)  # 关闭按钮绑定关闭方法
        self.screenshotButton.Bind(wx.EVT_BUTTON, self.screenshot)
        self.songButton.Bind(wx.EVT_BUTTON, self.song)
        self.searchButton.Bind(wx.EVT_BUTTON, self.search)
        self.runButton.Bind(wx.EVT_BUTTON, self.run)
        treceive = threading.Thread(target=self.receive)  # 接收信息线程
        treceive.start()
        #self.ShowFullScreen(True)  # 全屏
        self.Show()

    #def sayDown(self, event):
     #   trecording = threading.Thread(target=recording)
      #  trecording.start()

    def say(self, event):
        get_audio("E:/Python_Doc/voice_say/say_voice.wav" )
        sys.stdout.write("you ask>> ")
        text = keda_API.XF_text("E:/Python_Doc/voice_say/say_voice.wav", 16000)
        #con.write(('say ' + text + '\n').encode("utf-8"))

        self.message.AppendText(text)
        self.send(self)



    def send(self, event):
        # 发送消息
        message = str(self.message.GetLineText(0)).strip()
        global bot_use
        if message != '':
            if message == "chatbot":
                bot_use = "ChatBot"
                self.message.Clear()
                con.write(('noone_say You have been changed ChatBot-Chat' + '\n').encode("utf-8"))
                return
           # elif message == "tuling":
                #bot_use = "TuLing"
                #self.message.Clear()
                #con.write(( 'noone_say 华软小E为您服务' + '\n').encode("utf-8"))
                #return

            elif message == "user":
                bot_use = "User"
                self.message.Clear()
                con.write(('noone_say You have been changed User-Chat' + '\n').encode("utf-8"))
                return
            elif message == "打开酷狗。":#加入对软件的处理
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak("正在为您打开酷狗音乐，请稍等")
                con.write(('chatbot ' + '正在为您打开酷狗音乐，请稍等' + '\n').encode("utf-8"))
                os.system(r"start D:\KGMusic\KuGou.exe")
                bot_use = "打开酷狗。"
                self.message.Clear()

                return

            elif message == "关闭酷狗。":#加入对软件的处理
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak("已经为您关闭酷狗音乐")
                con.write(('chatbot ' + '已经为您关闭酷狗音乐' + '\n').encode("utf-8"))
                os.system("taskkill /F /IM  KuGou.exe")
                bot_use = "关闭酷狗。"
                self.message.Clear()
                #turing_answer_text = '好的主人，正在为您关闭酷狗音乐'r
                return
            elif '搜索' in message:#加入对网页的处理
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak('正在为您搜索'+message[2:])
                con.write(('正在为您搜索'+message[2:] + '\n').encode("utf-8"))
                webbrowser.open('https://www.baidu.com/baidu?ie=utf-8&wd='+message[2:])
                turing_answer_text = '好的'

            elif message == '打开网页。':#加入对网页的处理
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak("正在为您打开网页，请稍等")
                con.write(('chatbot ' + '正在为您打开网页，请稍等' + '\n').encode("utf-8"))
                self.message.Clear()
                webbrowser.open('https://tieba.baidu.com/f?kw=%C0%B3%C7%D0%CB%B9%CC%D8%B3%C7&tpl=5')
                turing_answer_text = '好的'

            elif '来一首' in message:#对唱歌的处理
               # pygame.init()
                #pygame.mixer.init()
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak('正在为您播放'+message[3:-1])
                con.write(('正在为您播放'+message[3:-1] + '\n').encode("utf-8"))
                #filename = 'E:/MP3精品2/'+message[2:]+'.mp3'
                os.system('D:/ChatRoom-master/'+message[3:-1]+'.mp3')
                #song=minimu.load(r'D:/ChatRoom-master/'+message[2:-1]+'.mp3')
                #song.play()# 开始播放

               # song.pause() # 暂停播放

                #song.resume() # 恢复播放

                #song.stop() # 停止播放

                #song.isplaying() # True:正在播放(包括暂停) False:已停止播放

                #song.volume(50) # 调节音量至50%
#clip = mp3play.load("./钟无艳.mp3")
                #clip.play()
                #time.sleep(min(30, clip.seconds()))#如果mp3文件的长度小于30少时，全部播放完，否则仅播放30秒。
                #clip.stop()



                # pygame.mixer.music.load(file)
                #pygame.mixer.music.play()
                self.message.Clear()

                return
            con.write(('say ' + message + '\n').encode("utf-8"))
            self.message.Clear()
            # 机器人回复
            if bot_use == "ChatBot":
                answer = chatbot(message)
                con.write(('chatbot_say ' + answer + '\n').encode("utf-8"))
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(answer)
            elif bot_use == "TuLing":
                answer = tuling(message)
                #con.write(('tuling_say '+time.strftime("%Y-%m-%d %H:%M:%S")+'\n').encode("utf-8"))
                con.write(('tuling_say '+answer + '\n').encode("utf-8"))
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(answer)
            elif bot_use == "User":
                return

        '''  if VOICE_SWITCH:
                # 写本地音乐文件
                baidu_api2(answer)
                # 新建线程播放音乐
                tplay_mp3 = threading.Thread(target=play_mp3)
                tplay_mp3.start()  */
                # thread.start_new_thread(play_mp3, ())'''
        return

    def run(self, event):
        # 查看当前在线用户
        global bot_use
        bot_use = "TuLing"
        self.message.Clear()
        con.write(( 'noone_say 华软小E为您服务' + '\n').encode("utf-8"))
        return

    def lookUsers(self, event):
        # 查看当前在线用户
        con.write(b'look\n')

    def screenshot(self, event):
        # 查看当前在线用户

        os.system(r"start C:\Windows\system32\SnippingTool.exe")

    def search(self, event):
        # 查看当前在线用户
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak("百度一下，你就知道")
        con.write(('noone_say ' + '百度一下，你就知道' + '\n').encode("utf-8"))
        self.message.Clear()
        webbrowser.open('https://www.baidu.com/')


    def song(self, event):
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak('正在为您播放钟无艳')
       # con.write('正在为您播放钟无艳' + '\n').encode("utf-8")
        #filename = 'E:/MP3精品2/'+message[2:]+'.mp3'
        os.system('D:/ChatRoom-master/钟无艳.mp3')


    def close(self, event):
        # 关闭窗口
        tremove_voice = threading.Thread(target=remove_voice)
        tremove_voice.start()
        # thread.start_new_thread(remove_voice, ())
        con.write(b'logout\n')
        con.close()
        self.Close()

    def receive(self):
        # 接受服务器的消息
        while True:
            sleep(1)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)

    def saytime(self):
        i = 0
        while True:
            self.chatFrame.AppendText('正在录音...' + str(i) + '秒\n')
            sleep(1)
            i = i + 1


if __name__ == '__main__':


    #frame = Frame()
    #frame.Show()

    app = wx.App()
    con = telnetlib.Telnet()
    MyPanel(None, -1, title="相约@华软", size=(1360, 730))
    app.MainLoop()
'''if __name__ == '__main__':
    #app = wx.PySimpleApp()
    app = wx.App()
    con = telnetlib.Telnet()
    frame = wx.Frame(None, -1, '相约@华软', size=(1360,730),style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU |wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
    my_panel = MyPanel(frame, -1)
    #frame = wx.Frame(None, -1, '相约@华软', size=(1360,730))
   # ChatFrame(None, -1, title="相约@华软", size=(960, 750))
    frame.Show()
    app.MainLoop()'''