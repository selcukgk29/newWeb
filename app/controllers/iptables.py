import os


def DellRule(sql):
    rule = "iptables -D INPUT -p "+sql[1]
    print(sql)
    if(sql[2] != ""):
        old = " -s "+sql[2]
        rule = rule+old
    if(sql[3] != ""):
        old = " --sport "+sql[3]
        rule = rule+old
    if(sql[4] != ""):
        old = " -d "+sql[4]
        rule = rule+old
    if(sql[5] != ""):
        old = " --dport "+sql[5]
        rule = rule+old
    deletedRule = rule+" -j "+sql[6]
    return deletedRule


def addRule(*args):
    rule = "iptables -A INPUT"+" -p "+args[0]["protocol"]
    if args[0]["sourceAdress"] != "":
        source = " -s "+args[0]["sourceAdress"]
        rule = rule+source
    if args[0]["protocol"] != "icmp":
        if args[0]["sourcePort"] != "":
            sPort = " --sport "+args[0]["sourcePort"]
            rule = rule+sPort
    if args[0]["destinationAdress"] != "":
        destination = " -d "+args[0]["destinationAdress"]
        rule = rule+destination
    if args[0]["protocol"] != "icmp":
        if args[0]["destinationPort"] != "":
            dPort = " --dport "+args[0]["destinationPort"]
            rule = rule+dPort
    addrules = rule+" -j "+args[0]["filterAction"]
    print(addrules)
    return addrules


def addPortForward(*args):
    rule = "iptables -t nat -A PREROUTING -p tcp --dport " + \
        args[0]["portForwards_DestinationPort"]+" -j DNAT --to-destination " + \
        args[0]["portForwards_ToDestinationAdress"]
    ip = args[0]["portForwards_ToDestinationAdress"].split(":")
    masRule = "iptables -t nat -A POSTROUTING -d " + \
    ip[0]+"/32 -p tcp -m tcp --dport "+ip[1]+" -j MASQUERADE"    

    os.system(rule)
    print(rule)
    os.system(masRule)
    print(masRule)
    os.system("iptables-save > /root/conf/rules.v4")


def DellPortForward(sql):
    rule = "iptables -t nat -D PREROUTING -p tcp --dport " + \
        str(sql[1])+" -j DNAT --to-destination "+str(sql[2])
    ip = sql[2].split(":")
    masRule = "iptables -t nat -D POSTROUTING -d " + \
        ip[0]+"/32 -p tcp -m tcp --dport "+ip[1]+" -j MASQUERADE"
    os.system(rule)
    print(rule)
    os.system(masRule)
    print(masRule)
    os.system("iptables-save > /root/conf/rules.v4")


def natRule(*args):
    if args[0]["natAction"] == "SNAT":
        rule = "iptables -t nat -A POSTROUTING -s " + args[0]["sourceAdress"]+" -o "+args[0]["outbound"]+" -j " + \
            args[0]["natAction"]+" --to-source "+args[0]["toSourceAddress"]
        print(rule)
        os.system(rule)
    if args[0]["natAction"] == "MASQUERADE":
        rule = "iptables -t nat -A POSTROUTING -s " + \
            args[0]["sourceAdress"]+" -o " + \
            args[0]["outbound"]+" -j "+args[0]["natAction"]
        print(rule)
        os.system(rule)
    os.system("iptables-save > /root/conf/rules.v4")
    return rule


def deleteNat(*args):
    print(args)
    if args[0][4] == "SNAT":
        rule = "iptables -t nat -D POSTROUTING -s " + \
            args[0][2]+" -o "+args[0][1]+" -j " + \
            args[0][4] + " --to-source "+args[0][3]
    if args[0][4] == "MASQUERADE":
        rule = "iptables -t nat -D POSTROUTING -s " + \
            args[0][2]+" -o "+args[0][1]+" -j "+args[0][4]
    os.system(rule)
    print(rule)
    os.system("iptables-save > /root/conf/rules.v4")
