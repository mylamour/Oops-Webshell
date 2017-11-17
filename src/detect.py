import types
import re
import util
import subprocess
from collections import namedtuple

def parser_yara(output):
    # return re.findall('\w+',str(output).strip('\r\n'))
    return str(output).split()[0]

def parser_ssdeep(output):
    parsers = []
    for item in str(output).split('\r\r\n'):
        if len(item) > 0:
            matched = item.split(':')[-1]
            matchfile = matched.split()[0]
            matchscore = re.sub("\D","",matched.split()[-1])

            # print('matchfile: ', matchfile)
            # print('matchscore: ',matchscore)

            matched = {
                'file' : matchfile,
                'score' : matchscore
            }
            parsers.append(matched)
    return parsers

class DetectStrategy:

    def __init__(self,func=None):
        self.filename = None
        self.dirpath = None
        self.rules_path = None
        self.rule_flag = None       #whitelist or blacklist
        self.features_path = None
        self.model = None

        self.ssdeep_path, self.yara_path = util.ssdeep_yara_path()

        if func is not None:
            self.execute = types.MethodType(func, self)

    def execute(self):
        """
            Actucally Execut ed Strategy:
            Yara,Ssdeep,Machine Learning, (WhiteBlackList was Intergrated By Yara), InfoEntropy.
        """
        pass
    
#Attation:       strategy method must be started with the prefix named in your Strategy Class
def execute_yaramatch_rules(self):
    """
        input: filename, check whether if rules  mathced
        output: True,False
    """
    output = subprocess.Popen([self.yara_path,'-r',self.rules_path,self.filename], stdout=subprocess.PIPE)
    res, _ = output.communicate()
    if len(res) > 0 :
        return True, parser_yara(res)
    else:
        return False,None

def execute_ssdeepmatch_features(self):
    """
        input: filename, check whether if features  mathced
        output: True,False

        Note: Ssdeep is not well in APT Detect, Because Usually we don't have the malware sample or something indeed
    """
    output = subprocess.Popen([self.ssdeep_path,'-bm',self.features_path,self.filename],stdout=subprocess.PIPE)
    res, _ = output.communicate()

    if len(res) > 0:
        return True, parser_ssdeep(res)
    else:
        return False, None
    
def execute_infoentropy_computer(self):
    """
        Give me a filename, return your information entropy
    """
    pass

# load model and balabala
def execute_ml_bayes_computer(self):
    pass

def execute_ml_cnn_computer(self):
    pass

def execute_ml_fasttext_computer(self):
    pass

