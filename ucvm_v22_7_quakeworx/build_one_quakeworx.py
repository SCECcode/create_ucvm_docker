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

    models = ["cvmh"]

    for m in models:
        print ("building model: " + m)
        cmd = "docker build --no-cache=false -f Dockerfile . -t ucvm_227_%s_quakeworx:%s " \
            "--build-arg APP_UNAME=ucvmuser --build-arg APP_GRPNAME=`id -g -nr` " \
            "--build-arg APP_UID=1000 --build-arg APP_GID=1000 --build-arg MODELID=%s --build-arg BDATE=%s"%(m,mdate,m,mdate)
    
        os.system(cmd)

        cmd = "docker tag ucvm_227_%s_quakeworx:%s sceccode/ucvm_227_%s_quakeworx:latest"%(m,mdate,m)
        os.system(cmd)

        print("pushing models: " + m + " with sceccode/ucvm_227_%s_quakeworx:%s" % (m,mdate))
        cmd = "docker push sceccode/ucvm_227_%s_quakeworx:latest" % (m)
        os.system(cmd)
