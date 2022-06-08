import socket
import threading

num = 0


def chat(connectionSocket, addr):
    # 新加进来的用户不在user元组中，就要向其他用户通告该用户进入进入连接的提示
    if not addr in user:
        print('new connection from %s:%s...' % addr)
        # 向其他用户通告新用户的加入
        for scs in serv_clie_socket:
            serv_clie_socket[scs].send(data + " %'enter the room'%".encode('utf-8'))
        # 将用户的IP+port对应的username加入到user中
        user[addr] = data.decode('utf-8')
        # 将用户的套接字加入到ser_clie_socket中
        serv_clie_socket[addr] = connectionSocket
    else:
        print('%s:%s already in the room' % addr)

    while True:
        d = connectionSocket.recv(1024)
        # 包含exit关键词退出
        if (('exit' in d.decode('utf-8')) | ('break the link' in d.decode('utf-8'))):
            name = user[addr]
            user.pop(addr)
            serv_clie_socket.pop(addr)

            # 向其他用户通告某一用户的离开
            for scs in serv_clie_socket:
                serv_clie_socket[scs].send((name + " %'left the room'%").encode('utf-8'))
            print('Connection from %s:%s closed.' % addr)
            global num
            num = num - 1
            # 结束该线程
            break
        # 展示信息
        else:
            print('%s:%s= "%s"' % (addr[0], addr[1],d.decode('utf-8') ))
            # 向其他用户通告接受的该条信息
            for scs in serv_clie_socket:
                if serv_clie_socket[scs] != connectionSocket:
                    serv_clie_socket[scs].send(d)

# 创建一个欢迎套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = ('39.107.251.68', 9999)
s.bind(addr)

# 监听用户的请求连接，设为128个请求
s.listen(128)

print('server on', addr[0], ":", addr[1])

# 存放请求用户的(IP+端口号:用户名)的键值对
user = {}

# 存放不同用户的socket
serv_clie_socket = {}

while True:
    try:
        print("Waiting for request from client:")
        connectionSocket, addr = s.accept()
        print("received request from client")
    except ConnectionResetError:
        print('Someone left unexcept.')

    # 从client接受到的用户名
    data = connectionSocket.recv(1024)
    if 'break the link' in data.decode():
        print(addr, "close chat window")
    else:
        print("user: ", data.decode())

    # 创建线程 守护进程
    r = threading.Thread(target=chat, args=(connectionSocket, addr), daemon=True)
    r.start()
    num = num + 1
    print("The current number of people is ", num)