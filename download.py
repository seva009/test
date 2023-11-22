import socket
import os

def reciveMsg(sock):
    return sock.recv(2048)

def saveFile(sock):
    filename = reciveMsg(sock).decode()
    file = open(filename, 'wb')
    data = reciveMsg(sock)
    while data:
        file.write(data)
        data = reciveMsg(sock)
    file.close()

def getHeader(typeS):
    if typeS == 'sfg':
        return 'sfg, header'
    elif typeS == 'sfs':
        return 'sfs, header'
    elif typeS == 'hg':
        return 'header received'

def getSign(typeS):
    if typeS == 'sfg, header':
        return 'sfg'
    elif typeS == 'sfs, header':
        return 'sfs'
    elif typeS == 'header received':
        return 'hg'

def getFile(getSock, sendSock):
    if getSign(reciveMsg(sock).decode()) == 'sfg':
        sendSock.send(getHeader('hg').encode())
        saveFile(getSock)
        print('<system> File saved')

def sendFile(getSock, sendSock):
    sendSock.send(getHeader('sfg').encode())
    print('header sent')
    header = reciveMsg(getSock).decode()
    print(header)
    if getSign(header) == 'hg':
        print('<system> Enter file name:')
        filename = input()
        sendSock.send(filename.encode())
        sendFile = open(filename, 'rb')
        data = sendFile.read(2048)
        while data:
            sendSock.send(data)
            data = sendFile.read(2048)
        sendFile.close()
    else:
        print('<system> Wrong header')