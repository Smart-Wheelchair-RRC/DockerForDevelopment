FROM ghcr.io/smart-wheelchair-rrc/noetic:latest

# Add the following labels
LABEL org.opencontainers.image.description="Docker Development Container"
LABEL org.opencontainers.image.title="ROS1Dev"
LABEL org.opencontainers.image.vendor="Tarun R"
LABEL org.opencontainers.image.source="https://github.com/Smart-Wheelchair-RRC/DockerForDevelopment"
LABEL maintainer="tarun.ramak@gmail.com"
LABEL org.opencontainers.image.licenses="MIT"
# handle default shell
SHELL ["/bin/bash", "-c"]

# Install Basic deps
RUN sudo apt-get update \
    && sudo apt-get -y install --no-install-recommends\
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
    xterm \
    git \
    vim \
    htop \
    python3 \
    python3-pip \
    && sudo apt-get autoremove -y \
    && sudo apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

#python deps

RUN sudo apt-get update \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir open3d