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

    cmd = "docker build -t test_jupyterlab:%s ."%(mdate)
    os.system(cmd)

    cmd = "docker tag test_jupyterlab:%s mpihuisu/test_jupyterlab:latest"%(mdate)
    os.system(cmd)

    cmd = "docker push mpihuisu/test_jupyterlab:latest" 
    os.system(cmd)

