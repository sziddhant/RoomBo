import socket
import sys
import _thread

import datetime
import random
import requests
import os

from wit_api import *
##############
NumberOfConnections =5
###################
host=''
port=8220
address=(host,port)
#############
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(NumberOfConnections)
#connections=0
addressList=[]
clients=set()

##############################
#Database to use untill NLP isn't applied
greetings = ['hola', 'hello', 'hi', 'hey']

database={
    'roombo':'Hello,how can i help you',
    'name':'RoomBo',
    'what is your name':'my name is RoomBo',
    'what can you do':'i can do many things..'
}

print("Listening for clients...")
############################################
#chat bot code(basic)
def chatbot(data):
    data1 = data.decode()
    x=mesgapi(data1)
    if x:
        print (x)
        bReply(x)
    elif data1 in database:
        print(database[data])
        bReply(database[data])
    elif data1 in greetings:
        random_greeting= random.choice(greetings)
        print(random_greeting)
        bReply(random_greeting)
    else:
        string1="Sorry i don't understand"
        conn.send(string1.encode())
        addData= open("fails.txt",'a')
        addData.write("\n")
        addData.write(data.decode())
        addData.close()

##############################################
#reply mechanism
def bReply(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            client.close()
###############################################
#Server
            
def clientthread(conn,addressList):
    while True:
        output = conn.recv(2048)
        if output.strip()=="disconnect":
            conn.close()
            sys.exit("Disconnect message recived. Shutting down..")
            conn.send("Connection lost")
        elif output:
            data=output
            print ("Message recived:")
            print(data)
            print("Reply:")
            chatbot(data)

while True:
    conn,address = server_socket.accept()
    print("Connected to client ", address)
    clients.add(conn)
    _thread.start_new_thread(clientthread,(conn,addressList))
conn.close()
sock.close()
