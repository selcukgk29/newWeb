import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "login.db")
con = sqlite3.connect(db_path, check_same_thread=False)
cursor = con.cursor()


def fetchAllData(table):
    query = "SELECT * from "+table
    cursor.execute(query)
    users = cursor.fetchall()
    return users


def sslLastUpdate():
    cursor.execute('SELECT sslLastUpdate from conf')
    sslLastTime = cursor.fetchone()
    return sslLastTime

def wlanState():
    cursor.execute('SELECT wlan_state from conf')
    state = cursor.fetchone()
    return state

def deleteSqlFunc(res, table, req):
    query = "Delete From " + table + " where " + req+"=?"
    cursor.execute(query, (res,))
    con.commit()


def fetchInfo(req, res, table):
    query = "Select * From "+table+" where "+req+"=?"
    cursor.execute(query, (res,))
    userInfo = cursor.fetchone()
    return userInfo

def getAuth(username):
    cursor.execute('Select auth From USERS where username=?', (username,))
    auth = cursor.fetchone()  
    return auth


def getIp(username):
    cursor.execute('Select ip,auth From USERS where username=?', (username,))
    ip = cursor.fetchone()
    return ip


def updateUser(username, password, mail, authority, id, accessIP):
    cursor.execute('Update USERS set username=?,password=?,auth=?,mail=?,ip=? where id=?',
                   (username, password, authority, mail, accessIP, id,))
    con.commit()


def addFilter(filterName, protocol, sourceAdress, sourcePort, destinationAdress, destinationPort, Action):
    cursor.execute('INSERT INTO filterTable (filterName,protocol,sourceAdress,sourcePort,destinationAdress,destinationPort,Action) VALUES(?,?,?,?,?,?,?)',
                   (filterName, protocol, sourceAdress, sourcePort, destinationAdress, destinationPort, Action))
    con.commit()


def updateFilter(filterName, protocol, sourceAdress, sourcePort, destinationAdress, destinationPort, Action, id):
    cursor.execute('Update filterTable set filterName=?,protocol=?,sourceAdress=?,sourcePort=?,destinationAdress=?,destinationPort=?,Action=? where id=?',
                   (filterName, protocol, sourceAdress, sourcePort, destinationAdress, destinationPort, Action, id))
    con.commit()


def addNatRule(natName, outbound, sourceAdress, toSourceAddress, Action):
    cursor.execute('INSERT INTO natTable (natName,outbound,sourceAdress,toSourceAddress,Action) VALUES(?,?,?,?,?)',
                   (natName, outbound, sourceAdress, toSourceAddress, Action))
    con.commit()


def updateNat(natName, outbound, sourceAdress, toSourceAddress, Action, id):
    cursor.execute('Update natTable set natName=?,outbound=?,sourceAdress=?,toSourceAddress=?,Action=? where id=?',
                   (natName, outbound, sourceAdress, toSourceAddress, Action, id,))
    con.commit()


def addPortForwad(name, destinationPort, ToDestination):
    cursor.execute('INSERT INTO PortForwardTable (PortForwardName,destinationPort,ToDestination) VALUES(?,?,?)',
                   (name, destinationPort, ToDestination))
    con.commit()


def updatePortForward(name, destinationPort, ToDestination, id):
    cursor.execute('Update PortForwardTable set PortForwardName=?,destinationPort=?,ToDestination=? where id=?',
                   (name, destinationPort, ToDestination, id))
    con.commit()


def addBridgeSql(name, intf, ip):
    cursor.execute('INSERT INTO bridgeTable (name,interfaces,ip) VALUES(?,?,?)',
                   (name, intf, ip))
    con.commit()
