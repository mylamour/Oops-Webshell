#!/usr/bin/env python
# coding: utf-8
# author : I

# import os
from .ssdeep_yara import ssdeep,yara
from .ml.aeval import read_and_predict,read_and_predict_dir
import os

"""
    when you import somehing use relative path, you need change a lot of import , How to slove it ? it' turely funny
"""

def webshelldetectsingle(filepath,m_checkpoint_dir):
    
    return read_and_predict(filepath,m_checkpoint_dir)

def webshelldetect(dir_path,ssdeep_features_path,yara_rule_path,checkpoint_path):
    """
        You must pass a diectory path was not null
    """
    # never_forget = []
    # for rt, dirs, files in os.walk(dir_path):
    #     for f in files:
    #         never_forget.append(os.path.abspath(f))

    res = []
    try:
        res1 = ssdeep(ssdeep_features_path, dir_path)
    except Exception as e:
        res1 = []
    
    res2 = yara(yara_rule_path,dir_path)

    if len(res1) > 0 and len(res2) > 0:
            for item in res1:
                try:
                    if item['file_type'] == 'Doubt':
                        filepath = os.path.join(dir_path, item['file_path'],item['file_name'])
                        ml_check = read_and_predict(filepath, checkpoint_path)
                        if ml_check is None:
                            res1 = comprae_remove_item(item,res1)       # ssdeep and ml was wrong                     
                        else:
                            res1[res1.index(item)] = ml_check
                            res2 = comprae_remove_item(item,res2)
                    # so, any normal situtaion , we use the ssdeep as the detect result
                    else:
                        res2 = comprae_remove_item(item,res2)
                        
                except TypeError as e:
                    pass
                finally:
                    pass

            res = res1 + res2
            return list({v['file_name']: v for v in res}.values())
    else:
        return res2

# There was a problem , performace!!
def comprae_remove_item(item,res):
    for _ in res:
        if item['file_name'] == _['file_name']:
            res.pop(res.index(_))
            return res
    return res
