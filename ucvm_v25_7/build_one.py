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

#        cmd = "docker build --no-cache -f Dockerfile . -t ucvm_257_%s:%s " \

    for m in models:
        print ("building model: " + m)
        cmd = "docker build --no-cache -f Dockerfile . -t ucvm_257_%s:%s " \
            "--build-arg APP_UNAME=ucvmuser --build-arg APP_GRPNAME=ucvmuser " \
            "--build-arg APP_UID=1000 --build-arg APP_GID=1000 --build-arg MODELID=%s --build-arg BDATE=%s"%(m,mdate,m,mdate)
        os.system(cmd)
#        cmd = "docker tag ucvm_257_%s:%s sceccode/ucvm_257_%s:%s"%(m,mdate,m,mdate)
#        os.system(cmd)

#    for m in models:
#        print("pushing models: " + m + " with sceccode/ucvm_257_%s:%s" % (m,mdate))
#        cmd = "docker push sceccode/ucvm_257_%s:%s" % (m,mdate)
#        cmd = "docker push sceccode/ucvm_257_%s:latest" % (m)
#        os.system(cmd)
