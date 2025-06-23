# Create UCVM model Docker Image based on rockylinux which is similar to Centos-8 used at USC CARC

FROM rockylinux:8.9
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

ENV MYHOME=/home/$APP_UNAME
ENV UCVM_SRC_PATH=$MYHOME/app/src
ENV UCVM_INSTALL_PATH=$MYHOME/app/ucvm

SHELL ["/bin/bash", "-c"]

# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac

#RUN groupadd --non-unique --gid $APP_GID $APP_GRPNAME
#RUN useradd -ms /bin/bash -g $APP_GRPNAME --uid $APP_UID $APP_UNAME
RUN groupadd --gid $APP_GID $APP_GRPNAME 
RUN useradd --uid $APP_UID --gid $APP_GID --create-home $APP_UNAME 
RUN mkdir -p /etc/sudoers.d && \
    echo "$APP_UNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$APP_UNAME && \
    chmod 0440 /etc/sudoers.d/$APP_UNAME

# Set up a basic .bashrc
RUN echo 'export PATH=$PATH:/usr/local/bin' >> $MYHOME/.bashrc && \
    echo 'alias ll="ls -alF"' >> $MYHOME/.bashrc && \
    echo 'alias la="ls -A"' >> $MYHOME/.bashrc && \
    echo 'alias l="ls -CF"' >> $MYHOME/.bashrc && \
    chown $APP_UNAME:$APP_UNAME $MYHOME/.bashrc

RUN echo $APP_UNAME $APP_GRPNAME $APP_UID $APP_GID $MODELID $BDATE

RUN yum clean all && \
   yum -y update && \
   yum -y groupinstall "Development Tools" && \
   yum -y install wget yum-utils gcc-gfortran gcc-c++ fftw-devel which perl sudo

RUN yum -y install perl-ExtUtils-MakeMaker perl-Text-Template perl-Pod-Html

#ENV PERL5LIB=/usr/local/lib/perl5:/usr/lib/perl5:/usr/share/perl5:/usr/share/perl5/vendor_perl

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
RUN ln -s /usr/bin/python3 /usr/bin/python

# Added steps to manage home directory permissions
RUN mkdir -p $MYHOME/.local && \
    mkdir -p $MYHOME/result && \
    mkdir -p $MYHOME/app && \
    mkdir -p $MYHOME/dotlocal && \
    mkdir -p $MYHOME/target && \
    chown -R $APP_UNAME:$APP_GRPNAME $MYHOME && \
    chmod -R 755 $MYHOME

USER $APP_UNAME

ENV PATH="$MYHOME/app/miniconda3/bin:~/.local/bin:$MYHOME/.local/bin:$MYHOME/dotlocal/bin:${PATH}"
ARG PATH="$MYHOME/app/miniconda3/bin:~/.local/bin:$MYHOME/.local/bin:$MYHOME/dotlocal/bin:${PATH}"
 
WORKDIR $MYHOME/app

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py312_24.5.0-0-Linux-x86_64.sh -O anaconda.sh && \
    mkdir $MYHOME/.conda && \
    /bin/bash anaconda.sh -b -p $MYHOME/app/miniconda3 && \
    rm -f anaconda.sh && \
    echo "Running $(conda --version)" && \
    conda update conda && \
    conda create -n plotPython && \
    conda init bash

RUN conda install -y scipy pip numpy matplotlib basemap basemap-data-hires

# Retrieve and build UCVM
WORKDIR $MYHOME/app
RUN git clone https://github.com/sceccode/ucvm.git src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR $UCVM_SRC_PATH/largefiles
RUN ./get_largefiles.py -m $MODELID && ./stage_largefiles.py

WORKDIR $UCVM_SRC_PATH

RUN CVM_LARGEDATA_DIR=$MYHOME/target CVM_IN_DOCKER='#' ./ucvm_setup.py -a -d -p $UCVM_INSTALL_PATH >& ./ucvm_setup_install.log
RUN chmod -R +r $UCVM_INSTALL_PATH/model

# Remove the src directories to save space
#WORKDIR $MYHOME/app
#RUN rm -rf src

ENV PYTHONPATH="${MYHOME}/app/miniconda3/lib/python3.12/site-packages:${MYHOME}/.local/lib/python3.12/site-packages:${MYHOME}/dotlocal/lib/python3.12/site-packages"
ARG PYTHONPATH="${MYHOME}/app/miniconda3/lib/python3.12/site-packages:${MYHOME}/.local/lib/python3.12/site-packages:${MYHOME}/dotlocal/lib/python3.12/site-packages"

# Install plotting libraries
WORKDIR $MYHOME/app
RUN git clone https://github.com/SCECcode/ucvm_plotting.git -b withAnaconda3
WORKDIR $MYHOME/app/ucvm_plotting
#RUN ./unpack-dist
RUN pip install dist/ucvm_plotting-0.0.6.tar.gz --prefix=$MYHOME/dotlocal
## /home/ucvmuser/.local/lib/python3.12/site-packages/pycvm/


# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date=$BDATE
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v25_7"

# Define file input/output mounted disk
# /home/ucvmuser/target
VOLUME $MYHOME/target

# Setup user with test input files
#
WORKDIR /app
COPY examples /app/examples

RUN echo "source ./.bashrc" > $MYHOME/setup_ucvm && \
    echo "conda activate plotPython" >> $MYHOME/setup_ucvm && \
    echo "export PATH=\"$MYHOME/app/miniconda3/bin:~/.local/bin:$MYHOME/.local/bin:$MYHOME/dotlocal/bin:${PATH}\"" >> $MYHOME/setup_ucvm && \
    echo "source $MYHOME/app/ucvm/conf/ucvm_env.sh" >> $MYHOME/setup_ucvm && \
    echo "cd $MYHOME/target" >> $MYHOME/setup_ucvm && \
    echo "echo 'Done with setup_ucvm ..'" >> $MYHOME/setup_ucvm && \
    chmod +x $MYHOME/setup_ucvm

RUN echo "source $MYHOME/app/ucvm/conf/ucvm_env.sh" >> $MYHOME/.bashrc && \
    echo "cd $MYHOME/target" >> $MYHOME/.bashrc && \
    echo "echo 'Done with .bashrc ..'" >> $MYHOME/.bashrc


#RUN copy example $MYHOME/example

# Set working directory
WORKDIR $MYHOME
ENTRYPOINT ["/bin/bash", "--login"]

