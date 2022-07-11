# Create UCVM model Docker Image based on Centos-8 also available at USC CARC
FROM centos:8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Define Build and runtime arguments
ARG APP_UNAME
ARG APP_GRPNAME
ARG APP_UID
ARG APP_GID
ENV APP_UNAME=$APP_UNAME \
APP_GRPNAME=$APP_GRPNAME \
APP_UID=$APP_UID \
APP_GID=$APP_GID
# Retrieve the userid and groupid from the args so 
# Define these parameters to support building and deploying on EC2 so user is not root
RUN echo $APP_UNAME
RUN echo $APP_GRPNAME
RUN echo $APP_UID
RUN echo $APP_GID

LABEL "maintainer"="Philip Maechling <maechlin@usc.edu>" "appname"="ucvm"
#
# Setup path for installation of ucvm into /app/bin
#
ENV UCVM_SRC_PATH=/app/src UCVM_INSTALL_PATH=/app/ucvm LD_LIBRARY_PATH=/app/ucvm/lib/euclid3/lib:/app/ucvm/lib/proj-5/lib:/app/ucvm/model/cvms/lib:/app/ucvm/model/cvms5/lib:/app/ucvm/model/cvmh1511/lib:/app/ucvm/model/cvmsi/lib:/app/ucvm/model/wfcvm/lib
ENV PYTHONPATH=/app/ucvm/utilities/pycvm
ENV PATH="/app/ucvm/bin:/usr/bin/python2:/usr/bin/python3:${PATH}"
#
RUN yum clean all && yum -y update && yum -y\
 groupinstall "Development Tools" && yum -y\
 install yum-utils gcc-gfortran gcc-c++ fftw-devel which python3

#
# Link python3
RUN ln -s /usr/bin/python3 /usr/bin/python
# Setup Owners
# Documents say this groupadd is needed when you build on linux, but not on Mac
RUN groupadd --non-unique --gid $APP_GID $APP_GRPNAME
RUN useradd -ms /bin/bash -G $APP_GRPNAME --uid $APP_UID $APP_UNAME
USER $APP_UNAME

WORKDIR /app
COPY --chown=$APP_UNAME:$APP_GRPNAME ucvm/ ./src
COPY --chown=$APP_UNAME:$APP_GRPNAME get_largefile_inputs.txt ./src/largefiles/.
# An external script has posted the correct .gz model file in the largefiles dir
# Install largefiles
WORKDIR /app/src/largefiles
RUN ./get_largefiles.py < ./get_largefile_inputs.txt
RUN ./stage_largefiles.py
WORKDIR /app/src
COPY --chown=$APP_UNAME:$APP_GRPNAME setup_inputs.txt ./setup_inputs.txt
RUN ./ucvm_setup.py -a -d < setup_inputs.txt
#
# Remove the src directories to save space
#
WORKDIR /app
RUN rm -rf src
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
COPY --chown=$APP_UNAME:$APP_GRPNAME test_latlons.txt ./test_latlons.txt
COPY --chown=$APP_UNAME:$APP_GRPNAME basic_query.txt ./basic_query.txt
#
#
# Add metadata to dockerfile using labels
LABEL org.label-schema.build-date="20211124"
LABEL org.label-schema.license="BSD 3-Clause"
LABEL org.scec.project="SCEC Unified Community Velocity Model"
LABEL org.scec.responsible_person="Philip Maechling"
LABEL org.scec.primary_contact="maechlin@usc.edu"
LABEL version="ucvm_v21_10_1124"
#
# start as command line terminal
#
ENTRYPOINT ["/bin/bash"]
