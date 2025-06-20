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

# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
# and for building the model and adding the correct date into the label
RUN echo $APP_UNAME $APP_GRPNAME $APP_UID $APP_GID $MODELID $BDATE

# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac
RUN groupadd -f --non-unique --gid $APP_GID $APP_GRPNAME 
RUN useradd -ms /bin/bash -g $APP_GRPNAME --uid $APP_UID $APP_UNAME

# Added explicit HOME environment variable
# /home/ucvmuser
ENV MYHOME=/home/$APP_UNAME
SHELL ["/bin/bash", "-c"]

WORKDIR $MYHOME
RUN yum clean all && \
    yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum -y install curl wget yum-utils gcc-gfortran gcc-c++ fftw-devel which python38 python38-devel

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
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

##wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O anaconda.sh && \

WORKDIR $MYHOME/app
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py312_24.5.0-0-Linux-x86_64.sh -O anaconda.sh && \
    mkdir $MYHOME/.conda && \
    /bin/bash anaconda.sh -b -p $MYHOME/app/miniconda3 && \
    rm -f anaconda.sh && \
    echo "Running $(conda --version)" && \
    conda update conda && \
    conda create -n plotPython && \
    conda init bash

RUN conda install -y matplotlib basemap basemap-data-hires jupyterlab 

#### building user app part 

# Retrieve and build UCVM
WORKDIR $MYHOME/app
RUN git clone https://github.com/sceccode/ucvm.git src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR $MYHOME/app/src/largefiles
RUN ./get_largefiles.py -m $MODELID && ./stage_largefiles.py

WORKDIR $MYHOME/app/src
RUN ./ucvm_setup.py -a -d -p $MYHOME/app/ucvm >& ./ucvm_setup_install.log
RUN chmod -R +r $MYHOME/app/ucvm/model

# Remove the src directories to save space
WORKDIR $MYHOME/app
RUN rm -rf src 

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
LABEL version="ucvm_v22_7"

#    echo "cd $MYHOME/app/ucvm_plotting; pip install dist/ucvm_plotting-0.0.6.tar.gz --prefix=$MYHOME/dotlocal" >> $MYHOME/setup_ucvm && \

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

# Expose the port JupyterLab will run on
#EXPOSE 8888

# Define file input/output mounted disk
VOLUME $MYHOME/target

WORKDIR $MYHOME

ENV JUPYTER_TERMINAL_DEFAULT_SHELL="/bin/bash"
ENV HOME=$MYHOME

# Define the command to run JupyterLab
# CMD  ["/bin/bash","--login"]
ENTRYPOINT ["/home/ucvmuser/app/miniconda3/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
