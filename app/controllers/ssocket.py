import socket
import json
from time import sleep
import threading


class socTh(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 6432
        self.mbuffer = ''
        self.byte_json = ''
        self.dataType0 = None
        self.dataType1 = None
        self.dataType2 = None
        self.dataTypeATBAND = None
        self.dataTypeATVERSION = None
        self.dataTypeATCSQ = None

    def run(self):
        newSend = ''
        devSend = ''
        while 1:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.TCP_IP, self.TCP_PORT))
                s.listen(1)
                self.conn, addr = s.accept()
                self.conn.settimeout(30)
                print('Listening for client from adress:', addr)
                with self.conn:
                    while 1:
                        data = self.conn.recv(100000).decode('utf-8')
                        if data == '':
                            print("Socket closed!Reconnectting...")
                            break
                        # Send block parameters to Dm50
                        from app import sendToClient
                        if (sendToClient != newSend and sendToClient != 0):
                            newSend = sendToClient
                            self.conn.send(newSend.encode('utf-8'))
                            # print(type(newSend.encode('utf-8')))
                            # print(newSend.encode('utf-8'))
                            #print( "=>>>>>>>>>>>>>>Send Block Parameters to client!!!")
                        ###

                        # Send device parameters to dm50
                        from app import sendDeviceParameters
                        if (sendDeviceParameters != devSend and sendDeviceParameters != 0):
                            devSend = sendDeviceParameters
                            self.conn.send(devSend.encode('utf-8'))
                            print(
                                "=>>>>>>>>>>>>>>Send Device parameters to client!!!")

                        self.mbuffer = self.mbuffer+data
                        idx = self.mbuffer.index('[')
                        while(idx >= 0):
                            if self.mbuffer[0] != '[' and idx > 0:
                                self.mbuffer = self.mbuffer[idx:len(
                                    self.mbuffer)]
                            idx = self.mbuffer.index(']')
                            if idx < 0:
                                print("line 63 socket")
                                break
                            if self.mbuffer[0] == '[' and idx > 0:
                                self.byte_json = self.mbuffer[0:idx+1]
                                self.mbuffer = self.mbuffer[idx +
                                                            1: len(self.mbuffer)]
                                if self.byte_json:
                                    newdata = json.loads(self.byte_json)
                                    if len(newdata) > 0:
                                        if 'DataType' in newdata[0]:
                                            if newdata[0]['DataType'] == 0:
                                                self.dataType0 = newdata
                                                #print('DataType0 recived size:', len(self.dataType0))
                                        else:
                                            self.dataType1 = newdata
                                            try:
                                                if(len(soc.dataType1[0]) <= 4):
                                                    if("VERSION" in self.dataType1[0]['Data']):
                                                        self.dataTypeATVERSION = (
                                                            self.dataType1[0]['Data'])[8:26]
                                                        print(
                                                            self.dataTypeATVERSION)
                                                    if("BAND" in self.dataType1[0]['Data']):
                                                        self.dataTypeATBAND = (
                                                            self.dataType1[0]['Data'])[5:7]
                                                        print(
                                                            self.dataTypeATBAND)

                                                    if("CSQ" in self.dataType1[0]['Data']):
                                                        self.dataTypeATCSQ = (
                                                            self.dataType1[0]['Data'])[4:10]
                                                        print(
                                                            self.dataTypeATCSQ)
                                                else:
                                                    self.dataType2 = self.dataType1
                                                    print(self.dataType2)
                                            except Exception as e:
                                                print(e)
                                            print('DataType1 received size :', len(
                                                self.dataType1))

                                break
                            idx = 0
                            sleep(0.5)
            except Exception as e:
                print(e)
                sleep(3)


soc = socTh()
soc.start()
