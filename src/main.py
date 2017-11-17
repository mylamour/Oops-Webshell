
import gevent

import os
import pathlib
import subprocess
from basic import BasicFile
from fileinfo.logfile import LogFile

def executefrompsfile(psfile,functionin):
    subprocess.call(["powershell.exe",'-ExecutionPolicy',
                             'Unrestricted',". \"{}\";".format(psfile),  "&{}".format(functionin)])

# check config path and outputdatapath
def initpath():
    # if os.path.exists(os.path.abspath('../conf')):
    #     os.rmdir('../conf')
    # if os.path.exists(os.path.abspath('./fileinfo/data')):
    #     os.rmdir('./fileinfo/data')
    pathlib.Path(os.path.abspath('./fileinfo/data/Account')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('./fileinfo/data/Log')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('./fileinfo/data/Network')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('./fileinfo/data/Process')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('./fileinfo/data/Registry')).mkdir(parents=True, exist_ok=True)

    pathlib.Path(os.path.abspath('../conf/blacklist')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('../conf/whitelist')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('../conf/features')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('../conf/model')).mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.abspath('../conf/rules')).mkdir(parents=True, exist_ok=True)

def initoutput():
    # Need Mutil Thread
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Net")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-PP")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Log")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Service")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-AccountInfo")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Net")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-FileAndDirectory")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Reg")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Evt")
    executefrompsfile(os.path.abspath('../lib/wininfo.ps1'), "MGet-Service")

def processfilefrom():
    # test = BasicFile('../lib/SecurityLog.csv')
    # test.computer()

    # First Should Execute Powershell Script or manualy by yourself
    # we can add a opition select to do this 
    # From Python To Use Powershell Function
    LogFile_SEC = LogFile(os.path.abspath('./fileinfo/data/Log/SecurityEventLog.csv'))
    LogFile_SEC.computer()
    # Use GreenLets Todo This Thing, or Cutom by Self, Use Yield From

    # LogFile_NET = LogFile(os.path.abspath('./'))
    # LogFile_NET.computer()

    # LogFile_SYSTEM = LogFile(os.path.abspath('./'))
    # LogFile_SYSTEM.computer()

    # LogFile_MpThreatDetection = LogFile(os.path.abspath('./'))
    # LogFile_MpThreatDetection.computer()
    
    # Account_USER = LogFile(os.path.abspath('./'))
    # Account_USER.computer()

    # Account_GROUP = LogFile(os.path.abspath('./'))
    # Account_GROUP.computer()

    # Account_SYSTEM = LogFile(os.path.abspath('./'))
    # Account_SYSTEM.computer()

def processsimple():
    # Just use yara to hit the extracted file
    # Or Simply filter by whitelist/blacklist and somthing else
    # For example,
    #    1.use yara scan Disk by APT Rules, IOCS.
    #    2.use yara scan Extracted Files bt Apt Rules, IOCS, And So on.(extracted file was included the process list and dnscache)
    pass

if __name__ == '__main__':
    # Options Select
    pass