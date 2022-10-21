import os
def journalctl():
    commd=os.popen("journalctl --no-pager -n 100").read()
    return commd
