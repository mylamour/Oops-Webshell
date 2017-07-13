#!/usr/bin/env bash

checkpath="/home/mour/resoures/webshell/php"
modelpath="./runs/1499142849/checkpoints/"

touch /tmp/tmp.oneline

for t in $(ls -d $checkpath/*php*)
do
    echo "Now we process $t "
    flag1=`md5sum /tmp/tmp.oneline | cut -c 1-32`

    python data_process.py $t /tmp/tmp.oneline

    flag2=`md5sum /tmp/tmp.oneline | cut -c 1-32 `

    if [ "$flag1" != "$flag2" ]
        then
        python aeval.py --eval_train --checkpoint_dir=$modelpath --unknown_file="/tmp/tmp.oneline" 
    else
        echo "Next"
    fi
done 

echo "Check Over"