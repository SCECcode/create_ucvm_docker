# -rm removes container on exit
# -it indicates inteactive + --tty so that users are at an interactive tty command line when the container starts
docker run -p 8888:8888 --rm -it --mount type=bind,source="$(pwd)"/target,destination=/home/ucvmuser/target sceccode/ucvm_227_jup_cvmh:latest
