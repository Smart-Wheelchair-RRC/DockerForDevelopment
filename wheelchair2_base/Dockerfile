FROM ghcr.io/rtarun1/humble:latest

# Add the following labels
LABEL org.opencontainers.image.description="Wheelchair2"
LABEL org.opencontainers.image.title="Wheelchair2DevCon"
LABEL org.opencontainers.image.vendor="Tarun R"
LABEL org.opencontainers.image.source="https://github.com/rtarun1/DockerForROS2Development"
LABEL maintainer="tarun.ramak@gmail.com"
LABEL org.opencontainers.image.licenses="MIT"
# handle default shell
SHELL ["/bin/bash", "-c"]

COPY rosPkgs.list /tmp/rosPkgs.list
RUN sudo apt-get update \
    && sudo apt-get -y install --no-install-recommends $(cat /tmp/rosPkgs.list) \
    && sudo apt-get autoremove -y \
    && sudo apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update \
    && sudo apt-get -y install --no-install-recommends \
    libssl-dev \
    libusb-1.0-0-dev \
    libudev-dev \
    pkg-config \
    libgtk-3-dev \
    wget \
    cmake \
    build-essential \
    libglfw3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    at \
    v4l-utils \
    && sudo rm -rf /var/lib/apt/lists/*


WORKDIR /home/rtarun1/wheelchair2

# Build and install Livox-SDK2
RUN git clone https://github.com/rtarun1/Livox-SDK2.git 
RUN cd Livox-SDK2 \
    && mkdir build \
    && cd build \
    && cmake .. && make -j \
    && sudo make installLivox

WORKDIR /home/rtarun1

RUN git clone --branch v2.56.2 https://github.com/IntelRealSense/librealsense.git

WORKDIR /home/rtarun1/librealsense

RUN sudo mkdir -p /etc/udev/rules.d && \
    ./scripts/setup_udev_rules.sh \
    ./scripts/patch-realsense-ubuntu-lts-hwe.sh 

RUN mkdir build && cd build \
    && cmake ../ \
    && sudo make uninstall && make clean && make && sudo make install 
