import socket
import time
import os
import sys

host = ""
port = 8000

def ServerList():
    print("Sending Acknowledgment of command.")
    msg = "LIST"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Server.")
    F = os.listdir(path="F:\\Programs\\Python-Programs\\file-transfer\\server")
    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)

def ServerExit():

    s.close()
    sys.exit()


def ServerGet(g):
    print("Sending Acknowledgment of command.")
    msg = "GET"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")
    if os.path.isfile(g):
        msg = "File exists. Let's go ahead "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message about file existence sent.")

        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size  # number of packets
        print("File size in bytes:" + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)

        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Packet number:" + str(c))
            print("Data sending in process:")
        GetRunS.close()
        print("Sent from Server - Get function")

    else:
        msg = "Error: File does not exist in Server directory."
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("Message Sent.")


def ServerPut():
    msg = "PUT"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)
    print("Message Sent to Client.")

    if t2[0] == "put":

        BigSAgain = open(t2[1], "wb")
        d = 0
        try:
            Count, countaddress = s.recvfrom(4096)
        except ConnectionResetError:
            print("Error. Port numbers not matching")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        tillI = Count.decode('utf8')
        tillI = int(tillI)

        while tillI != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            dataS = BigSAgain.write(ServerData)
            d += 1
            tillI = tillI - 1
            print("Received packet number:" + str(d))
        BigSAgain.close()
        print("New file Received")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socket initialized")
    s.bind((host, port))
    print("Successful binding. Waiting for Client now.")
except socket.error:
    print("Failed to create socket")
    sys.exit()

# time.sleep(1)
while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print("Error. Port numbers not matching")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()
    if t2[0] == "get":
        ServerGet(t2[1])
    elif t2[0] == "put":
        ServerPut()
    elif t2[0] == "list":
        ServerList()
    elif t2[0] == "exit":
        ServerExit()
    else:
        pass


quit()