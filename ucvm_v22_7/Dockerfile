
# Create UCVM model Docker Image based on rockylinux which is similar to Centos-8 used at USC CARC
#
# ON mac M1 chipset,
# this leads to: qemu-x86_64: Could not open '/lib64/ld-linux-x86-64.so.2': No such file or directory
# according to this: https://stackoverflow.com/questions/71040681/qemu-x86-64-could-not-open-lib64-ld-linux-x86-64-so-2-no-such-file-or-direc
# docker build --platform linux/amd64 --no-cache=false ...
#=> => writing image sha256:3166c6f927375ce31ca27e5deb34d1f721b7143bbbc33da038807ff9791c9bf  0.0s
#=> => naming to docker.io/library/ucvm_227_ivlsu:0810                                       0.0s
## running
#WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
#(Python2) [ucvmuser@b5e2c720b80b target]$ 
## running with addition: -e DISPLAY=$DISPLAY 
## and view_png.py
## tkinter.TclError: couldn't connect to display "/private/tmp/com.apple.launchd.dcqaQplifw/org.xquartz:0"
## also adding : -v /tmp/.X11-unix:/tmp/.X11-unix
## same error
## ===
## another solution: https://stackoverflow.com/questions/70722222/how-to-run-tkinter-inside-a-docker-container-on-macbook-pro
##
## run with 
#docker run --platform linux/amd64 --rm -it -e DISPLAY=$"${IP}:0"  --mount type=bind,source="$(pwd)"/target,destination=/app/target sceccode/ucvm_227_cvms5:0710
# disable the warning
#

FROM rockylinux:8.5
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Define Build and runtime arguments
#ARG APP_UNAME
#ARG APP_GRPNAME
#ARG APP_UID
#ARG APP_GID
#ARG MODELID
#ARG BDATE

ENV APP_UNAME=ucvmuser \
APP_GRPNAME=staff \
APP_UID=503 \
APP_GID=1000 \
MODELID=ivlsu \
BDATE=0810

# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
# and for building the model and adding the correct date into the label
RUN echo $APP_UNAME
RUN echo $APP_GRPNAME
RUN echo $APP_UID
RUN echo $APP_GID
RUN echo $MODELID
RUN echo $BDATE

RUN yum clean all && yum -y update && yum -y\
 groupinstall "Development Tools" && yum -y\
 install wget yum-utils gcc-gfortran gcc-c++ fftw-devel which python38

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
RUN ln -s /usr/bin/python3 /usr/bin/python

# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac
RUN groupadd --non-unique --gid $APP_GID $APP_GRPNAME
RUN useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
WORKDIR /app
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh -O anaconda.sh && \
    /bin/bash anaconda.sh -b -p /usr/local/opt/conda && \
    rm anaconda.sh && \
    ln -s /usr/local/opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    find /usr/local/opt/conda/ -follow -type f -name '*.a' -delete && \
    find /usr/local/opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /usr/local/opt/conda/bin/conda clean -afy

RUN echo "source /usr/local/opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN /usr/local/opt/conda/bin/conda create -n Python2 python=2.7.15 scipy pip numpy matplotlib basemap basemap-data-hires

# Retrieve and build UCVM
WORKDIR /app
RUN git clone https://github.com/sceccode/ucvm.git src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR /app/src/largefiles

RUN ./get_largefiles.py -m $MODELID
RUN ./stage_largefiles.py

WORKDIR /app/src
RUN ./ucvm_setup.py -a -d -p /app/ucvm >& ~/ucvm_setup_install.log && \
    echo "source  /app/ucvm/conf/ucvm_env.sh" >> ~/.bashrc

# Remove the src directories to save space
WORKDIR /app
RUN rm -rf src

# Install plotting libraries
WORKDIR /app/ucvm
RUN echo "conda activate Python2" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN git clone https://github.com/SCECcode/ucvm_plotting.git
WORKDIR /app/ucvm/ucvm_plotting
RUN ./unpack-dist

# Define file input/output mounted disk
#
VOLUME /app/target

# Setup user with test input files
#
WORKDIR /app
COPY --chown=$APP_UNAME:$APP_GRPNAME test_latlons.txt ./test_latlons.txt
COPY --chown=$APP_UNAME:$APP_GRPNAME basic_query.txt ./basic_query.txt
COPY --chown=$APP_UNAME:$APP_GRPNAME make_mesh.py ./make_mesh.py

RUN mkdir inputs && \
    mv test_latlons.txt inputs && \
    mv basic_query.txt inputs && \
    mv make_mesh.py inputs

RUN chmod -R og+rw /app/ucvm/tests


# Define directory that will be mounted and used for file input/output
#

# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date=$BDATE
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v22_7"

WORKDIR /app/target

USER $APP_UNAME

RUN echo "source /usr/local/opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "source  /app/ucvm/conf/ucvm_env.sh" >> ~/.bashrc
RUN echo "conda activate Python2" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]

WORKDIR /app/target


ENTRYPOINT ["/bin/bash"]

