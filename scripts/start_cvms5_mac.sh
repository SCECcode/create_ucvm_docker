## for mac with X service(XQuartz)
# Set Mac IP address
IP=`ifconfig -l | xargs -n1 ipconfig getifaddr`

echo "Remember to run : xhost - "$IP
# Allow connections from Mac to XQuartz
/opt/X11/bin/xhost + "$IP"

## special case check for M1
if [[ $(uname -m) == 'arm64' ]]; then
  docker run --platform=linux/amd64 -e DISPLAY=$"${IP}:0" --rm -it --mount type=bind,source="$(pwd)"/target,destination=/app/target sceccode/ucvm_227_cvms5:latest
else
  docker run -e DISPLAY=$"${IP}:0" --rm -it --mount type=bind,source="$(pwd)"/target,destination=/app/target sceccode/ucvm_227_cvms5:latest
fi

/opt/X11/bin/xhost - "$IP"


