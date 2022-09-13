
DATE=`date '+%m%d'`
docker run --rm -it -e APP_UNAME=username -e APP_GRPNAME=`id -g -nr` -e APP_UID=`id -u` -e APP_GID=`id -g` --mount type=bind,source="$(pwd)"/target,destination=/app/target ucvm_227_cvmh:$DATE
