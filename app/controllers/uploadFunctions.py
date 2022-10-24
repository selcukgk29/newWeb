from time import sleep
import os

def convertion(newfirmware):
    path="/root/"+newfirmware
    print(path)
    with open(path,"rb") as input:
        filecontent=input.read()
        with open("/root/core" ,"wb") as output:
            output.write(filecontent[24:])
            os.system("chmod 777 /root/*")
            print("File converted!")
    sleep(2)
    os.system("rm -rf"+" "+path)


def stopService():
    try:
        os.system('systemctl stop dm50')
        print("Service stopped...")
    except:
        print("Service couldn't stop")


def startService():
    try:
        os.system('systemctl start dm50')
        print('Service started...')
    except:
        print("Service couldn't start")


def restartService():
    stopService()
    sleep(6)
    startService()

def systemMove(oldCore, newName): 
    try:
        os.system('mv '+oldCore+" "+newName)
        print("Moved...")
    except:
        print("Failed!System move")


def refreshFirmware(firmware):
    stopService()   
    sleep(6)
    os.system("mkdir /root/oldCore")
    systemMove("/root/core", "/root/oldCore/core_upload")
    convertion(firmware)  
    startService()
