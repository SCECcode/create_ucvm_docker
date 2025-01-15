#!/usr/bin/env python3
# This script is used to update the inputs models and generate new docker build scripts for each configuration
#

import os
import datetime

## pip install py-cpuinfo
import cpuinfo

if __name__ == '__main__':

    ## this is a bug in docker about apple's M1 chip
    cpudata = cpuinfo.get_cpu_info()['brand_raw']
    cpuname = cpudata.split(" ")[1]

    models = ["cvmhvbn",
              "cvmhsgbn"]

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

    """
    for m in models:
        print ("building model: " + m)
## special case for mac M1 chip
        if cpuname == "M1" :
          cmd = "docker build --platform=linux/amd64 --no-cache=false -f Dockerfile . -t ucvm_227_%s " \
            "--build-arg APP_UNAME=ucvmuser --build-arg APP_GRPNAME=`id -g -nr` " \
            "--build-arg APP_UID=`id -u` --build-arg APP_GID=`id -g` --build-arg MODELID=%s --build-arg BDATE=%s"%(m,m,mdate)

        print(cmd)
        os.system(cmd)
	
        print("tagging model: " + m)
        cmd = "docker tag ucvm_227_%s sceccode/ucvm_227_%s"%(m,m)
        print(cmd)
        os.system(cmd)


    for m in models:
        print ("pushing model: " + m)
        print("pushing models tags: " + m)
        cmd = "docker push sceccode/ucvm_227_%s" % (m)
        print(cmd)
        os.system(cmd)
