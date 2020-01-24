FROM ubuntu:18.04

# Install dependencies - there are various system libraries
# that are required to run GUI apps but aren't installed by default
RUN apt-get update -y
RUN apt install -y python3-pip libgl1-mesa-dev libgssapi-krb5-2 libfontconfig-dev libxkbcommon-x11-dev git libopenblas-dev

# Install quantiphyse first which ensures we get Cython+Numpy which
# are required at build time for some of the plugins
RUN pip3 install git+https://github.com/ibme-qubic/quantiphyse@multiview

# Install plugins and their dependencies
RUN pip3 install git+https://github.com/ibme-qubic/quantiphyse-asl \
                 git+https://github.com/ibme-qubic/quantiphyse-cest \
                 git+https://github.com/ibme-qubic/quantiphyse-dce \
                 git+https://github.com/ibme-qubic/quantiphyse-dsc \
                 git+https://github.com/ibme-qubic/quantiphyse-fabber \
                 git+https://github.com/ibme-qubic/quantiphyse-fsl \
                 git+https://github.com/ibme-qubic/quantiphyse-perfsim \
                 git+https://github.com/ibme-qubic/quantiphyse-qbold \
                 git+https://github.com/ibme-qubic/quantiphyse-sv \
                 git+https://github.com/ibme-qubic/quantiphyse-t1 \
                 git+https://github.com/ibme-qubic/maskSLIC \
                 git+https://github.com/ibme-qubic/pyfab \
                 git+https://github.com/ibme-qubic/oxasl \
                 git+https://github.com/ibme-qubic/oxasl_ve \
                 git+https://github.com/ibme-qubic/oxasl_mp \
                 git+https://github.com/ibme-qubic/oxasl_multite \
                 nibabel==2

# We build Fabber and just copy the executables to the container. Note that
# we could build fabber on the container but would need FSL+build tools.
# However we have to make sure the build machine is binary compatible with
# the container.
COPY fabber /fabber
ENV FABBERDIR /fabber

# Copy scripts for running Quantiphyse
COPY container_scripts/set_registered.py /set_registered.py
COPY container_scripts/run_quantiphyse.sh /run_quantiphyse.sh
CMD /run_quantiphyse.sh
