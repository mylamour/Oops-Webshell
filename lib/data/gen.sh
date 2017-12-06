ls ./rules | awk '{print "#include\"rules/" $1"\"" } ' > ./yaratestrules

echo "rule MyRuleSet"  		 >> ./yaratestrules
echo "{"		 	 >> ./yaratestrules
echo "\tcondition:"      >> ./yaratestrules



find ./rules -type f -name "*.yar" -exec cat {} \; | grep rule | awk '{print $2}' | awk '!a[$1]++' | awk '{print  "\t",$1, "or"}' | sed /^$/d | sed /^\=/d >> ./yaratestrules
echo "}"		 	 >> ./yaratestrules                                                                                                                     
