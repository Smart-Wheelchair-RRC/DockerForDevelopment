FROM ghcr.io/smart-wheelchair-rrc/humble_jetson:v4.0

ARG USERNAME=container_user

# Add the following labels
LABEL org.opencontainers.image.description="Wheelchair2"
LABEL org.opencontainers.image.title="Wheelchair2DevCon"
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
    python3-venv \
    python3-pip \
    && sudo apt-get autoremove -y \
    && sudo apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

# Build and install Realsense-SDK
WORKDIR /home/$USERNAME
RUN git clone --depth=1 --progress --verbose --branch v2.56.2 https://github.com/IntelRealSense/librealsense.git
WORKDIR /home/$USERNAME/librealsense
RUN sudo mkdir -p /etc/udev/rules.d && \
    ./scripts/setup_udev_rules.sh \
    ./scripts/patch-realsense-ubuntu-lts-hwe.sh 
RUN mkdir build && cd build \
    && cmake ../ \
    && sudo make uninstall && make clean && make && sudo make install

# Build and install Livox-SDK2
WORKDIR /home/$USERNAME
RUN git clone --depth=1 --progress --verbose https://github.com/rtarun1/Livox-SDK2.git 
RUN cd Livox-SDK2 \
    && mkdir build \
    && cd build \
    && cmake .. && make -j \
    && sudo make install

COPY rosPkgs.list /tmp/rosPkgs.list
RUN sudo apt-get update \
    && sudo apt-get -y install --no-install-recommends $(cat /tmp/rosPkgs.list) \
    && sudo rm -rf /var/lib/apt/lists/*

# Deal with python dependencies
RUN mkdir /home/$USERNAME/python3_venvs

## casadi
COPY casadi-requirements.txt /tmp/casadi-requirements.txt
RUN python3 -m venv /home/$USERNAME/python3_venvs/casadi_venv --system-site-packages --upgrade-deps --symlinks \
    && /home/$USERNAME/python3_venvs/casadi_venv/bin/python -m pip install -r /tmp/casadi-requirements.txt \
    && echo "# source /home/$USERNAME/python3_venvs/casadi_venv/bin/activate" >> /home/$USERNAME/.bashrc

## open3d
RUN python3 -m venv /home/$USERNAME/python3_venvs/o3d_venv --system-site-packages --upgrade-deps --symlinks \
    && /home/$USERNAME/python3_venvs/o3d_venv/bin/python -m pip install open3d \
    && /home/$USERNAME/python3_venvs/o3d_venv/bin/python -m pip install numpy==1.24 \
    && echo "# source /home/$USERNAME/python3_venvs/o3d_venv/bin/activate" >> /home/$USERNAME/.bashrc

RUN sudo apt-get update \
    && sudo apt-get -y install --no-install-recommends\
    tmux \
    vim \
    nano \
    tree \
    && sudo apt-get autoremove -y \
    && sudo apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

# Set TERM and colorful prompt in bashrc
RUN echo 'export TERM="xterm-256color"' | sudo tee -a ~/.bashrc > /dev/null && \
    echo "export PS1='\\[\\033[01;32m\\]\\u@\\h:\\[\\033[01;34m\\]\\w\\$\\[\\033[00m\\] '" | sudo tee -a ~/.bashrc > /dev/null

COPY .tmux.conf /home/wheelchair2/.tmux.conf

# Environment variable for map folder
ENV MAP_DIR=/home/$USERNAME/wheelchair2/src/wheelchair2_navigation/maps