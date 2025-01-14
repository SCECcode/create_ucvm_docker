# Create UCVM model Docker Image based on rockylinux which is similar to Centos-8 used at USC CARC

FROM rockylinux:8.5
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Define Build and runtime arguments
ARG APP_UNAME
ARG APP_GRPNAME
ARG APP_UID
ARG APP_GID
ARG MODELID
ARG BDATE

ENV APP_UNAME=$APP_UNAME \
APP_GRPNAME=$APP_GRPNAME \
APP_UID=$APP_UID \
APP_GID=$APP_GID \
MODELID=$MODELID \
BDATE=$BDATE

# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
# and for building the model and adding the correct date into the label
RUN echo $APP_UNAME $APP_GRPNAME $APP_UID $APP_GID $MODELID $BDATE

RUN yum clean all && yum -y update && yum -y\
 groupinstall "Development Tools" && yum -y\
 install wget yum-utils gcc-gfortran gcc-c++ fftw-devel which python38

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
WORKDIR /app
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh -O anaconda.sh && \
    /bin/bash anaconda.sh -b -p /usr/local/opt/conda && \
    rm anaconda.sh && \
    source /usr/local/opt/conda/bin/activate && \
    conda init

RUN conda config --add channels conda-forge && \
    conda install scipy pip numpy matplotlib basemap basemap-data-hires && \
    conda install conda-forge::gmt setuptools anaconda::pybind11 conda-forge::h5py

# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac
RUN groupadd --non-unique --gid $APP_GID $APP_GRPNAME && \
    useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME

RUN chmod -R og+rw /app

# Retrieve and build UCVM
WORKDIR /app
RUN git clone https://github.com/sceccode/ucvm.git -b withSFCVM src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR /app/src/largefiles
RUN ./get_largefiles.py -m $MODELID && ./stage_largefiles.py

WORKDIR /app/src
RUN CVM_LARGEDATA_DIR="/Users/mei/scec/CVM_DATASET_DIRECTORY" ./ucvm_setup.py -a -d -p /app/ucvm >& ./ucvm_setup_install.log

# Remove the src directories to save space
#WORKDIR /app
#RUN rm -rf src

# Install plotting libraries
WORKDIR /app/ucvm
git clone https://github.com/SCECcode/ucvm_metadata_utilities metadata_utilities
cd metadata_utilities
source ./setup.sh
WORKDIR /app/ucvm
RUN git clone https://github.com/SCECcode/ucvm_plotting.git -b withAnaconda3
cd /app/ucvm/ucvm_plotting
RUN ./unpack-dist
conda install dist/ucvm_plotting-0.0.6.tar.gz


# Define file input/output mounted disk
#
VOLUME /app/target

# Setup user with test input files
#
WORKDIR /app
COPY examples /app/examples

RUN chmod -R og+rw /app/ucvm /app/examples && \
    chmod -R +x /app/examples/*.py /app/examples/*.sh && \
    chmod -R og+rw /app/target

# Define directory that will be mounted and used for file input/output
#

# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date=$BDATE
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v25_2"

USER $APP_UNAME
RUN echo "source /usr/local/opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "source /app/ucvm/conf/ucvm_env.sh" >> ~/.bashrc && \
    echo "export CVM_LARGEDATA_DIR=/Users/mei/scec/CVM_DATASET_DIRECTORY" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]
WORKDIR /app/target
ENTRYPOINT ["/bin/bash"]

