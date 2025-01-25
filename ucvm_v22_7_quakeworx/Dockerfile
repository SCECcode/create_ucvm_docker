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
ENV HOME=/home/$APP_UNAME

WORKDIR /home/$APP_UNAME
RUN yum clean all && \
    yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum -y install curl wget yum-utils gcc-gfortran gcc-c++ fftw-devel which python38 python38-devel

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
RUN ln -s /usr/bin/python3 /usr/bin/python

# Added steps to manage home directory permissions
RUN mkdir -p $HOME/.local && \
    mkdir -p $HOME/result && \
    chown -R $APP_UID:$APP_GID $HOME && \
    chmod -R 755 $HOME

USER $APP_UNAME

ENV PATH="$HOME/miniconda3/bin:$HOME/.local/bin:${PATH}"
ARG PATH="$HOME/miniconda3/bin:$HOME/.local/bin:${PATH}"

WORKDIR /home/$APP_UNAME
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O anaconda.sh && \
    mkdir $HOME/.conda && \
    /bin/bash anaconda.sh -b && \
    rm -f anaconda.sh && \
    echo "Running $(conda --version)" && \
    conda update conda && \
    conda create -n plotPython && \
    conda init bash

RUN echo "conda activate plotPython" >> $HOME/.bashrc && \
    /bin/bash $HOME/.bashrc && \
    conda install -y matplotlib basemap basemap-data-hires 

RUN conda install -y jupyterlab


#### building user app part 

# Retrieve and build UCVM
WORKDIR $HOME/app
RUN git clone https://github.com/sceccode/ucvm.git src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR $HOME/app/src/largefiles
RUN ./get_largefiles.py -m $MODELID && ./stage_largefiles.py

WORKDIR $HOME/app/src
RUN ./ucvm_setup.py -a -d -p $HOME/app/ucvm >& ./ucvm_setup_install.log

# Remove the src directories to save space
WORKDIR $HOME/app
RUN rm -rf src 

ENV PYTHONPATH="${HOME}/miniconda3/lib/python3.12/site-packages:${HOME}/.local/lib/python3.12/site-packages/pycvm:${PYTHONPATH}"
ARG PYTHONPATH="${HOME}/miniconda3/lib/python3.12/site-packages:${HOME}/.local/lib/python3.12/site-packages/pycvm:${PYTHONPATH}"

#import site
#print(site.getsitepackages())
#also "/usr/local/opt/conda/envs/plotPython/lib/python3.12/site-packages:${PYTHON_PATH}"
#./miniconda3/lib/python3.12/site-packages
#/.local/lib/python3.12/site-packages

# Install plotting libraries
WORKDIR $HOME/app
RUN git clone https://github.com/SCECcode/ucvm_plotting.git -b withAnaconda3
WORKDIR $HOME/app/ucvm_plotting
RUN ./unpack-dist
## not able to unpack into system spot and so ended up at
## /home/ucvmuser/.local/lib/python3.12/site-packages/pycvm/

# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date=$BDATE
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v22_7"

RUN echo "conda activate plotPython" >> $HOME/.bashrc && \
    echo "export PATH=\"$HOME/miniconda3/bin:$HOME/.local/bin:$PATH\"" >> $HOME/.bashrc && \
    echo "cd $HOME/app/ucvm_plotting; ./unpack-dist" >> $HOME/.bashrc && \
    echo "conda activate plotPython" >> /home/$APP_UNAME/.bashrc && \
    echo ". $HOME/app/ucvm/conf/ucvm_env.sh" >> $HOME/.bashrc && \
    echo "cd $HOME" >> $HOME/.bashrc && \
    echo "echo 'Done with .bashrc ..'" >> $HOME/.bashrc

RUN echo "echo 'calling setup ..'" > $HOME/setup && \
    echo "source $HOME/app/ucvm/conf/ucvm_env.sh" >> $HOME/setup && \
    echo "cd $HOME/app/ucvm_plotting; ./unpack-dist" >> $HOME/setup && \
    echo "cd $HOME" >> $HOME/setup

# Expose the port JupyterLab will run on
EXPOSE 8888

# Define file input/output mounted disk
VOLUME $HOME/app/target

WORKDIR $HOME

# Define the command to run JupyterLab
#CMD  ["/bin/bash","--login"]
ENTRYPOINT ["/home/ucvmuser/miniconda3/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

