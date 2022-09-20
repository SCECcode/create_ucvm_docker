[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
![GitHub repo size](https://img.shields.io/github/repo-size/sceccode/ucvm_docker)

## The Unified Community Velocity Model (UCVM) Docker Images Create Utilities 

## Description: 
The SCEC Unified Community Velocity Model (UCVM) software framework is a collection of software tools that provide a standard query interface to seismic velocity models. Once a seismic velocity model is registered into UCVM, it can be queried and combined with other velocity models through the UCVM software interface.

UCVM was developed as an interdisciplinary research collaboration involving geoscientists and computer scientists. UCVM geoscience research includes identification and assembly of existing California velocity models into a state-wide model and improvements to existing velocity models. UCVM computer science research includes definition of a easy-to-use CVM query interface, integration of regional 3D and geotechnical models, and automated CVM evaluation processing capabilities.

UCVM is open-source scientific software designed to support earth scientists, civil engineers, and other groups interested in detailed information about earth properties. UCVM is primarily used by scientists to work with earth material properties on regional scales. One important use of UCVM is to create simulation meshes used in high resolution 3D wave propagation simulations.

UCVM public accessible docker images(https://github.com/SCECcode/ucvm_docker/wiki) are for users to access UCVM who does not or might not be able to install full UCVM on their computers.

This github repository contains the Dockerfile and related files for creating the UCVM Docker images with the UCVM v22.7 and the UCVM plotting utilities from https://github.com/SCECcode/ucvm_plotting. 

## Table of Contents:
1. [Usage](#usage)
2. [Contributing](#contributing)
3. [Credits](#credit)
4. [License](#license)

## Usage
Before building a UCVM Docker image, make sure you can access dockerhub's sceccode image repository space. You should login to your Docker account that has permission to push to the sceccode organization registry. If you want to build UCVM Docker images for 
local testing and not pushing the created image to sceccode space on the dockerhub, you could mark off the 'docker push' commands in the build python scripts.

To build a Docker image, there is a build_one.py  python script under ucvm_v22_7 directory.
<pre>
$ ./build_one.py
</pre>

To build a full set of Docker images, 
<pre>
$ ./build_all.py
</pre>

To test Docker images please refer to ucvm_docker's wiki(https://github.com/SCECcode/ucvm_docker/wiki)

## Support
Support for UCVM docker images create utilities are provided by that Southern California Earthquake Center (SCEC) Research Computing Group. This group supports several research software distributions including UCVM. Users can report issues and feature requests using UCVM's github-based issue tracking link below. Developers will also respond to emails sent to the SCEC software contact listed below.
1. [UCVM Docker Github Issue Tracker:](https://github.com/SCECcode/create_ucvm_docker/issues)
2. Email Contact: software@scec.usc.edu

## Contributing
We welcome contributions to the UCVM software framework. An overview of the process for contributing seismic models or software updates to the UCVM Project is provided in the [UCVM contribution](CONTRIBUTING.md) guidelines. UCVM contributors agree to abide by the code of conduct found in our [Code of Conduct](CODE_OF_CONDUCT.md) guidelines.

## Credits
Development of UCVM is a group effort. Developers that have contributed to the UCVM docker software are listed in the [CREDITS.md](CREDITS.md) file in this repository.

## License
The UCVM software is distributed under the BSD 3-Clause open-source license. Please see the [LICENSE.txt](LICENSE.txt) file for more information.
