import socket
import os

def reciveMsg(sock):
    return sock.recv(2048)

def saveFile(sock):
    print('<system> Saving file...')
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
    if reciveMsg(getSock).decode() == 'sfg, header':
        sendSock.send('header received'.encode())
        saveFile(getSock)
        print('<system> File saved')

def sendFile(getSock, sendSock):
    sendSock.send(getHeader('sfg').encode())
    print('header sent')
    header = reciveMsg(getSock).decode()
    print(header)
    if header == 'header received':
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