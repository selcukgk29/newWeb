import os

def getTimeUp():
    uptime = os.popen('uptime -p').read()
    return uptime


def getTime():
    time = os.popen('date').read()
    return time


def ramUsage():
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    return(str(used_memory) + " / " + str(total_memory) + " used:%  " + str(round((used_memory/total_memory) * 100, 2)))


def interfaceControl():
    list=["eth0","eth1","wlan0","br0"]
    result=[]
    for i in list:
        result.append(os.popen(" cat /sys/class/net/{0}/operstate".format(i)).read().upper())
    return result

def grepGSMip():
    try:
        request=os.popen("ifconfig ppp0 | egrep '([0-9]{1,3}\.){3}[0-9]{1,3}'").read()
        for i in request.split(" "):
            if "addr" in i:
                resultip=i[5:]
        return resultip
    except:
        return None


