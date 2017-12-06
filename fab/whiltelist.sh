#!/usr/bin/env bash

#example:
#------------------------------------------------------------------------------------------------
#import "hash"
#rule wordpress
# {
#    condition:
#        /* /home/mour/working/data/wordpress/wordpress-mu-2.6.3/wp-admin */
#        hash.sha1(0, filesize) == "a677f8f321832903f361f21ff07cbbac82c132f4" or 
#        hash.sha1(0, filesize)  == "44ba7a5b685f4a52113559f366aaf6e9a22ae21e"   
# }
#------------------------------------------------------------------------------------------------

# php-malware-finder[https://github.com/nbs-system/php-malware-finder/tree/master/php-malware-finder/utils]里提供了一份白名单生成工具， python2.7执行环境 

whitelist_path="/home/mour/working/data/wordpress"
rulename="wordpress"

whitelist_generator()
{

find $whitelist_path -type f -exec sha1sum {} \; | awk '{ print $1 }' > sha1sum.txt

echo """import \"hash\"
rule $rulename
{
    condition:
"""
for filesum in $(cat sha1sum.txt)
do
    echo "      hash.sha1(0,filesize) ==" \"$filesum\" "or"
done 

echo  }


} 

whitelist_generator | tac | sed '2s/or//g' | tac > my_wordpress.yar
rm sha1sum.txt

