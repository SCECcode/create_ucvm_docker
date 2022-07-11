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
APP_MODELID=$MODELID \
APP_BDATE=$BDATE

# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
# and for building the model and adding the correct date into the label
RUN echo $APP_UNAME
RUN echo $APP_GRPNAME
RUN echo $APP_UID
RUN echo $APP_GID
RUN echo $MODELID
RUN echo $BDATE

#
# Setup path for installation of ucvm into /app/bin
#
#
RUN yum clean all && yum -y update && yum -y\
 groupinstall "Development Tools" && yum -y\
 install yum-utils gcc-gfortran gcc-c++ fftw-devel which python38

#
# Create python link as root before setting user. This is needed by
# the ucvm_setup.py script which will run to the ucvm installation
# To support the python2 plotting library, we will install Anaconda with a python2
# virtual environment in this image
RUN ln -s /usr/bin/python3 /usr/bin/python

#
# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac
RUN groupadd --non-unique --gid $APP_GID $APP_GRPNAME
RUN useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME
USER $APP_UNAME

WORKDIR /home/$APP_UNAME
COPY --chown=$APP_UNAME:$APP_GRPNAME Anaconda3-2022.05-Linux-x86_64.sh ./Anaconda3-2022.05-Linux-x86_64.sh
COPY --chown=$APP_UNAME:$APP_GRPNAME anaconda_inputs.txt ./anaconda_inputs.txt
RUN bash Anaconda3-2022.05-Linux-x86_64.sh < anaconda_inputs.txt
RUN rm /home/$APP_UNAME/Anaconda3-2022.05-Linux-x86_64.sh
RUN /home/$APP_UNAME/anaconda3/condabin/conda create -n Python2 python=2.7.15 scipy pip numpy matplotlib basemap basemap-data-hires

WORKDIR /app
RUN git clone https://github.com/sceccode/ucvm.git
RUN mv /app/ucvm /app/src
WORKDIR /app

# An external script has selected the correct model files for this image in the largefiles dir
# by setting the model abbreviations in the largefile_inputs.txt file
WORKDIR /app/src/largefiles

RUN ./get_largefiles.py -m $MODELID
RUN ./stage_largefiles.py

# The setup_input.txt contains the path where the ucvm binaries will be installed
#
WORKDIR /app/src
COPY --chown=$APP_UNAME:$APP_GRPNAME setup_inputs.txt ./setup_inputs.txt
RUN ./ucvm_setup.py -a -d < setup_inputs.txt
#
# Remove the src directories to save space
#
WORKDIR /app
RUN rm -rf src
#
# Install plotting libraries
#
RUN echo "conda activate Python2" >> ~/.bashrc
RUN echo "source /app/ucvm/conf/ucvm_env.sh" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

WORKDIR /app/ucvm
RUN git clone https://github.com/SCECcode/ucvm_plotting.git
WORKDIR /app/ucvm/ucvm_plotting
RUN ./unpack-dist
#
# Define file input/output mounted disk
#
VOLUME /app/target
#
# Setup user with test input files
#
WORKDIR /app
COPY --chown=$APP_UNAME:$APP_GRPNAME test_latlons.txt ./test_latlons.txt
COPY --chown=$APP_UNAME:$APP_GRPNAME basic_query.txt ./basic_query.txt
COPY --chown=$APP_UNAME:$APP_GRPNAME make_mesh.py ./make_mesh.py
#
# Define directory that will be mounted and used for file input/output
#
WORKDIR /app/target
#
# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date=$BDATE
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v22_7"
#
# start as command line terminal
#
ENTRYPOINT ["/bin/bash"]
