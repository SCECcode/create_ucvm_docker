#!/bin/env python
import sys
import os
# Define vertical profile depth and resolution
STEP = 1
START_depth = 0
END_depth = 1000

sites_dict = {
"RIDG":[-117.5,35.5],
"USC":[-118.2851,34.0224],
"s035":[-118.840210, 34.758660],
"s117":[-118.780920, 34.474230],
"WNGC":[-118.065300, 34.041824],
"LAPD":[-118.125000, 34.557000],
"s568":[-117.470700, 34.382520],
"s650":[-117.281830, 34.293160],
"SVD":[-117.098220, 34.106470],
"SBSM":[-117.292010, 34.064986],
"PEDL":[-117.462920, 33.990140],
"MRVY":[-117.168280, 33.925270],
"PERR":[-117.249040, 33.805940],
"PIBU":[-117.850220, 34.653070],
"s211":[-118.325570, 34.780900],
"s764":[-117.375520, 33.610750]
}


for key,value in sites_dict.items():
    SITE_NAME = key
    LAT = value[1]
    LON = value[0]

    MODEL="cvmsi"
    LABEL = "cvmsi_default_%s"%(SITE_NAME)

    cmd = "plot_depth_profile.py -s %f,%f -b %f -e %f -d vs,vp,density -v %s -c %s -t %s -o /app/target/%s.png"% \
      (LAT,LON,START_depth,END_depth,STEP,MODEL,LABEL,LABEL)

    print(cmd)
    os.system(cmd)

    MODEL = "cvmsi,elygtl:ely"
    LABEL = "cvmsi_elygtl_ely_default_z_%s"%(SITE_NAME)

    cmd = "plot_depth_profile.py -s %f,%f -b %f -e %f -d vs,vp,density -v %s -c %s -t %s -o /app/target/%s.png"% \
      (LAT,LON,START_depth,END_depth,STEP,MODEL,LABEL,LABEL)

    print(cmd)
    os.system(cmd)

    MODEL = "cvmsi,elygtl:ely"
    LABEL = "cvmsi_elygtl_ely_z_700m_%s"%(SITE_NAME)

    cmd = "plot_depth_profile.py -s %f,%f -b %f -e %f -d vs,vp,density -v %s -c %s -z 0,700 -t %s -o /app/target/%s.png"% \
      (LAT,LON,START_depth,END_depth,STEP,MODEL,LABEL,LABEL)

    print(cmd)
    os.system(cmd)

sys.exit(0)
