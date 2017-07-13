#!/usr/bin/env bash

usage()
{
  (echo "Usage: $0 [options]"
   echo "Available options:"
   echo "  -h | --help                  prints this"
   echo "  -r | --run,             	specifies script opition  (default: run all images)"
   echo "  -ip,               	        specifies script poopition  (default: get containers ip)"
   echo "  -s | --stop,               	specifies script poopition  (default: stop all containers)"
   echo "  -m | --rmove,               	specifies script poopition  (default: remove containers)" 
  )
}

runcontainer()
{
	for container in $(docker images -q)
	do
		echo "Now we start a container was named: $container"
		docker run  -it -d  $container 
		# docker run --rm -it -d  $container  
	done 
}

getallip()
{
	for con in $(docker ps -aq)
	do
		docker inspect --format '{{ .NetworkSettings.IPAddress }}' $con
	done
}

stopallcontainer()
{
	echo "Now we will stop all running containers"
	docker stop $(docker ps -a -q)
}

rmallcontainer()
{	
	echo "Now, we will remove all stoped containers"
	docker rm $(docker ps -a -q)
}


while [ $# -gt 0 ]
do
  case $1 in

    -h|--help)
      usage
      exit 0
      ;;

    -r|--run)
      runcontainer
      exit 0
      ;;

    -s|--stop)
      stopallcontainer
      exit 0
      ;;

    -m|--remove)
      stopallcontainer
      rmallcontainer
      exit 0
      ;;

    -ip)
      getallip
      exit 0
      ;;
  esac
  echo "Please select a correct opitions. Also you can use --help to display it."
  exit 0 
done
