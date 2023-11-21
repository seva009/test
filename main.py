import socket
import os
import threading


def getLocIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    locIP = s.getsockname()[0]
    s.close()
    return locIP

def genConnectionCode():
    lastipnum = int(socket.inet_aton(getLocIP())[-1])
    return lastipnum

def genIPByCode(code):
    return socket.inet_ntoa((socket.inet_aton(getLocIP())[:-1] + bytes([int(code)])))

def connectByIP(ip):
    sock = socket.socket()
    sock.connect((ip, 4444))
    return sock

def bindClient():
    sock = socket.socket()
    sock.bind(('', 4444))
    sock.listen(5)
    flag = True
    while flag:
        conn, addr = sock.accept()
        if conn:
            flag = False
    return conn

def sendMsg(sock, msg):
    sock.send(msg)

def reciveMsg(sock):
    return sock.recv(2048)

def closeSock(sock):
    sock.close()

def startInit():
    myServer = bindClient()
    myClient = connectByIP(genIPByCode(reciveMsg(myServer)))
    return myServer, myClient

if __name__ == '__main__':
    connCode = genConnectionCode()
    print(f'Your connection code is: {connCode}')
    isCS = int(input('Enter 1 if you want to connect to your server: '))
    if isCS:
        print('Connecting to server...')
        myServer, myClient = startInit()
        def send_thread():
            while True:
                msg = input()
                sendMsg(myClient, msg.encode())
                print(msg)
                if msg == 'exit':
                    break
        
        def receive_thread():
            while True:
                msg = reciveMsg(myServer).decode()
                print(msg)
                if msg == 'exit':
                    break

        send_thread = threading.Thread(target=send_thread)
        receive_thread = threading.Thread(target=receive_thread)

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()
        
    else:
        myServer = connectByIP(genIPByCode(int(input('Enter code: '))))
        sendMsg(myServer, str(connCode).encode())
        myClient = bindClient()
        def send_thread():
            while True:
                msg = input()
                sendMsg(myClient, msg.encode())
                print(msg)
                if msg == 'exit':
                    break
        
        def receive_thread():
            while True:
                msg = reciveMsg(myClient).decode()
                print(msg)
                if msg == 'exit':
                    break

        send_thread = threading.Thread(target=send_thread)
        receive_thread = threading.Thread(target=receive_thread)

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()