#!/usr/bin/env python
# coding: utf-8
# author : I

import subprocess
import re,os
import csv,json
import platform

plat = platform.system()

import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

yara_sec_type = [ item for item in config['yara']['yara_sec_type'].split(',')]
yara_dan_type = [item for item in config['yara']['yara_dan_type'].split(',')]


def descriptionoutput(s):
    # cao = list(map(lambda x: hex(int(x, 8)), s.split("\\")[1:]))
    """ 
        due to yara can't display Non-Ascii, we need format description to utf-8 
    """

    return bytearray([int(x, 8) for x in s.split("\\") if x]).decode("utf-8")

def check_platform_verion():
    if plat == 'Linux':
        return os.path.abspath('./webshell/bin/ssdeep'), os.path.abspath('./webshell/bin/yara')
    elif plat == 'Windows':
        return os.path.abspath('./webshell/bin/ssdeep.exe'), os.path.abspath('./webshell/bin/yara.exe')

ssdeep_path,yara_path = check_platform_verion()

def yara(rule_path,dir_path):
    """ 
        注意，yara取决于rule，经在wordpress上的测试，发现误报率，很高。。。。。所以这个作为白名单过滤后的使用还可以，否则就不行了。
        取决于规则的写法，所以返回的type也会不同，todo: 抽取feature，or 手写 or 用GAN生成？？？不太现实吧。
                                                                                                    """
    p = subprocess.Popen([yara_path,'-rm',rule_path, dir_path] , stdout=subprocess.PIPE) 
    a = p.stdout.read().decode('utf8')
    funny_res = []

    if len(a) == 0:
        return None
    else:
        
        tmp = {}
        r = re.compile('^[a-zA-Z]{0,16}')
        d = re.compile(r'\\.*\\[0-9]{3}')

        for _ in a.split('\n'):
            # 将第一个空格之后的一切作为abs路径和文件名，重新进行路径切割，避免文件名空格导致切分错误
            file_path,file_name = os.path.split(''.join(_.split(' ')[1:]))
            file_path = os.path.basename(file_path)
            file_type = r.findall(_)[0]
            description = d.findall(_)

            if len(description) > 0:
                description = descriptionoutput(description[0])

            if file_type in yara_sec_type:
                file_type = 'Safe'
            elif file_type in yara_dan_type:
                file_type = 'Dangerous'   
            tmp = {'file_type': file_type, 'file_name': file_name,
                   'detect_method': 'Yara', 'platform': plat, 'description': description}
            funny_res.append(tmp)

        # 移除最后一个输出为空的
        res = list({v['file_name']: v for v in funny_res}.values())[:-1:1]
        return res

def ssdeep(rule_path,dir_path):
    # ssdeep -bsm  /home/mour/working/data/ssdeep/php.ssdeep  -r ./php -t 75 -c
    def dangerous(prop):
        if int(prop) >= 85 :
            file_type = 'Dangerous'
        else:
            file_type = 'Doubt'
        
        description = '该文件与已知恶意文件相似度为{}'.format(prop)
        return file_type,description

    rule_path = os.path.abspath(rule_path)
    dir_path = os.path.abspath(dir_path)

    funny_res = []
    tmp = {}

    p = subprocess.Popen([ssdeep_path,'-m',rule_path,'-r',dir_path,'-t','45','-c'] , stdout=subprocess.PIPE)
    a = p.stdout.read().decode('utf8')
    reader = csv.reader(a.split('\n'), delimiter=',')

    for row in reader:
        if len(row) != 0:
            if plat == 'Linux':
                file_type, description = dangerous(row[-1])
                file_path,file_name = os.path.split(row[0])
                file_path = os.path.basename(file_path)
            elif plat == 'Windows':
                file_type, description = dangerous(row[-1].strip('()'))
                file_path = os.path.basename(row[0])
                file_name = row[-2].strip('./')

            tmp = {'file_type': file_type, 'file_name': file_name,
                   'detect_method': 'ssdeep', 'platform': plat, 'description': description}
            funny_res.append(tmp)
    res = list({v['file_name']: v for v in funny_res}.values())
    return res


def test():
    import time
    start = time.time()
    end = time.time()
    print("Totally time is : ",end - start)

    # for item in res:
    #     print(item)

    import time
    start = time.time()
    res2 = ssdeep('../lib/ssdeep/php.ssdeep','/home/mour/resoures/webshell-sample/php')
    end = time.time()
    print("Totally time is : ",end - start)

    # for item in res2:
    #     print(item)


def main():
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option("-y",  dest="yararule",
                    help="yara rule file ", metavar="FILE")
    parser.add_option("-s",  dest="ssdeepfeature",
                    help="ssdeep features file ", metavar="FILE")
    parser.add_option("-d" , dest="dirname", help="target dir")

    (options, args) = parser.parse_args()

    if options.yararule is not None and options.dirname is not None and options.ssdeepfeature is not None:
        res1 =  yara(options.yararule,options.dirname)
        res2 =  ssdeep(options.ssdeepfeature,options.dirname)
        res = res1 + res2
    elif options.yararule is not None and options.dirname is not None:
        res = yara(options.yararule,options.dirname)
        print(res)
        print(len(res))

    elif options.ssdeepfeature is not None and options.dirname is not None:
        res = ssdeep(options.ssdeepfeature,options.dirname)
        print(res)
        print(len(res))

    else:
        print('Please at least a options and a dirname')
if __name__ == '__main__':
    main()
