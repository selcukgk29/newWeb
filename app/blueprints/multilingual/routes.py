import datetime
import ipaddress
import json
from flask import (jsonify, render_template, Blueprint, g, redirect, send_file, send_from_directory, session,
                   request, current_app, abort, flash, url_for)
from app.controllers.uploadFunctions import refreshFirmware, restartService
from app.db.sqlProcess import *
import sqlite3
import app.controllers.statuspage as statuspage
from app.controllers.ssocket import *
from app.controllers import validator
from app.controllers import *
import app.controllers.syslogController as syslogFunc
import app.controllers.logView as journalctl
import app.controllers.iptables as iptables
import app.controllers.bridge as bridge

from flask_babel import _
from app import app
import os


con = sqlite3.connect("./app/db/login.db", check_same_thread=False)
cursor = con.cursor()

UPLOAD_FOLDER = '/root'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


multilingual = Blueprint('multilingual', __name__,
                         template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    if values is None:
        values = {}
    g.lang_code = values.pop('lang_code', None)


@multilingual.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        adapter = app.url_map.bind('')
        try:
            endpoint, args = adapter.match(
                '/en' + request.full_path.rstrip('/ ?'))
            return redirect(url_for(endpoint, **args), 301)
        except:
            print("Hata!!")

    dfl = request.url_rule.defaults
    if 'lang_code' in dfl:
        if dfl['lang_code'] != request.full_path.split('/')[1]:
            abort(404)

# Giriş route u ilk açılışta login e yönlendirir.


@app.route('/')
def route():
    os.system("mkdir /root/conf")
    return redirect('/en')

# İlk webserver açılışında Default username pass değiştirme sayfası route


@multilingual.route("/updateDefaultUser", defaults={"lang_code": "en"}, methods=['GET', "POST"])
@multilingual.route("/userGuncelle", defaults={"lang_code": "tr"}, methods=['GET', "POST"])
def updateDefaultUser():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template("multilingual/changeDefaultPass.html", EditUserInfo=fetchInfo("id", 0, "USERS"))
    if request.method == 'POST':
        if validator.usernameValid(request.form['newUsername']):
            if validator.password_check(request.form['newUserPassword']):
                if validator.emailValid(request.form['newUserMail']):
                    message = str(validator.emailValid(
                        request.form["newUserMail"]))
                    flash(message)
                    return redirect(url_for("multilingual.updateDefaultUser"))
                else:
                    updateUser(request.form['newUsername'], request.form['newUserPassword'],
                               request.form['newUserMail'], "Administrator", "0", "-")
            else:
                flash(
                    'Password must be 8-16 characters long and contain one uppercase and one lowercase character.')
                return redirect(url_for("multilingual.updateDefaultUser"))
        else:
            flash('Invalid username!')
            return redirect(url_for("multilingual.updateDefaultUser"))
        return redirect('/')


@multilingual.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('multilingual/index.html', userInfo=session['username'], auth=getAuth(session['username']), uptime=statuspage.getTimeUp(), time=statuspage.getTime(), ramUsage=statuspage.ramUsage(), netstatus=statuspage.interfaceControl(), dataType1=soc.dataType2)
            # return render_template('multilingual/index.html', userInfo=session['username'], auth=getAuth(session['username']), uptime="statuspage.getTimeUp()", time="statuspage.getTime()", ramUsage="statuspage.ramUsage()", netstatus="statuspage.interfaceControl()", dataType1="asd")
        else:
            return render_template('multilingual/login.html')
    if request.method == 'POST':
        cursor.execute('SELECT username,password,auth FROM USERS where username =? and password=?',
                       (request.form['username'], request.form['password']))
        global user
        user = cursor.fetchone()
        try:
            print(user[0])
            print(getAuth(user[0])[0])
        except:
            flash('Username or Password is incorrect.')
            return redirect('/en')
        # Default password change page route
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session['defaultUser'] = 1
            return redirect("/updateDefaultUser")
        if (getAuth(user[0])[0] == "Technician" or getAuth(user[0])[0] == "Operator") and getIp(user[0])[0] == request.remote_addr:
            session['username'] = user[0]
            return redirect('index')
        elif getAuth(user[0])[0] == "Administrator":
            session['username'] = user[0]
            print(session)
            # return render_template('index.html', userInfo=session['username'], netstatus=statuspage.interfaceControl(), auth=getAuth(session['username']), uptime=statuspage.getTimeUp(), time=statuspage.getTime(), ramUsage=statuspage.ramUsage(), dataType1=soc.dataType2)
            return render_template('multilingual/index.html', userInfo=session['username'], auth=getAuth(session['username']), uptime="statuspage.getTimeUp()", time="statuspage.getTime()", ramUsage="statuspage.ramUsage()", netstatus="statuspage.interfaceControl()", dataType1="asd")

        elif getIp(user[0])[0] != request.remote_addr:
            print(request.remote_addr)
            flash('IP not authorized to access!')
            return redirect('/en')
        else:
            flash('Username or Password is incorrect.')
            return redirect('/en')


@multilingual.route('/index')
def index():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/index.html', userInfo=session['username'], auth=getAuth(session['username']), uptime="statuspage.getTimeUp()", time="statuspage.getTime()", ramUsage="statuspage.ramUsage()", netstatus="statuspage.interfaceControl()", dataType1="asd")


@multilingual.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        print("session temizlendi")
        return redirect('/')


@multilingual.route('/uploadProject', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route('/projeYukle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def uploadProject():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/uploadProject.html', userInfo=session['username'], auth=getAuth(session['username']))
    if request.method == 'POST':
        uploaded_file = request.files['project']
        if uploaded_file.filename != " ":
            uploaded_file.filename = "project"
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            print("Project File uploaded!!")
            restartService()
        return redirect(url_for('multilingual.uploadProject'))


@multilingual.route('/firmwareYukle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/uploadFirmware', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def uploadFirmware():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/uploadFirmware.html', userInfo=session['username'], auth=getAuth(session['username']))
    if request.method == 'POST':
        uploaded_file = request.files['firmware']
        if uploaded_file.filename != '':
            uploaded_file.filename = "core.mx3"
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            print("File uploaded!!")
            refreshFirmware(uploaded_file.filename)
            print("Firmware refreshing...")
        return redirect(url_for('multilingual.uploadFirmware'))


@multilingual.route('/sslGuncelle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/sslUpdatePage', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def sslUpdatePage():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/sslUpdatePage.html', userInfo=session['username'], auth=getAuth(session['username']), sslUpdateTime=(sslLastUpdate()[0])[:16])
    if request.method == 'POST':
        uploaded_file = request.files['sslUpdate']
        if uploaded_file.filename != " ":
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            print("SSL certificate uploaded!!")
            updateTime = datetime.datetime.now()
            print(updateTime)
            cursor.execute("Update conf set sslLastUpdate= ?", (updateTime,))
        con.commit()
        return redirect(url_for('multilingual.sslUpdatePage'))


sendDeviceParameters = 0


@multilingual.route('/userManagement', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route('/kullaniciYonetimi', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def userManagement():
    if request.method == 'GET':
        try:
           session['username']
        except:
            return redirect('/')
        return render_template('multilingual/userManagement.html', userInfo=session['username'], auth=getAuth(session['username']), users=fetchAllData("USERS"))
    if request.method == 'POST':
        if request.form['DeleteUserId']:
            return redirect(request.referrer)


@multilingual.route('/kullaniciYonetimi/kullaniciEkle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/userManagement/adduser', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def userManagementAddUser():
    if request.method == 'POST':
        cursor = con.cursor()
        if validator.usernameValid(request.form['newUsername']):
            if validator.password_check(request.form['newUserPassword']):
                if validator.emailValid(request.form['newUserMail']):
                    message = str(validator.emailValid(
                        request.form["newUserMail"]))
                    flash(message)
                    return redirect(url_for('multilingual.userManagement'))
                else:
                    cursor.execute('INSERT INTO USERS (username,password,auth,mail,ip) VALUES(?,?,?,?,?)', (
                        request.form['newUsername'], request.form['newUserPassword'], request.form['auth'], request.form['newUserMail'], request.form['newUserIP']))
                    con.commit()
                    print("Added new user!")
                    return redirect(url_for('multilingual.userManagement'))
            else:
                flash('Password must be 8-16 characters long and contain one number one special character one uppercase and one lowercase character.')
            return redirect(url_for('multilingual.userManagement'))
        flash('Invalid username! (Username must be min 3 characters.)')
        return redirect(url_for('multilingual.userManagement'))

@multilingual.route('/kullaniciYonetimi/kullaniciDuzenle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/userManagement/editUser', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def userManagementEditUser():
    if request.method == 'POST':
        global userId
        userId = int(request.form['EditUserId'])
        print(userId)
        userInfo = fetchInfo("id", userId, "USERS")
        return render_template('multilingual/userEditPage.html', auth=getAuth(session['username']), EditUserInfo=userInfo)
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        print(userId)
        userInfo = fetchInfo("id", userId, "USERS")
        return render_template('multilingual/userEditPage.html', auth=getAuth(session['username']), EditUserInfo=userInfo)


@multilingual.route('/userManagement/editUserButton', methods=['GET', 'POST'])
def userManagementEditUserButton():
    if request.method == 'POST':
        if validator.usernameValid(request.form['newUsername']):
            if validator.password_check(request.form['newUserPassword']):
                if validator.emailValid(request.form['newUserMail']):
                    message = str(validator.emailValid(
                        request.form["newUserMail"]))
                    flash(message)
                    return redirect(url_for('multilingual.userManagementEditUser'))
                else:
                    updateUser(request.form['newUsername'], request.form['newUserPassword'],
                               request.form['newUserMail'], request.form['auth'], userId, request.form['newUserIP'])
            else:
                flash(
                    'Password must be 8-16 characters long and contain one uppercase and one lowercase character.')
                return redirect(url_for('multilingual.userManagementEditUser'))
        else:
            flash('Invalid username!')
            return redirect(url_for('multilingual.userManagementEditUser'))
        return redirect(url_for('multilingual.userManagement'))       


@multilingual.route('/userManagement/deleteUser', methods=['GET', 'POST'])
def userManagementDeleteUser():
    if request.method == 'POST':
        deleteSqlFunc(request.form['DeleteUserId'], "USERS", "id")
        return redirect(url_for('multilingual.userManagement'))       


@multilingual.route('/ipAyarlari/eth0', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/ipSettings/eth0', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def ipSettingsEth0():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        print(soc.dataType2)
        return render_template('multilingual/ipSettingsEth0.html', userInfo=session['username'], dataType1=soc.dataType2, auth=getAuth(session['username']))
    if request.method == 'POST':
        if(soc.dataType2 != None):
            soc.dataType2[0]['LocalIp'] = request.form['ethIP']
            soc.dataType2[0]['Netmask'] = request.form['ethSubnet']
            soc.dataType2[0]['Gateway'] = request.form['gateway0']
            global sendDeviceParameters
            print(sendDeviceParameters)
            sendDeviceParameters = json.dumps(soc.dataType2)
        return redirect(url_for("multilingual.ipSettingsEth0"))


@multilingual.route('/ipAyarlari/eth1', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/ipSettings/eth1', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def ipSettingsEth1():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/ipSettingsEth1.html', userInfo=session['username'], dataType1=soc.dataType2, auth=getAuth(session['username']))
    if request.method == 'POST':
        if(soc.dataType2 != None):
            soc.dataType2[0]['LocalIp2'] = request.form['ethIP']
            soc.dataType2[0]['Netmask2'] = request.form['ethSubnet']
            soc.dataType2[0]['Gateway2'] = request.form['gateway1']
            global sendDeviceParameters
            sendDeviceParameters = json.dumps(soc.dataType2)
            print(sendDeviceParameters)
        return redirect(url_for("multilingual.ipSettingsEth1"))


@multilingual.route('/ipAyarlari/gsm', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/ipSettings/gsm', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def ipSettingsGSM():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/ipSettingsGSM.html', userInfo=session['username'], dataType1=soc.dataType2, auth=getAuth(session['username']))

    if request.method == 'POST':
        if(soc.dataType2 != None):
            soc.dataType2[0]['GprsApn'] = request.form['APN']
            soc.dataType2[0]['GprsName'] = request.form['Name']
            soc.dataType2[0]['GprsPssw'] = request.form['Password']
            global sendDeviceParameters
            sendDeviceParameters = json.dumps(soc.dataType2)
        return redirect(url_for("multilingual.ipSettingsGSM"))


@multilingual.route('/ipAyarlari/wlan', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/ipSettings/wlan', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def ipSettingsWlan():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/ipSettingsWlan.html', userInfo=session['username'], wifiState=wlanState(), dataType1=soc.dataType2, auth=getAuth(session['username']))
    if request.method == 'POST':
        # wlan client modda db ye 0 yaz.
        if(soc.dataType2 != None):
            cursor.execute("Update conf set wlan_state= ?", (0,))
            con.commit()
            soc.dataType2[0]['WifiSSID'] = request.form['SSID']
            soc.dataType2[0]['WifiPssw'] = request.form['Password']
            soc.dataType2[0]['WifiLocalIp'] = request.form['WifiLocalIp']
            soc.dataType2[0]['WifiGateway'] = request.form['WifiGateway']
            soc.dataType2[0]['WifiDns1Ip'] = request.form['WifiDns1Ip']
            soc.dataType2[0]['WifiDns2Ip'] = request.form['WifiDns2Ip']
            soc.dataType2[0]['WifiMode'] = "0"
            global sendDeviceParameters
            sendDeviceParameters = json.dumps(soc.dataType2)
        return redirect(url_for("multilingual.ipSettingsWlan"))


@multilingual.route('/ipAyarlari/wlan/hotspot', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/ipSettings/wlan/hotspot', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def wlanSetting():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/ipSettingsWlanHotspot.html', userInfo=session['username'], wifiState=wlanState(), dataType1=soc.dataType2, auth=getAuth(session['username']))
    if request.method == 'POST':
        # wlan client modda db ye 1 yaz.
     
        if(soc.dataType2 != None):
            cursor.execute("Update conf set wlan_state= ?", (1,))
            con.commit()
            soc.dataType2[0]['WifiSSID_Hspot'] = request.form['WifiSSID_Hspot']
            soc.dataType2[0]['WifiPssw_Hspot'] = request.form['WifiPssw_Hspot']
            soc.dataType2[0]['WifiLeaseTime'] = request.form['WifiLeaseTime'] 
            soc.dataType2[0]['WifiCountry'] = request.form['WifiCountry']
            soc.dataType2[0]['WifiLocalIp_Hspot'] = request.form['WifiLocalIp_Hspot']
            soc.dataType2[0]['WifiStartIp'] = request.form['WifiStartIp']
            soc.dataType2[0]['WifiEndIp'] = request.form['WifiEndIp']
            soc.dataType2[0]['WifiDns1Ip'] = request.form['WifiDns1Ip']
            soc.dataType2[0]['WifiDns2Ip'] = request.form['WifiDns2Ip']
            soc.dataType2[0]['WifiMode'] = "2"
            global sendDeviceParameters
            sendDeviceParameters = json.dumps(soc.dataType2)
        return redirect(url_for("multilingual.ipSettingsWlan"))



@multilingual.route('/ipSettings/wlan/disable', methods=['GET', 'POST'])
def disable_wlan():
    # wlan client modda db ye 2 yaz.
    cursor.execute("Update conf set wlan_state= ?", (2,))
    con.commit()
    if soc.dataType2 != None: 
        soc.dataType2[0]['WifiMode'] = "3"
        global sendDeviceParameters
        sendDeviceParameters = json.dumps(soc.dataType2)
    return "Disabled"


@multilingual.route('/firewall/filter', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route('/guvenlikDuvari/filter', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def filteringRules():
    if request.method == "POST":
        if(request.form["protocol"] == "icmp" or request.form["protocol"] == "ALL"):
            addFilter(request.form["filterName"], request.form["protocol"], request.form["sourceAdress"],
                      " ", request.form["destinationAdress"], " ", request.form["filterAction"])
            os.system(iptables.addRule(request.form))
            os.system("iptables-save > /root/conf/rules.v4")
            print("icmp or all rule added")
        else:
            addFilter(request.form["filterName"], request.form["protocol"], request.form["sourceAdress"], request.form["sourcePort"],
                      request.form["destinationAdress"], request.form["destinationPort"], request.form["filterAction"])
            os.system(iptables.addRule(request.form))
            os.system("iptables-save > /root/conf/rules.v4")
        return redirect(url_for("multilingual.filteringRules"))
    if request.method == "GET":
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/filteringRules.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchAllData("filterTable"))


@multilingual.route('/firewall/filterRule/deletefilter', methods=['GET', 'POST'])
def filteringdeleteRules():
    if request.method == "POST":
        ruleFromSQL = fetchInfo(
            "id", request.form["DeleteFilter"], "filterTable")
        if(ruleFromSQL[1] == "icmp" or ruleFromSQL[1] == "ALL"):
            deleteRule = "iptables -D INPUT -s " + \
                ruleFromSQL[2]+" -p "+ruleFromSQL[1]+" -d " + \
                ruleFromSQL[4]+" -j "+ruleFromSQL[6]
            deleteSqlFunc(request.form["DeleteFilter"], "filterTable", "id")
            os.system(deleteRule)
            print(deleteRule)
            os.system("iptables-save > /root/conf/rules.v4")
            return redirect(url_for("multilingual.filteringRules"))
        os.system(iptables.DellRule(ruleFromSQL))
        print(iptables.DellRule(ruleFromSQL))
        print("705 line >>>>>>>>>")
        os.system("iptables-save > /root/conf/rules.v4")
        deleteSqlFunc(request.form["DeleteFilter"], "filterTable", "id")
        return redirect(url_for("multilingual.filteringRules"))


@multilingual.route('/guvenlikDuvari/filtrele/filtreDuzenle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/firewall/filterRule/editfilter', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def filteringEditRules():
    if request.method == "POST":
        global id
        id = request.form["EditFilter"]
        global oldRule
        oldRule = fetchInfo("id", id, "filterTable")
        return render_template('multilingual/filteringRulesEdit.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchInfo("id", id, "filterTable"))


@multilingual.route('/firewall/filterRule/editfilterButton', methods=['GET', 'POST'])
def filteringEditButtonRules():
    if request.method == "POST":
        if(request.form["protocol"] == "icmp" or request.form["protocol"] == "ALL"):
            updateFilter(request.form["filterName"], request.form["protocol"], request.form["sourceAdress"],
                         " ", request.form["destinationAdress"], " ", request.form["filterAction"], id)
            print(iptables.DellRule(oldRule))
            os.system(iptables.DellRule(oldRule))
            print("deleted")
            os.system(iptables.addRule(request.form))
            print("added")
            os.system("iptables-save > /root/conf/rules.v4")
        else:
            updateFilter(request.form["filterName"], request.form["protocol"], request.form["sourceAdress"], request.form["sourcePort"],
                         request.form["destinationAdress"], request.form["destinationPort"], request.form["filterAction"], id)
            os.system(iptables.DellRule(oldRule))
            print(iptables.DellRule(oldRule))
            os.system(iptables.addRule(request.form))
            os.system("iptables-save > /root/conf/rules.v4")
        return redirect(url_for("multilingual.filteringRules"))


@multilingual.route('/guvelikDuvari/portYonlendirme', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/firewall/portForwarding', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def portForwarding():
    if request.method == "POST":
        if request.form["portForwards_ToDestinationAdress"].split(":")[1]=="":
            flash(
                "Please enter correct internal address.Write spesific port!(X.X.X.X:<portNumber>)")
            return redirect(url_for("multilingual.portForwarding"))
        addPortForwad(request.form["portForwardingName"], request.form["portForwards_DestinationPort"],
                      request.form["portForwards_ToDestinationAdress"])
        iptables.addPortForward(request.form)
        print("Port Forwarding Rule Added!")
        return redirect(url_for("multilingual.portForwarding"))

    if request.method == "GET":
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/portForwards.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchAllData("PortForwardTable"))


@multilingual.route('/firewall/portForwarding/deletePortForwadingRule', methods=['GET', 'POST'])
def portForwardingDelete():
    if request.method == "POST":
        ruleFromSQL = fetchInfo(
            "id", request.form["DeletePortForwardRule"], "PortForwardTable")
        deleteSqlFunc(
            request.form["DeletePortForwardRule"], "PortForwardTable", "id")
        iptables.DellPortForward(ruleFromSQL)
    return redirect(url_for("multilingual.portForwarding"))


@multilingual.route('/guvelikDuvari/portYonlendirme/duzenlePortYonlendirme', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/firewall/portForwarding/editPortForwards', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def editPortForwards():
    if request.method == "POST":
        global portForwardID
        portForwardID = request.form["EditPortForwards"]
        global oldRulePF
        oldRulePF = fetchInfo("id", portForwardID, "PortForwardTable")
        print(oldRulePF)
    return render_template('multilingual/portForwardsEditPage.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchInfo("id", portForwardID, "PortForwardTable"))


@multilingual.route('/firewall/portForwarding/editButtonPortForwards', methods=['GET', 'POST'])
def editButtonPortForwards():
    if request.method == "POST":
        if len(request.form["portForwards_ToDestinationAdress"].split(":")) < 2:
            flash("Please enter correct ToDestinationAddress.Write spesific port!")
            return redirect(url_for("multilingual.portForwarding"))
        updatePortForward(request.form["portForwardingName"], request.form["portForwards_DestinationPort"],
                          request.form["portForwards_ToDestinationAdress"], portForwardID)
        iptables.DellPortForward(oldRulePF)
        iptables.addPortForward(request.form)
        print("edited")
    return redirect(url_for("multilingual.portForwarding"))


@multilingual.route('/firewall/networkBridge', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route("/guvenlikDuvari/agKoprule", defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def networkBridge():
    if request.method == "GET":  
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/bridge.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchAllData("bridgeTable"))
    if request.method == "POST":
        print(request.form)
        if fetchInfo("name", request.form["bridgeName"], "bridgeTable") != None:
            flash(
                "Device "+request.form["bridgeName"]+" already exists; can't create bridge with the same name")
            return redirect(url_for("multilingual.networkBridge"))
     
        # Interface başında boşluk var !! ( eth1)
        a = fetchInfo("interfaces", " eth0", "bridgeTable")
        b = fetchInfo("interfaces", " eth1", "bridgeTable")
        c = fetchInfo("interfaces", " eth0 eth1", "bridgeTable")
  
        if a == None and b == None and c == None:  # Flash messages bridge
            bridge.addbridge(request.form) 
            print("hiçbiri yoksa birini ekle ")
        elif a == None and b==None:
            bridge.addbridge(request.form)    
            print("c yi ekle ekledi ")  
        elif c != None and (b!=None or a!=None):
            bridge.addbridge(request.form)    
            print("eth1 ekledi ")       
        elif c == None and b==None:
            bridge.addbridge(request.form)    
            print("eth1 ekledi ")   
        else:
            flash(
                "Device eth is already a member of a bridge; can't enslave it to bridge.")
            return redirect(url_for("multilingual.networkBridge"))
        return redirect(url_for("multilingual.networkBridge"))


@multilingual.route('/firewall/networkBridge/deleteBridge', methods=['GET', 'POST'])
def deleteBridge():
    if request.method == "POST":
        ruleFromSQL = fetchInfo(
            "id", request.form["DeleteBridgeRule"], "bridgeTable")
        print(ruleFromSQL)
        bridge.delBridge(ruleFromSQL)
        return redirect(url_for("multilingual.networkBridge"))


@multilingual.route('/logsView', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route('/logSayfasi', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def logview():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
    return render_template('multilingual/logsView.html', userInfo=session['username'], auth=getAuth(session['username']), logs=journalctl.journalctl())


@app.route('/downloadlog', methods=['GET', 'POST'])
def downloadlog():
    os.popen("rm -rf /root/logs.txt")
    os.popen("journalctl --output=short > /root/logs.txt")
    sleep(16)
    path = os.path.join(
        app.config['UPLOAD_FOLDER'], "logs.txt")
    print(path)
    return send_file(path, as_attachment=True)


@multilingual.route('/connection', methods=['GET', 'POST'])
def webguiconnection():
    if request.method == 'GET':
        if soc.dataType0 != None:
            print("Connected TCP SOCKET")
            return jsonify('', render_template('multilingual/webguiConnection.html', state="Connected"))
        else:
            print("Not Connected!")
            return jsonify('', render_template('multilingual/webguiConnection.html', state="Not Connected"))


@multilingual.route('/syslogServer', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route('/syslogSunucu', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def syslog():
    if request.method == 'GET':
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/syslog.html', userInfo=session['username'], syslogIp=syslogFunc.syslogRead()[5:], auth=getAuth(session['username']))
    if request.method == 'POST':
        try:
            sysIp = request.form['syslogIP']
            ipaddress.ip_address(sysIp)
            syslogFunc.syslogRead()
            syslogFunc.syslogFormatter(sysIp)
            return render_template('multilingual/syslog.html', userInfo=session['username'], syslogIp=syslogFunc.syslogRead()[5:], auth=getAuth(session['username']))
        except:
            flash('Invalid IP format!')
            return render_template('multilingual/syslog.html', userInfo=session['username'], syslogIp=syslogFunc.syslogRead()[5:], auth=getAuth(session['username']))


@multilingual.route('/güvenlikDuvari/nat', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/firewall/nat', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def natSettings():
    if request.method == "GET":
        try:
            session['username']
        except:
            return redirect('/')
        return render_template('multilingual/natSettings.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchAllData("natTable"))
    if request.method == "POST":
        if(request.form["natAction"] == "SNAT"):
            addNatRule(request.form["RuleName"], request.form["outbound"],
                       request.form["sourceAdress"], request.form["toSourceAddress"], request.form["natAction"])
            iptables.natRule(request.form)
        if(request.form["natAction"] == "MASQUERADE"):
            addNatRule(request.form["RuleName"], request.form["outbound"],
                       request.form["sourceAdress"], " ", request.form["natAction"])
            iptables.natRule(request.form)
        return redirect(url_for("multilingual.natSettings"))


@multilingual.route('/firewall/nat/deleteNat', methods=['GET', 'POST'])
def natDeleteRules():
    if request.method == "POST":
        fetchRule = fetchInfo("id", request.form["DeleteNat"], "natTable")
        iptables.deleteNat(fetchRule)
        deleteSqlFunc(request.form["DeleteNat"], "natTable", "id")
        return redirect(url_for("multilingual.natSettings"))


@multilingual.route('/firewall/nat/natKuralDuzenle', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
@multilingual.route('/firewall/nat/editNatRule', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
def editNatRule():
    if request.method == "POST":
        global id
        id = request.form["EditNat"]
        global oldRule
        oldRule = fetchInfo("id", id, "natTable")
        return render_template('multilingual/natEditPage.html', userInfo=session['username'], auth=getAuth(session['username']), filters=fetchInfo("id", id, "natTable"))


@multilingual.route('/firewall/nat/natEditButtonRules', methods=['GET', 'POST'])
def natEditButtonRules():
    if request.method == "POST":
        if(request.form["natAction"] == "SNAT"):
            updateNat(request.form["RuleName"], request.form["outbound"],
                      request.form["sourceAdress"], request.form["toSourceAddress"], request.form["natAction"], id)
            if oldRule[4] == "SNAT":
                iptables.deleteNat(oldRule)
                print("deleted")
                iptables.natRule(request.form)
                print("added")
        else:
            updateNat(request.form["RuleName"], request.form["outbound"],
                      request.form["sourceAdress"], "-", request.form["natAction"], id)
            iptables.deleteNat(oldRule)
            print("deleted")
            iptables.natRule(request.form)
            print("added")
        return redirect(url_for("multilingual.natSettings"))


sendToClient = 0


@multilingual.route('/blockparameters', defaults={'lang_code': 'en'}, methods=['GET', 'POST'])
@multilingual.route('/blokparametreleri', defaults={'lang_code': 'tr'}, methods=['GET', 'POST'])
def webgui():
    try:
        session['username']
    except:
        return redirect('/')
    if request.method == 'GET':
        print(soc.dataType0)
        return render_template('multilingual/blockparameters.html', dataType0=soc.dataType0, userInfo=session['username'], auth=getAuth(session['username']))

# Block parameters left table


@app.route('/webguivalue', methods=['POST'])
def update():
    if request.method == 'POST':
        return jsonify('', render_template('multilingual/webguivalue.html', dataType0=soc.dataType0))
    return "Not Connected!", 29


@multilingual.route('/webguivalue3', defaults={'lang_code': "en"}, methods=['POST', 'GET'])
@multilingual.route('/webguideger3', defaults={'lang_code': "tr"}, methods=['POST', 'GET'])
def webguivalue3():
    if request.method == 'GET':
        return render_template('multilingual/webguivalue3.html', dataType0=soc.dataType0)
    if request.method == 'POST':
        updateData = [{
            'BlockLineLabel': soc.dataType0[int(request.form['index'])]['BlockLineLabel'],
            'BlockNumber': soc.dataType0[int(request.form['index'])]['BlockNumber'],
            'BlockType': soc.dataType0[int(request.form['index'])]['BlockType'],
            'BlockValue': float(request.form['value']),
            'DataType': soc.dataType0[int(request.form['index'])]['DataType'],
        }]
        global sendToClient
        print(type(request.form['value']))
        sendToClient = json.dumps(updateData)
        print(sendToClient)
        return redirect(url_for("multilingual.webgui"))
# Index page network status cards


@app.route('/refreshTime', methods=['GET', 'POST'])
def refreshTime():
    if request.method == 'GET':
        return jsonify('', render_template('Div_systemTime.html', time=statuspage.getTime()))


@app.route('/refreshRam', methods=['GET', 'POST'])
def refreshRam():
    if request.method == 'GET':
        return jsonify('', render_template('Div_ramUsage.html', ramUsage=statuspage.ramUsage()))


@app.route('/refreshVersion', methods=['GET', 'POST'])
def refreshVersion():
    if request.method == 'GET':
        return jsonify('', render_template('Div_statusversion.html', firmware=soc.dataTypeATVERSION))


@app.route('/gsmcard', methods=['GET', 'POST'])
def gsmcard():
    if request.method == 'GET':
        return jsonify('', render_template('networkGsmStatus.html', gsmIP=statuspage.grepGSMip(), ATBAND=soc.dataTypeATBAND, ATCSQ=soc.dataTypeATCSQ))


@app.route('/refreshGSMStatus', methods=['GET', 'POST'])
def refreshGSMStatus():
    if request.method == 'POST':
        ATLOCAL = [{
            "MessageType": "ATCommandData",
            "AtCommand": "AT+VERSION=?\r",
        }]
        global sendToClient
        sendToClient = json.dumps(ATLOCAL)
        sleep(1)
        ATBAND = [{
            "MessageType": "ATCommandData",
            "AtCommand": "AT+BAND=?\r",
        }]
        sendToClient = json.dumps(ATBAND)
        sleep(1)
        ATCSQ = [{
            "MessageType": "ATCommandData",
            "AtCommand": "AT+CSQ=?\r",
        }]
        sendToClient = json.dumps(ATCSQ)
        return 'ATCOMMANDS'


@app.route('/refreshCard/<cardName>', methods=['GET'])
def refreshCard(cardName):
    if request.method == 'GET':
        if cardName == 'eth0':
            return jsonify('', render_template('networkstatusETH0.html', dataType1=soc.dataType2, netstatus=statuspage.interfaceControl()))
        if cardName == 'eth1':
            return jsonify('', render_template('networkstatusETH1.html', dataType1=soc.dataType2, netstatus=statuspage.interfaceControl()))
        if cardName == 'wlan0':
            return jsonify('', render_template('networkstatusWLANcard.html', dataType1=soc.dataType2, netstatus=statuspage.interfaceControl()))


@app.before_first_request  # runs before FIRST request (only once)
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


if __name__ == '__main__':
    app.debug = True
    socketObject = socTh()
