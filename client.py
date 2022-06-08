# 使用者端
import tkinter
from tkinter import font
import tkinter.messagebox
import socket
import threading
import time

string = ''


def my_string(s_input):
    string = s_input.get()


def Send(sock):

    if string != '':
        message = name + ' : ' + string
        sock.send(message.encode('utf-8'))

        if 'exit' in string.lower():
            exit(0)


def recv(sock):
    sock.send(name.encode('utf-8'))

    while True:
        data = sock.recv(1024)
        # 获取其他用户信息的时间
        time_tuple = time.localtime(time.time())
        str = ("{}:{}:{}:{}:{}:{}".format(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3], time_tuple[4],time_tuple[5]))
        time_recv = tkinter.Label(t,text=str,width=40,anchor='w')
        time_recv.pack()

        if "%'enter the room'%" in data.decode('utf-8'):
            rrecv = tkinter.Label(t, text=data.decode('utf-8'), width=40, anchor='w',bg='powderblue')
        elif "%'left the room%'" in data.decode('utf-8'):
            rrecv = tkinter.Label(t, text=data.decode('utf-8'), width=40, anchor='w', bg='pink')
        else:
            rrecv = tkinter.Label(t, text=data.decode('utf-8'), width=40, anchor='w')

        rrecv.pack()


# def getOnline():
#     tmp = socket.recv(1024)
#     data1 = tmp.d
#     if "%'online is'%" in data1:
#         num = []
#         num = data1.dp


def left():
    global string
    # 得到文本框中的内容
    string = rv1.get()
    # 发送信息
    Send(s)

    if string != '':
        time_tuple = time.localtime(time.time())

        str = ("{}:{}:{}:{}:{}:{}".format(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3], time_tuple[4],time_tuple[5]))

        # 发送时间
        time_send = tkinter.Label(t,text=str,width=40,anchor='e')
        time_send.pack()

        # 发送信息
        rleft = tkinter.Label(t, text=string, width=40, anchor='e')
        rleft.pack()
        rv1.set('')


def Creat():
    global name
    name = n.get()

    # 开启一个接收信息线程
    tr = threading.Thread(target=recv, args=(s,), daemon=True)
    tr.start()

    # 销毁之前的窗口
    l.destroy()
    e.destroy()
    b.destroy()

    # 创建主对话窗口
    t.title("聊天室")
    t.geometry("400x500")

    # # 在线人数标签 待完成
    # name_top_label = tkinter.Label(t, text='', width=40)
    # name_top_label.pack()
    # currentOnline = getOnline()
    # name_top_label.configure(text=currentOnline)

    # 当前用户名称
    rL0 = tkinter.Label(t, text='%s' % name, width=40)
    rL0.pack()

    rE1 = tkinter.Entry(t, textvariable=rv1,width=40)
    rE1.place(x=1, y=450)         # 200 450
    rB1 = tkinter.Button(t, text="send", width=7, height=1, command=left)
    rB1.place(x=320, y=450)



def close_chat():
    # 点击窗口退出时，增加提示页面
    tkinter.messagebox.showwarning(title='exit', message='exit?')
    # 向服务器发送退出信息
    s.send("break the link".encode('utf-8'))
    exit(0)


# 创建一个客户端socket,让操作系统分配port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ('39.107.251.68', 9999)
s.connect(server)  # 建立連線

t = tkinter.Tk()
t.title("chat")
t.geometry("300x270+500+200")

l = tkinter.Label(t, text='please input your nickname', width=40, height=10,font=('黑体',15,''))
l.pack()

n = tkinter.StringVar()
e = tkinter.Entry(t, width=20, textvariable=n,font=('黑体',15,''))
e.pack()

rv1 = tkinter.StringVar()
# 获取用户名
name = n.get()

b = tkinter.Button(t, text="login", width=30, height=40, command=Creat)
b.pack()

# 添加协议处理程序机制，点击退出按钮时，弹窗提示
t.protocol("WM_DELETE_WINDOW", close_chat)


t.mainloop()

s.close()