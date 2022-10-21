import os 
def syslogRead():
    global a
    a=os.popen("grep -E '@[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' /etc/syslog.conf").read()
    return a

def syslogFormatter(syslogIp):   
    if(len(a)>0):
        print("Syslog server's ip aldready exists in configuration file.Changing...") 
        os.system("sed -r -i 's/^\*\.\* @([0-9]{1,3}\.){3}[0-9]{1,3}/*.* @"+syslogIp+"/g' /etc/syslog.conf")      
        os.system("systemctl restart syslog")
        print("Syslog service restarted.")            
    else:
        print('There is no syslog ip! Adding confiration file.')
        os.system("echo '*.* @"+syslogIp+"' >> /etc/syslog.conf")
        os.system("systemctl restart syslog")
        print("Syslog service restarted.")    

def enableMod():
    print("Syslog disabled!")
    os.system("sed -r -i 's/^\*\.\* @([0-9]{1,3}\.){3}[0-9]{1,3}//g' /etc/syslog.conf")
    os.system("systemctl restart syslog")



