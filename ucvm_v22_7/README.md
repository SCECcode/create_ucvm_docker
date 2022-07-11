# To build
In this directory
clone the most recent version of ucvm. It will create a subdirectory called ucvm


## Run Cmd:
docker run --rm -it --mount type=bind,source="$(pwd)"/target,destination=/app/target  ucvm:1345

This is a coding and configuration test for creating a UCVM docker image that can be run on AWS.

## .dockerignore file
There is a .dockerignore file that defines which files not to include in the image. The Dockerfile and this README.md are excluded.

## Dockerfile
This lists the steps needed to build the container.

## Contents of large_file_inputs
(base) [maechlin@discovery2 largefiles]$ ./get_largefiles.py 
Running in ./largefiles source directory. 
This script will download and install ucvm.e, ucvm_utah.e and several other files.
Due to the size of the files, this download could take minutes to hours to complete.
Would you like to download cvms5, will need 1.2G?
Enter yes or no: yes
Would you like to download cca, will need 9.2G?
Enter yes or no: no
Would you like to download cs173, will need 72G?
Enter yes or no: no
Would you like to download cs173h, will need 72G?
Enter yes or no: no
Would you like to download cvms, will need 326M?
Enter yes or no: yes
Would you like to download cvmsi, will need 1.6G?
Enter yes or no: yes
Would you like to download cencal, will need 21G?
Enter yes or no: no
Would you like to download cvmh, will need 1.6G?
Enter yes or no: yes
Would you like to download albacore, will need 2.3M?
Enter yes or no: yes
Would you like to download cvlsu, will need 7.0M?
Enter yes or no: yes
Would you like to download ivlsu, will need 3.1M?
Enter yes or no: yes
Would you like to download wfcvm, will need 50M?
Enter yes or no: yes
