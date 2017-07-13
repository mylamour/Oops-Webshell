#!/usr/bin/env bash

#
#	Attation: ssdeep can't find a one word webshell, because it's not able to compute the fuzzy hash,
#	so we can only use it to check the different webshell 
#	You can use : process to generator the feature database was named ssdeep.features
#	also use the fuzzy_check_hash_webshell to check the probability of the target
#   webshell path only was used for the first playing 

features="php jsp asp"
webshell_path='../../../resoures/webshell'
check_path='your path here'


process()
{
for suffix in $features
do
	
	echo "Now we would generator the $suffix features file "
	find  $webshell_path -type f -name "*$suffix*" -exec ssdeep -b {} \; > $suffix.ssdeep 2>/dev/null

	echo "Delete Blank line and repeated promot"
	sed -i '/ssdeep,1.1--blocksize:hash:hash,filename/d' $suffix.ssdeep 
	# if use 2>&1 you should uncomment the line	
	#sed -i '/ssdeep: Did not process files large enough to produce meaningful results/d'  $suffix.ssdeep                   
	sed -i '/^$/d' $suffix.ssdeep

	echo "Insert a new promot line"
	sed -i '1 issdeep,1.1--blocksize:hash:hash,filename' $suffix.ssdeep

	echo "$suffix was processed :  Done"
done

	echo "Combine to one features"
	cat $(ls *.ssdeep) > ssdeep.features	
}

fuzzy_check_hash_webshell()
{
	for suffix in $features
	do
		find $check_path -type f -exec ssdeep -t 80 -bm $suffix.ssdeep {} \; > $suffix.res.test.check 2>/dev/null &
		# Also there another way to use ssdeep. Just use flag -r to recurisve the directory file
		# ssdeep -bsm  /home/mour/working/data/ssdeep/php.ssdeep  -r ./php -t 75 -c
	done
	
	find $check_path -type f -exec ssdeep -t 80 -bm ssdeep.features {} \; > all.res.test.check 2>/dev/null &
}

fuzzy_check_hash_webshell



