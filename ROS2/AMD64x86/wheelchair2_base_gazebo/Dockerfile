FROM ghcr.io/smart-wheelchair-rrc/humble_gazebo:v5.2

ARG USERNAME=container_user

# Add the following labels
LABEL org.opencontainers.image.description="Wheelchair2"
LABEL org.opencontainers.image.title="Wheelchair2DevCon"
LABEL org.opencontainers.image.vendor="Tarun R"
LABEL org.opencontainers.image.source="https://github.com/Smart-Wheelchair-RRC/DockerForDevelopment"
LABEL maintainer="tarun.ramak@gmail.com"
LABEL org.opencontainers.image.licenses="MIT"


# Build and install Realsense-SDK
WORKDIR /home/$USERNAME
RUN git clone --depth=1 --progress --verbose https://github.com/IntelRealSense/librealsense.git # --branch v2.56.2
WORKDIR /home/$USERNAME/librealsense
RUN sudo mkdir -p /etc/udev/rules.d && \
    ./scripts/setup_udev_rules.sh \
    ./scripts/patch-realsense-ubuntu-lts-hwe.sh 
RUN mkdir build && cd build \
    && cmake ../ \
    && sudo make uninstall -j4 && make clean && make -j4 && sudo make install -j4

# Build and install Livox-SDK2
WORKDIR /home/$USERNAME
RUN git clone --depth=1 --progress --verbose https://github.com/Smart-Wheelchair-RRC/Livox-SDK2.git 
RUN cd Livox-SDK2 \
    && mkdir build \
    && cd build \
    && cmake .. && make -j \
    && sudo make install -j4

COPY rosPkgs.list /tmp/rosPkgs.list
RUN sudo apt-get update \
    && sudo apt-get -y install --no-install-recommends $(cat /tmp/rosPkgs.list) \
    && sudo rm -rf /var/lib/apt/lists/*

COPY pythonPkgs.list /tmp/pythonPkgs.list
RUN sudo apt-get update \
    && pip3 install $(cat /tmp/pythonPkgs.list) \
    && sudo rm -rf /var/lib/apt/lists/*

# 3D-BBS
WORKDIR /home/container_user
RUN git clone https://github.com/KOKIAOKI/3d_bbs.git --recursive --depth 1
RUN cd 3d_bbs \
    && mkdir build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda && make \
    && sudo make install \
    && cd /home/container_user \
    && rm -rf 3d_bbs


    #Install Miniconda
# RUN mkdir -p ~/miniconda3 && \
#     wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh && \
#     bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
#     rm ~/miniconda3/miniconda.sh && \
#     source ~/miniconda3/bin/activate && \
#     conda init --all && \ 
#     conda config --set auto_activate_base false

# Set TERM and colorful prompt in bashrc
RUN echo 'export TERM="xterm-256color"' | sudo tee -a ~/.bashrc > /dev/null && \
    echo "export PS1='\\[\\033[01;32m\\]\\u@\\h:\\[\\033[01;34m\\]\\w\\$\\[\\033[00m\\] '" | sudo tee -a ~/.bashrc > /dev/null

COPY .tmux.conf /home/$USERNAME/.tmux.conf

# Environment variable for map folder
ENV MAP_DIR=/home/$USERNAME/wheelchair2/src/wheelchair2_navigation/maps

# handle default shell
SHELL ["/bin/bash", "-c"]