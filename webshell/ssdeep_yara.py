#!/usr/bin/env python
# coding: utf-8
# author : I

import gevent
from gevent import monkey,Greenlet; monkey.patch_all()   #18.18s vs 17s what hells going on ?
import subprocess
import re,os
import csv,json



def yara(rule_path,dir_path):
    """ 
        注意，yara取决于rule，经在wordpress上的测试，发现误报率，很高。。。。。所以这个作为白名单过滤后的使用还可以，否则就不行了。
        取决于规则的写法，所以返回的type也会不同，todo: 抽取feature，or 手写 or 用GAN生成？？？不太现实吧。
                                                                                                    """

    # 不是一种好的写法
    yara_sec_type = ['wordpress','Owncloud','Phpmyadmin','Misc','Magento2','Magento','Prestashop','Symfony','Drupal','Roundcube','Concrete5','Dotclear']
    yara_dan_type = ['DangerousPhp','HiddenInAFile','DodgyPhp','PasswordProtection','ObfuscatedPhp','NonPrintableChar','SuspiciousEncodi','DodgyStrings']                                                                                                
    p = subprocess.Popen(['yara','-r',rule_path, dir_path] , stdout=subprocess.PIPE)
    a = p.stdout.read().decode('utf8')
    funny_res = []

    if len(funny_res) == 1 and funny_res[0].file_name == '':
        # tmp = {'file_type': r.findall(_)[0], 'file_path':file_path,'file_name':file_name}
        # return tmp
        return None
    else:
        
        tmp = {}
        r = re.compile('^[a-zA-Z]{0,16}')
        for _ in a.split('\n'):
            # 将第一个空格之后的一切作为abs路径和文件名，重新进行路径切割，避免文件名空格导致切分错误
            file_path,file_name = os.path.split(''.join(_.split(' ')[1:]))
            file_type = r.findall(_)[0]
            if file_type in yara_sec_type:
                file_type = 'Safe'
            elif file_type in yara_dan_type:
                file_type = 'Dangerous'   

            tmp={'file_type': file_type , 'file_path':file_path,'file_name':file_name}
            funny_res.append(tmp)

    #　由于可能出现yara多条规则命中一个文件造成的重复现象，所以此处进行去重。顺便删除空的
        res = []
        nullinfo = {'file_type': '', 'file_path': '', 'file_name': ''}
        tl = [str(r) for r in funny_res]
        for  record in set(tl):
            n = eval(record)
            if n != nullinfo:
                res.append(n)
        return res

def ssdeep(rule_path,dir_path):
    # ssdeep -bsm  /home/mour/working/data/ssdeep/php.ssdeep  -r ./php -t 75 -c
    p = subprocess.Popen(['ssdeep','-m',rule_path,'-r',dir_path,'-t','45','-c'] , stdout=subprocess.PIPE)
    a = p.stdout.read().decode('utf8')
    
    funny_res = []
    tmp = {}

    import platform
    if platform.system() == 'Linux':
        reader = csv.reader(a.split('\n'), delimiter=',')
        for row in reader:
            if len(row) != 0:
                if int(row[-1]) <= 50 :
                    file_type = 'Safe'
                elif int(row[-1]) >= 85 :
                    file_type = 'Dangerous'
                else:
                    file_type = 'Doubt'
                file_path,file_name = os.path.split(row[0])
                tmp = {'file_type': file_type, 'file_path':file_path,'file_name':file_name }
                funny_res.append(tmp)
            else:
                pass
    elif platform.system() == 'Windows':
        #Windows下ssdeep的输出不一样，根本不能输出csv格式
        reader = csv.reader(a.split('\n'), delimiter=' ')
        for row in reader:
            if len(row) != 0:
                prop = row[-1].strip('()')
                if int(prop) <= 50 :
                    file_type = 'Safe'
                elif int(prop) >= 85 :
                    file_type = 'Dangerous'
                else:
                    file_type = 'Doubt'
                tmp = {'file_type': file_type, 'file_path':row[0],'file_name':row[-2].strip('./') }
                funny_res.append(tmp)
            else:
                pass


    
    res = []
    nullinfo = {'file_type': '', 'file_path': '', 'file_name': ''}
    for  record in funny_res:
        if nullinfo != record:
            res.append(record)
    return res

def test():
    import time
    start = time.time()
    res = yara('/home/mour/resoures/php-malware-finder/php-malware-finder/php.yar','/home/mour/resoures/webshell-sample/php')
    end = time.time()
    print("Totally time is : ",end - start)

    # for item in res:
    #     print(item)

    import time
    start = time.time()
    res2 = ssdeep('/home/mour/working/data/ssdeep/php.ssdeep','/home/mour/resoures/webshell/php')
    end = time.time()
    print("Totally time is : ",end - start)

    # for item in res2:
    #     print(item)

def test_gevent():
    import time
    start = time.time()
    thread1 =  gevent.spawn(yara,'/home/mour/resoures/php-malware-finder/php-malware-finder/php.yar','/home/mour/resoures/webshell-sample/php')
    thread2 = gevent.spawn(ssdeep,'/home/mour/working/data/ssdeep/php.ssdeep','/home/mour/resoures/webshell/php')
    gevent.joinall([thread1,thread2])
    end = time.time()
    print("Totally time is : ",end - start)

if __name__ == '__main__':
    test()
    test_gevent()
# test() is same to the test_gevent
    