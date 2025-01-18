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

# Added steps to manage home directory permissions
RUN mkdir -p $HOME/.local \
    && chown -R $APP_UID:$APP_GID $HOME \
    && chmod -R 755 $HOME

WORKDIR /home/$APP_UNAME

RUN yum clean all && \
    yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum -y install curl wget yum-utils gcc-gfortran gcc-c++ fftw-devel which python38 python38-devel

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
RUN ln -s /usr/bin/python3 /usr/bin/python

# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
WORKDIR /home/$APP_UNAME/app
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O anaconda.sh && \
    mkdir /home/$APP_UNAME/.conda && \
    /bin/bash anaconda.sh -b -p /usr/local/opt/conda && \
    rm -f anaconda.sh && \
    echo "Running $(conda --version)" && \
    /usr/local/opt/conda/bin/conda update conda && \
    /usr/local/opt/conda/bin/conda init bash

#RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh -O anaconda.sh && \
#    /bin/bash anaconda.sh -b -p /usr/local/opt/conda && \
#    rm anaconda.sh && \
#    ln -s /usr/local/opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
#    find /usr/local/opt/conda/ -follow -type f -name '*.a' -delete && \
#    find /usr/local/opt/conda/ -follow -type f -name '*.js.map' -delete && \
#    /usr/local/opt/conda/bin/conda clean -afy && \
#    /usr/local/opt/conda/bin/conda init bash

RUN echo "source /usr/local/opt/conda/etc/profile.d/conda.sh" >> /home/$APP_UNAME/.bashrc && \
    bash /home/$APP_UNAME/.bashrc && \
    /usr/local/opt/conda/bin/conda install -y pip bzip2

#RUN /usr/local/opt/conda/bin/conda create -n Python2 -y python=2.7.15 scipy numpy matplotlib basemap basemap-data-hires 
RUN /usr/local/opt/conda/bin/conda create -n plotPython -y numpy matplotlib basemap basemap-data-hires 

RUN /usr/local/opt/conda/bin/conda install -y jupyterlab


#### building user app part 

# Retrieve and build UCVM
WORKDIR /home/$APP_UNAME/app
RUN git clone https://github.com/sceccode/ucvm.git src

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR /home/$APP_UNAME/app/src/largefiles
RUN ./get_largefiles.py -m $MODELID && ./stage_largefiles.py

WORKDIR /home/$APP_UNAME/app/src
RUN ./ucvm_setup.py -a -d -p /home/$APP_UNAME/app/ucvm >& ./ucvm_setup_install.log

# Remove the src directories to save space
WORKDIR /home/$APP_UNAME/app
RUN rm -rf src

# Install plotting libraries
WORKDIR /home/$APP_UNAME/app/ucvm
RUN git clone https://github.com/SCECcode/ucvm_plotting.git
WORKDIR /home/$APP_UNAME/app/ucvm/ucvm_plotting
##RUN ./unpack-dist

# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date=$BDATE
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v22_7"

RUN echo "source /home/$APP_UNAME/app/ucvm/conf/ucvm_env.sh" >> /home/$APP_UNAME/.bashrc && \
    echo "export PATH=\"/usr/local/opt/conda/bin:$PATH\"" >> /home/$APP_UNAME/.bashrc && \
    echo "conda activate plotPython" >> /home/$APP_UNAME/.bashrc

# Added steps to manage home directory permissions
RUN mkdir -p $HOME/.local \
    && chown -R $APP_UID:$APP_GID $HOME \
    && chmod -R 755 $HOME

USER $APP_UNAME

ENV PATH="/usr/local/opt/conda/bin:${PATH}"
ARG PATH="/usr/local/opt/conda/bin:${PATH}"

WORKDIR /home/$APP_UNAME

# Expose the port JupyterLab will run on
EXPOSE 8888

# Define file input/output mounted disk
#VOLUME /home/$APP_UNAME/app/target

SHELL ["/bin/bash", "--login", "-c"]

#ENTRYPOINT ["/bin/bash"]
# Define the command to run JupyterLab
ENTRYPOINT ["/usr/local/opt/conda/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]

