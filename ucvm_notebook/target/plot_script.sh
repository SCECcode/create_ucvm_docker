#!/bin/bash
# Script for running depth profile plots
#
# Configuration Changes:
# Set the UCVM installation, and the model config file directories
#
# The script can be re-run for different sites by
# changing the site number for each selected site
#
#
UCVM_CONF_PATH=/app/ucvm/conf

# String to change
# gtl = off
# gtl = on
#
#
# Define resolution of profile
#
STEP=1
START_depth=0
END_depth=1000
# Start with Site at USC in LA Basin
# This is the latlong for USC
#
# SITE_NUM=1
# LAT=34.0224
# LON=-118.2851
#
# Re-run script with site ne
SITE_NUM=2
LAT=35.5
LON=-117.5

## Test Cases 4
# Test cvm-si (CVM-S4.26.M01 with native gtl
# Test cvm-s4- with elygtl:ely
#

MODEL=cvmsi
LABEL=cvmsi_default_${SITE_NUM}

plot_depth_profile.py -s ${LAT},${LON} -b ${START_depth} -e ${END_depth} -d vs,vp,density -v ${STEP} -c ${MODEL} -t ${LABEL} -o /app/target/${LABEL}.png


MODEL=cvmsi,elygtl:ely
LABEL=cvmsi_elygtl_ely_default_z_${SITE_NUM}

plot_depth_profile.py -s ${LAT},${LON} -b ${START_depth} -e ${END_depth} -d vs,vp,density -v ${STEP} -c ${MODEL} -t ${LABEL} -o /app/target/${LABEL}.png

MODEL=cvmsi,elygtl:ely
LABEL=cvmsi_elygtl_ely_z_700m_${SITE_NUM}

plot_depth_profile.py -s ${LAT},${LON} -b ${START_depth} -e ${END_depth} -d vs,vp,density -v ${STEP} -c ${MODEL} -z 0,700 -t ${LABEL} -o /app/target/${LABEL}.png
