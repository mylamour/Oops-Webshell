"""
    doc string:
    notion: if want install basic , first install util, oh, shit
    inherit from basic was wrong, caocaocaocao
"""

import util
import basic
import os,re
import codecs

class Registry(basic.BasicFile):
    """
        Registry Parser, From Exported Registry File To Key,Value 
        And if yara_path nad yara_rules_path is Not None , we can use yara rules to match it
        else only parser it..
    """

    def __init__(self,filename,yara_path=None,yara_rules_path=None):
        super().__init__(filename)

        self.filename = filename
        self.tmpfile = None
        self.kv = self.kvenum()
        # self.tmpfile = "./{}.tmp".format(filename)                    # why, fuck idiot

        self.YaraPath = yara_path
        self.YaraRulePath = yara_rules_path

    def kvenum(self):
        self.tmpfile = "{}.regUTF_8.tmp".format(self.filename)  
        basic.convert(self.filename,self.tmpfile)
        v = self.caodan()
        return v

    def caodan(self):
        with codecs.open(self.tmpfile,'r',"utf-8") as f:                # origin registry export file was utf-16-le
            key_value = {}
            attributer_kv = {}
            key_flag = None
            flag_begin_line = None
            flag_end_line = None
            for linenumber,item in enumerate(f):
                if item.startswith('['):
                    if attributer_kv:
                        key_value.update({key_flag:attributer_kv})
                        attributer_kv = {}
                    else:
                        key_flag = item
                        key_value.update({item:'None'})
                elif '=' in item :                                       
                    if flag_begin_line != None:
                        flag_end_line = linenumber                              # linenumber + 1 -1 

                        import linecache
                        if flag_end_line - 1  == flag_begin_line:
                            _ = [i for i in linecache.getline(self.tmpfile,flag_begin_line).split("=",1)]
                        else:
                            hex_line = ''.join(linecache.getline(self.tmpfile,_).strip('\n ').replace('\\','') for _ in range(flag_begin_line,flag_end_line + 1))
                            _ = [i for i in hex_line.split("=")]
                        flag_begin_line = None
                        flag_end_line = None
                        attributer_kv.update({_[0]:_[1]})

                    if 'hex' in item:
                        flag_begin_line = linenumber + 1
                    else:
                        _ = [i for i in item.replace('\"','').strip("\n\r ").split("=",1)]

                        attributer_kv.update({_[0]:_[1]})

        return key_value

# def main():
#     test = Registry('./fileinfo/data/HKEY_USERS.reg')
#     fun = test.kvenum()
#     print(test.Filename)
#     for k,v in fun.items():
#         print(k,v)

# if __name__ == '__main__':
#     main()