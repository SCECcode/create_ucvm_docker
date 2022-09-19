# Set Mac IP address
IP=`ifconfig -l | xargs -n1 ipconfig getifaddr`

echo "Remember to run : xhost - "$IP
# Allow connections from Mac to XQuartz
/opt/X11/bin/xhost + "$IP"

docker run --platform linux/amd64 --rm -it -e DISPLAY=$"${IP}:0"  --mount type=bind,source="$(pwd)"/target,destination=/app/target sceccode/ucvm_227_cvms5:latest

/opt/X11/bin/xhost - "$IP"


