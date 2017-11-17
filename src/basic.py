"""
    In This Project, All Filename was mean the file with full path 
"""

import hashlib
import os
import util
import configparser
import detect as dt
import codecs
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CONFIGFILEPATH = os.path.abspath('../config.ini')
fileparser = configparser.ConfigParser ()
fileparser.read(CONFIGFILEPATH)
print("Please Make Sure Your Config File Was Placed In : ",bcolors.WARNING,CONFIGFILEPATH,bcolors.ENDC)

def allowed_file_type(fileparser):
    pass

def convert(filename,tmpfile):
    with codecs.open(filename, 'r', 'utf-16') as infile:
        with codecs.open(tmpfile, 'w', 'utf-8') as outfile:
            for line in infile.readlines():
                if not re.match(r'^\s*$', line):
                    outfile.writelines(line)

class BasicFile:
    """
        You need init it with a full path filename
    """
    def __init__(self,filename):

        self.Filename = filename
        self.FileSize = self.filesize()
        self.FilePath = self.filepath()
        self.FileOSStat = util.get_file_os_stat(filename)

        self.FileTimeStamp = {
            'create_time' : self.FileOSStat.get('st_ctime'),
            'access_time' : self.FileOSStat.get('st_atime'),
            'modified_time' : self.FileOSStat.get('st_mtime')
        }

        self.FileOwner = self.FileOSStat.get('st_uid')
        self.FileGroupOwner = self.FileOSStat.get('st_gid')

        self.Suffix =  self.suffix()
        self.Operation = util.get_file_os_operation(filename)

        self.MD5 = self.md5sum()
        # self.FuzzyHash = self.fuzzyhash()
        self.SHA1 =self.sha1sum()

        self.SsdeepPath , self.YaraPath = util.ssdeep_yara_path()
        self.SsdeepFeaturesPath, self.YaraRulePath, = util.features_rurles_path(fileparser)


        self.YaraHit = self.yarahit()
        self.SsdeepHit = self.ssdeephit()
        self.Result = self.computer()

    def filepath(self):
        return os.path.abspath((self.Filename))

    def filesize(self):
        return os.path.getsize(self.Filename)
        
    def suffix(self):
        """
            Did any good answer?
        """
        if self.FileOSStat.get('st_ftype') is not None:                 #sf_type only in RISCOS system
            return self.FileOSStat.get('st_ftype')

        sf = os.path.splitext(self.Filename)
        if len(sf) > 1:
            return sf[1]
        else:
            return None

    # @classmethod                         Q: """为什么此处不能使用classmethod,否则会显示找不到文件"""
    def md5sum(self):
        return hashlib.md5(open(self.Filename,'rb').read()).hexdigest()

    def sha1sum(self):
        return hashlib.sha1(open(self.Filename,'rb').read()).hexdigest()        


    # def fuzzyhash(self):
    #     pass

    def ssdeephit(self):

        method =  dt.DetectStrategy(dt.execute_ssdeepmatch_features)
        method.filename = self.Filename
        method.ssdeep_path = self.SsdeepPath
        method.features_path = self.SsdeepFeaturesPath
        return method.execute()
        
    def yarahit(self):

        method = dt.DetectStrategy(dt.execute_yaramatch_rules)
        method.filename = self.Filename
        method.yara_path = self.YaraPath
        method.rules_path = self.YaraRulePath
        return method.execute()

    def computer(self):
        """
            Logical judgement, Check 
            * Most Important is How to  Return The Source Name(example: APT32, APT45)
        """
        if self.SsdeepHit is True or self.YaraHit is True: 
            return True

# def main():
#     test = BasicFile('./tmp.txt')
#     print(test.Filename)
#     print(test.FilePath)
#     print(test.MD5)
#     print(test.SHA1)
#     print(test.Suffix)
#     print(test.FileCreateTime)
#     print(test.FileAccessTime)
#     print(test.FileModifiedTime)
#     print(test.Operation)
#     print(test.FileTimeStamp)
#     print(test.ssdeephit())
#     print(test.yarahit())

# if __name__ == '__main__':
#     main()