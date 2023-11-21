import socket

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

def connectByIP(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock

def bindClient(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(5)
    conn, addr = sock.accept()
    return conn

def sendMsg(sock, msg):
    sock.send(msg.encode())

def reciveMsg(sock):
    return sock.recv(2048).decode()

def closeSock(sock):
    sock.close()

def startInit():
    myServer = bindClient(9090)
    myClient = connectByIP(genIPByCode(reciveMsg(myServer)), 9090)
    return myServer, myClient

if __name__ == '__main__':
    connCode = genConnectionCode()
    print(f'Your connection code is: {connCode}')
    isCS = int(input('Enter 1 if you want to connect to your server: '))
    if isCS:
        print('Connecting to server...')
        myServer, myClient = startInit()
        while True:
            msg = input()
            sendMsg(myClient, msg)
            if msg == 'exit':
                break
            msg = reciveMsg(myServer)
            print(msg)
            if msg == 'exit':
                break
    else:
        myServer = connectByIP(genIPByCode(int(input('Enter code: '))), 9090)
        sendMsg(myServer, str(connCode))
        myClient = bindClient(9091)
        while True:
            msg = input()
            sendMsg(myClient, msg)
            if msg == 'exit':
                break
            msg = reciveMsg(myServer)
            print(msg)
            if msg == 'exit':
                break