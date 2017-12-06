lynx -dump -listonly https://wordpress.org/download/release-archive > tmplink
cat tmplink | grep -e "tar.gz" | grep -v -e "md5" -e "sha1"  > link

for url in $(cat link)
do

	echo "Now Download In BackGroud" $url
	wget -q -nc $url	
done


