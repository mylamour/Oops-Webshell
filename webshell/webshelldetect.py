#!/usr/bin/env python
# coding: utf-8
# author : I

from ssdeep_yara import ssdeep,yara
from ml.aeval import read_and_predict


"""
    when you import somehing use relative path, you need change a lot of import , How to slove it ? it' turely funny
"""

def webshelldetect(dir_path,ssdeep_php_features_path,yara_rule_path,checkpoint_path):
    """
        You must pass a diectory path was not null
    """
    res = []

    res1 = ssdeep(ssdeep_php_features_path,dir_path)
    res2 = yara(yara_rule_path,dir_path)

    # So firstly we combine the two resouce? En, It's should be. 

    # res2 include res1, beacuse yara can check every file in the directory, but ssdeep only return the match file above a value
    # for item2 in res2:
    #     if item2 in res1: # not possible, Because HeHe, i don't know how to say
    #         item2['file_type'] == res1[res1.index(item2)]['file_type']
    #     res.append(item2)

    # priority:  yara < ssdeep < ml

    for item in res1:
        try:
            if item['file_type'] == 'Doubt':
                ml_check = read_and_predict(item['file_path']+'/'+item['file_name'],checkpoint_path)
                if ml_check is None:
                    res1 = comprae_remove_item(item,res1)       # ssdeep and ml was wrong                     
                else:
                    res1[res1.index(item)] = ml_check
                    res2 = comprae_remove_item(item,res2)
            # so, any normal situtaion , we use the ssdeep as the detect result
            else:
                res2 = comprae_remove_item(item,res2)
                
        except TypeError as e:
            #{'file_type':'','file_path':'',file_name:''}
            # Also you can slice it at the first start
            # It's not need  any more, beacuse i already del the res[-1] in the ssdeep fucntion
            pass
        finally:
            pass
                
    res = res1 + res2
    return res

# There was a problem , performace!!
def comprae_remove_item(item,res):
    for _ in res:
        if item['file_name'] == _['file_name']:
            res.pop(res.index(_))
            return res
    return res
