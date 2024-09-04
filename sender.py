#!/usr/bin/env python3

import socket
import select
import SenderSW
import ReceiverSW
import SenderGBN
import ReceiverGBN
import SenderSR
import ReceiverSR


senderList = [SenderSW, SenderGBN, SenderSR]
receiverList = [ReceiverSW, ReceiverGBN, ReceiverSR]


def my_sender():
    print('Select Protocol For Sending Data :-')
    print('1.Stop and wait\n2.Go Back N ARQ\n3.Selective Repeat ARQ\n')
    protocol = int(input('Enter choice for protocol: '))
    if(protocol > 3 or protocol < 1):
        protocol = 1
    protocol -= 1
    HOST = '127.0.0.1'
    PORT = 3000
    with socket.socket() as client:
        client.connect((HOST, PORT))
        msg = client.recv(1024).decode()
        print(msg, end='')
        name = input()
        client.sendall(bytes(name, 'utf-8'))
        address = client.recv(1024).decode()
        senderAddress = int(address)
        while(True):
            print('Input options:-\n1.Send data\n2.Exit\n')
            choice = int(input('Enter option: '))
            if(choice == 1):
                client.send(str.encode("request for sending"))
            elif(choice == 2):
                client.send(str.encode("close"))
                break
            inputs = [client]
            output = []
            readable, writable, exceptionals = select.select(
                inputs, output, inputs, 3600)
            for s in readable:
                data = s.recv(1024).decode()
                if(data == "No client is available"):
                    print(data)
                    break
                elif(choice == 1):
                    #file_name = 'data.txt'
                    file_name = "C:/Users/Sutanjoy Pal/Desktop/Flow-Control/data.txt"
                    receiver_list = data.split(',')
                    print('Available clients are :-')
                    for index in range(0, len(receiver_list)):
                        print((index+1), '. ', receiver_list[index])
                    choice = int(input('\nYour Client choice : '))
                    choice -= 1
                    while(choice not in range(0, (len(receiver_list)))):
                        choice = int(input('Choose correctly: '))
                        choice -= 1
                    s.send(str.encode(str(choice)))
                    receiverAddress = int(s.recv(1024).decode())
                    # print("SenderAddress: ",senderAddress)
                    # print("ReceiverAddress: ",receiverAddress)
                    my_sender = senderList[protocol].Sender(
                        client, name, senderAddress, receiver_list[index], receiverAddress, file_name)
                    my_sender.transmit()
                    data = s.recv(1024)
                    data = data.decode()
                    print(data)
            if not (readable or writable or exceptionals):
                continue


if __name__ == '__main__':
    my_sender()
