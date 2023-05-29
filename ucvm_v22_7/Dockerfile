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
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
RUN ln -s /usr/bin/python3 /usr/bin/python

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

RUN /usr/local/opt/conda/bin/conda create -n Python2 python=2.7.15 scipy pip numpy matplotlib basemap basemap-data-hires

# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac
RUN groupadd --non-unique --gid $APP_GID $APP_GRPNAME && \
    useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME

RUN chmod -R og+rw /app

# Retrieve and build UCVM
WORKDIR /app
RUN git clone https://github.com/sceccode/ucvm.git src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR /app/src/largefiles
RUN ./get_largefiles.py -m $MODELID && ./stage_largefiles.py

WORKDIR /app/src
RUN ./ucvm_setup.py -a -d -p /app/ucvm >& ./ucvm_setup_install.log

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
LABEL version="ucvm_v22_7"

USER $APP_UNAME
RUN echo "source /usr/local/opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "source /app/ucvm/conf/ucvm_env.sh" >> ~/.bashrc && \
    echo "conda activate Python2" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]
WORKDIR /app/target
ENTRYPOINT ["/bin/bash"]

