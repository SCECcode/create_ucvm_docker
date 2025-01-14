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

    # build date tag
    dt=datetime.datetime.today()
    month=dt.month
    day=dt.day
    mdate="%02d%02d"%(month,day)

    all_models = ["cvmh"]

    models = ["cvmh"]

    for m in models:
        print ("building model: " + m)
## special case for mac M1 chip
        if cpuname == "M1" :
          cmd = "docker build --platform=linux/amd64 --no-cache=false -f Dockerfile . -t ucvm_252_%s:%s " \
            "--build-arg APP_UNAME=ucvmuser --build-arg APP_GRPNAME=`id -g -nr` " \
            "--build-arg APP_UID=`id -u` --build-arg APP_GID=`id -g` --build-arg MODELID=%s --build-arg BDATE=%s"%(m,mdate,m,mdate)
        else:
          cmd = "docker build --no-cache=false -f Dockerfile . -t ucvm_252_%s:%s " \
            "--build-arg APP_UNAME=ucvmuser --build-arg APP_GRPNAME=`id -g -nr` " \
            "--build-arg APP_UID=`id -u` --build-arg APP_GID=`id -g` --build-arg MODELID=%s --build-arg BDATE=%s"%(m,mdate,m,mdate)
    
        os.system(cmd)

        cmd = "docker tag ucvm_252_%s:%s sceccode/ucvm_252_%s:latest"%(m,mdate,m)
        os.system(cmd)

#    for m in models:
#        print("pushing models: " + m + "with sceccode/ucvm_252_%s:%s" % (m,mdate))
#        cmd = "docker push sceccode/ucvm_252_%s:%s" % (m,mdate)
#        cmd = "docker push sceccode/ucvm_252_%s:latest" % (m)
#        os.system(cmd)
