import socket
import base64
import os

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
    sock.connect((ip, 9090))
    return sock

def bindClient():
    sock = socket.socket()
    sock.bind(('', 9090))
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

async def sendAndRecive(myServer, myClient):
    while True:
        msg = input()
        sendMsg(myClient, msg.encode())
        if msg == 'exit':
            break
        msg = reciveMsg(myServer).decode()
        print(msg)
        if msg == 'exit':
            break

if __name__ == '__main__':
    connCode = genConnectionCode()
    print(f'Your connection code is: {connCode}')
    isCS = int(input('Enter 1 if you want to connect to your server: '))
    if isCS:
        print('Connecting to server...')
        myServer, myClient = startInit()
        msg = ""
        while True:
            sendAndRecive(myServer, myClient)
            if msg == 'exit':
                break
    else:
        myServer = connectByIP(genIPByCode(int(input('Enter code: '))))
        sendMsg(myServer, str(connCode).encode())
        myClient = bindClient()
        while True:
            sendAndRecive(myServer, myClient)
            if msg == 'exit':
                break
