#!/bin/bash

## special case check for M1
if [[ $(uname -m) == 'arm64' ]]; then
  docker run --platform=linux/amd64 --rm -it -e APP_UNAME=ucvmuser -e APP_GRPNAME=`id -g -nr` -e APP_UID=`id -u` -e APP_GID=`id -g` --mount type=bind,source="$(pwd)"/target,destination=/app/target sceccode/ucvm_227_cvms5:latest
else
  docker run --rm -it -e APP_UNAME=ucvmuser -e APP_GRPNAME=`id -g -nr` -e APP_UID=`id -u` -e APP_GID=`id -g` --mount type=bind,source="$(pwd)"/target,destination=/app/target sceccode/ucvm_227_cvms5:latest
fi

