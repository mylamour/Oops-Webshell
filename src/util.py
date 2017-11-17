import os 
import inspect
import psutil,platform
import time
import subprocess
import json,csv

plt = platform.system()

def ssdeep_yara_path():
    if plt == 'Linux':
        return os.path.abspath('./bin/ssdeep'),os.path.abspath('./bin/yara')
    elif plt == 'Windows':
        return os.path.abspath('./bin/ssdeep.exe'),os.path.abspath('./bin/yara.exe')
    
def get_obj_result(func):
    def wrapper(*args):
        info = func(*args)
        attributes = [name for name,thing in inspect.getmembers(info) if str(name).startswith('_') is not True and str(thing).find('method') == -1]
        output = {item:getattr(info,item) for item in attributes if hasattr(info,item) is True}
        return output
    return wrapper

@get_obj_result
def get_file_os_stat(filename):
    """
    In Windows System There would be
    return:
            {'n_fields': 17, 
            'n_sequence_fields': 10, 
            'n_unnamed_fields': 3, 
            'st_atime': 1506533440.2406597, 
            'st_atime_ns': 1506533440240659700, 
            'st_ctime': 1506533440.2406597, 
            'st_ctime_ns': 1506533440240659700, 
            'st_dev': 3765395523, 'st_file_attributes': 32, 
            'st_gid': 0,
            'st_ino': 6473924464397415,
            'st_mode': 33206, 
            'st_mtime': 1505454648.4051523, 
            'st_mtime_ns': 1505454648405152300, 
            'st_nlink': 1, 
            'st_size': 4247, 
            'st_uid': 0}
    """
    
    if os.path.isfile(filename):
        a = os.stat(filename)
        return a

# print(get_file_os_stat('./test.txt'))


def get_file_os_operation(filename):
    access = {'read':os.R_OK,'write':os.W_OK,"execute":os.X_OK}
    return {k:os.access(filename,v) for k,v in access.items() if os.access(filename,os.F_OK)}

# print(get_file_os_operation('./test.txt'))

def net_timestamp(threadid=None):

    if threadid is None:
        """Get Thread Network flow"""
        pass
    else:
        """Get all Network flow"""
        pass

@get_obj_result
def get_cpu_info(threadid=None):

    if threadid == None:
        """Get All CPU Info """
        yo = psutil.cpu_stats()

        return yo
    else:
        """Get Thread CPU Info"""
        pass

# print(get_cpu_info())

def get_disk_info():
    res = []
    for _ in  psutil.disk_partitions():
        @get_obj_result
        def process():
            return _
        @get_obj_result
        def disk_useage():
            return psutil.disk_usage(_.device)   
        res.append({**process(),**disk_useage()})
    return res

# print(get_disk_info())

def get_dir_file(dirpath):
    """
        check dirpath here or ?
    """
    dir_file = []
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        for p,d,f in os.walk(dirpath):
            dir_file.append(os.path.join(p,f))
        return dir_file

def write_file(res,filename):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename,'a') as f:
        f.write(res)

def print_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


def ssdeep_threshold(number):
    """
        return type from ssdeep match score(0-100):
            if type was dangerous , return 1
            else type was doubt 
    """
    if number > 100:
        return None
    elif 85 <= number <= 100:
        return {'type': 1 }
    elif 0 <= number < 85:
        return {'type': 0}
    else:
        return None

def features_rurles_path(fileparser,conf=None):
    """
        pass pargraments conf = 'ssdeep' or conf = 'yara'
        return features path or rule path  
        if none return all
    """

    PhpRuleDirPath = fileparser.get('rule','PHP_RULE_PATH')
    AspRuleDirPath = fileparser.get('rule','ASP_RULE_PATH')
    JspRuleDirPath = fileparser.get('rule','JSP_RULE_PATH')

    PhpFeaturesPath = fileparser.get('features','PHP_FEATURES_PATH')
    AspFeaturesPath = fileparser.get('features','PHP_FEATURES_PATH')
    JspFeaturesPath = fileparser.get('features','PHP_FEATURES_PATH')
    
    yara_rule_path = {
        'PhpRuleDirPath' : PhpRuleDirPath,
        'AspRuleDirPath' : AspRuleDirPath,
        'JspRuleDirPath' : JspRuleDirPath
    }
    ssdeep_features_path = {
        'PhpFeaturesPath' : PhpFeaturesPath,
        'AspFeaturesPath' : AspFeaturesPath,
        'JspFeaturesPath' : JspFeaturesPath
    }

    if conf == 'yara':
        return yara_rule_path
    elif conf == 'ssdeep':
        return ssdeep_features_path
    elif conf is None:
        return ssdeep_features_path, yara_rule_path
    else:
        return None

def get_vmem_info():
    """
        get vmem info, time range:  2 min
        return {
            percent: [2min...],
            used: [2min...]
        }

        for: normal distribution ???
    """

    two_min = {
        'percent' : [],
        'used' : []
    }
    for i in range(1,120):
        vmem_info = psutil.virtual_memory()
        two_min['percent'].append(vmem_info.percent)
        two_min['used'].append(vmem_info.used)
        time.sleep(1)
    return two_min

# print(get_vmem_info())

def getPowerShellRes(powershllcmd, resformat='csv'):
    """
        Exec the powershell cmd ,and get res with csv format default
        -NoTypeInformation is better than Select -skip 1
    """
    allowed_format = {
        'csv' :  'ConvertTo-Csv -NoTypeInformation',
        'json': 'ConvertTo-Json'
        }

    # Due to we can't change the powershell output encoding, Get System Encoding
    encoding = subprocess.getoutput('powershell.exe [Console]::OutputEncoding.BodyName')

    if resformat.lower() in allowed_format.keys():
        ft = allowed_format.get(resformat.lower())
        cmd = 'powershell.exe {0} | {1}'.format(powershllcmd, ft)
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    res, _ = output.communicate()
    res = res.decode(encoding)
    return csv.DictReader(res.splitlines(), delimiter=",") if resformat.lower() == 'csv' else json.loads(res)

# for row in getPowerShellRes('Get-DnsClientCache'):
#     print(row)
# for row in getPowerShellRes('Get-Process'):
#     print(row)
