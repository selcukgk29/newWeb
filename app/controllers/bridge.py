import os
from time import sleep
from venv import create
from app.db.sqlProcess import addBridgeSql, deleteSqlFunc

# addbridge function


def addMakeFile(name, ip, intf):
    with open("/root/conf/makebridge.sh", "a") as f:
        f.writelines("brctl addbr "+name+"\n")
        f.writelines("brctl addif "+name+intf)
        f.writelines("ifconfig "+name +
                     " "+ip+" up\n")


def deleteBridgeFormMakeFile(BrName):
    with open("/root/conf/makebridge.sh", "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if BrName not in line:
                f.write(line)
        f.truncate()


def addbridge(*args):
    os.system("touch /root/conf/makebridge.sh")
    createBridge = "brctl addbr "+args[0]["bridgeName"]+"\n"  # Bridge oluştur
    os.system(createBridge)
    print(createBridge)
    intf = []
    try:
        if(args[0]["toggle"] == "on"):
            # eth0 varsa oluşturduğun birdge e ekle
            print(args[0]["toggle"])
            os.system("brctl addif "+args[0]["bridgeName"]+" eth0")
            os.system("ifconfig "+args[0]["bridgeName"] +
                      " "+args[0]["bridgeIP"]+" up")
            # makebridge.sh file for working on boot
            addMakeFile(args[0]["bridgeName"], args[0]["bridgeIP"], " eth0\n")
            intf.append("eth0")
    except:
        print("Not selected intf eth0")
    try:
        # eth1 varsa oluşturduğun birdge e ekle
        if(args[0]["toggle1"] == "on"):
            os.system("brctl addif "+args[0]["bridgeName"]+" eth1")
            os.system("ifconfig "+args[0]["bridgeName"] +
                      " "+args[0]["bridgeIP"]+" up")
            addMakeFile(args[0]["bridgeName"], args[0]["bridgeIP"], " eth1\n")
            intf.append("eth1")
    except:
        print("Not selected intf eth1")
    result = ""
    for i in intf:
        result = result+" "+i
    addBridgeSql(args[0]["bridgeName"], (result), args[0]["bridgeIP"])

# Delete bridge function


def delBridge(args):
    # interfaceleri boşluğa göre split et daha sonra down
    list(filter(lambda x: os.system("ifconfig "+x+" down"), args[1].split()))
    list(filter(lambda x: os.system(
        "ifconfig "+args[0]+" down"), args[1].split()))
    rule = "brctl delbr "+args[0]
    os.system(rule)
    sleep(2)
    print(rule)
    deleteBridgeFormMakeFile(args[0])
    deleteSqlFunc(args[3], "bridgeTable", "id")
    list(filter(lambda x: os.system("ifconfig "+x+" up"), args[1].split()))
