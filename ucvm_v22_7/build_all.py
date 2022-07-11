#!/usr/bin/env python3
# This script is used to update the inputs models and generate new docker build scripts for each configuration
#

import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # build date tag
    mdate = "0710"

    models = ["cvms5",
              "cca",
              "cvms",
              "cvmsi",
              "cencal",
              "cvmh"]
"""

    models = ["cvms5",
              "cca",
              "cvms",
              "cvmsi",
              "cencal",
              "cvmh",
              "albacore",
              "cvlsu",
              "ivlsu",
              "wfcvm",
              "cvmhlabn cvmhsgbn cvmhvbn cvmhibbn cvmhrbn cvmhstbn cvmhsbbn cvmhsbcbn cvmhsmbn"]


    for m in models:
        print ("building model: " + m)
        cmd = "docker build --no-cache=false -f Dockerfile . -t ucvm_227_%s:%s " \
            "--build-arg APP_UNAME=`id -u -nr` --build-arg APP_GRPNAME=`id -g -nr` " \
            "--build-arg APP_UID=`id -u` --build-arg APP_GID=`id -g` --build-arg MODELID=%s --build-arg BDATE=%s"%(m,mdate,m,mdate)

        os.system(cmd)

        cmd = "docker tag ucvm_227_%s:%s sceccode/ucvm_227_%s:%s"%(m,mdate,m,mdate)
        os.system(cmd)
"""

    for m in models:
        print("pushing models: " + m)
        cmd = "docker push sceccode/ucvm_227_%s:%s"%(m,mdate)
        os.system(cmd)
