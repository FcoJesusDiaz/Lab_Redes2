#!/usr/bin/python3

#Práctica realizada por Francisco Jesús Díaz Pellejero 2ºB

import socket
import hashlib #Módulo perteneciente a la librería estándar
import struct
import array
import sys
import base64

########################## Reto 0 ########################## 
def challenge0():
    sock=socket.socket()
    sock.connect(('rick',2000))
    print(sock.recv(1024).decode("utf-8"))

    sock.send('lucid_knuth'.encode("utf-8"))

    instructions=sock.recv(1024).decode("utf-8")
    print(instructions)
    sock.close()
    return instructions


########################## Reto 1 ########################## 

def challenge1(id):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(('',2753))
    sock.sendto(("2753 "+id).encode(),('rick',4000))
    data,client=sock.recvfrom(1024)
    print(data.decode("utf-8"))
    sock.sendto(id.upper().encode("utf-8"),client)
    data,client=sock.recvfrom(1024)
    instructions=data.decode("utf-8")
    print(instructions)
    sock.close()
    return instructions


########################## Reto 2 ########################## 

def challenge2(id):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('rick',3006))
    sock.send(replyCubes(countCubes(sock),id).encode("utf-8"))
    instructions=waitInstr(sock)
    #print(instructions)
    sock.close()
    return instructions

def countCubes(sock):
    nCubes=0
    turret=bytes('\u256D'+'('+'\u25C9'+')'+'\u256E',"utf-8")
    companionCube=bytes('['+'\u2764'+']',"utf-8")
    while 1:
        data=sock.recv(10000)
        index=data.find(turret)
        if index != -1:
            nCubes+=data.count(companionCube,0,index)
            break
        nCubes+=data.count(companionCube)
    return nCubes

def replyCubes(nCubes,id):
    msg=''
    while nCubes>0:
        msg+='['+'\u2764'+']'
        nCubes-=1
    msg+=' '+id
    return msg


########################## Reto 3 ########################## 

def challenge3(id):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('rick',6520))
    data=read_Until_Palindrome(sock)
    reverseNumbers(data)
    sock.send(replyReverseNumbers(data,id).encode("utf-8"))
    instructions=waitInstr(sock)
    #print(instructions)
    sock.close()
    return instructions

def read_Until_Palindrome(sock):
    data=''
    pos=[0] #Posición de la lista de números y palabras donde se encuentra el palíndromo
            #Utilizo una lista para pasar la variable por referencia a una función
    while 1:
        data+=sock.recv(10000).decode("utf-8")
        pos[0]=0
        if checkPalindrome(data,pos):
            break   
    data=data.split()
    return data[:pos[0]-1]


def checkPalindrome(data,pos):
    for i in data.split():
        pos[0]+=1
        if not (i.isnumeric()) and i == i[::-1] and len(i)!=1:
            return True
    return False

def reverseNumbers(data):
    num=[] #Lista que almacena los números recibidos al revés
    num_index=[] #Lista que almacena la posición de los números en la lista 'data'
    extractNumbers(data,num,num_index)
    data.reverse()
    insertNumbers(data,num,num_index)

def extractNumbers(data,num,num_index):
    dataCp=[] 
    dataCp+=data 
    cont_index=0 #Posición de un elemento de la lista 'data'
    cont_index_Cp=0 #Posición de un elemento de la copia 
    for i in dataCp:
        if i.isnumeric():
            data.pop(cont_index)
            num.append(i[::-1])
            num_index.append(cont_index_Cp)
            cont_index-=1 #Si se quita un elemento de 'data' tenemos que restar uno a la
                          #posición para no saltarnos el siguiente elemento
        cont_index+=1
        cont_index_Cp+=1

def insertNumbers(data,num,num_index):
    for i,j in zip(num_index,num):
        data.insert(i,j)

def replyReverseNumbers(data,id):
    separator=" "
    return id+" "+separator.join(data)+ " --"



########################## Reto 4 ##########################
def challenge4(id):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('rick',9000))
    sock.send(id.encode("utf-8"))
    result=hashlib.md5(readFileData(getFileSize(sock),sock))
    sock.send(result.digest())
    instructions=waitInstr(sock)
    #print(instructions)
    return instructions

def getFileSize(sock):
    data=''
    while 1:
        newData=sock.recv(1).decode()
        if newData == ':':
            break
        data+=newData
    return int(data)

def readFileData(size,sock):
    data=b''
    while 1:
        newData=sock.recv(size)
        size-=len(newData)
        if size == 0:
            data=data+newData   
            break
        data=data+newData
    return data


########################## Reto 5 ##########################
def challenge5(id):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    pseudoHeader=struct.pack("!3sHBH",b'YAP',0,0,1)
    payload=base64.b64encode(id.encode())
    msg=struct.pack("!3sHBHH",b'YAP',0,0,cksum(pseudoHeader+payload),1)+payload
    sock.sendto(msg,('rick',6001))
    instructions,client=sock.recvfrom(10000)
    instructions=base64.b64decode(instructions[10:]+b'============').decode()
    print(instructions)
    return instructions

def cksum(pkt):
    # type: (bytes) -> int
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H', pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff


############ Métodos usados en más de un reto ############# 

def waitInstr(sock):
    instr=''
    while 1:
        newData=sock.recv(10000)
        if not newData:
            break
        instr=newData.decode("utf-8","replace")
        print(instr)
    return instr

def getId(instructions):
    aux=instructions.split("\n")
    aux=aux[0]
    id=aux.split(":")
    return id[1]


########################## Main ########################## 

def main():
    instructions=challenge0()
    instructions=challenge1(getId(instructions))
    instructions=challenge2(getId(instructions))
    instructions=challenge3(getId(instructions))
    instructions=challenge4(getId(instructions))
    instructions=challenge5(getId(instructions))

if __name__=="__main__":
    main()


