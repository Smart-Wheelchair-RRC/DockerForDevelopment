FROM ghcr.io/smart-wheelchair-rrc/humble_cuda:v5.1

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
    && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j \
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
# Build and install GTSAM
WORKDIR /home/$USERNAME
RUN git clone https://github.com/borglab/gtsam \
    && cd gtsam \
    && git checkout 4.3a0 \
    && mkdir build && cd build \
    && cmake .. -DGTSAM_BUILD_EXAMPLES_ALWAYS=OFF \
         -DGTSAM_BUILD_TESTS=OFF \
         -DGTSAM_WITH_TBB=OFF \
         -DGTSAM_USE_SYSTEM_EIGEN=ON \
         -DGTSAM_BUILD_WITH_MARCH_NATIVE=OFF \
    && make -j$(nproc) \
    && sudo make install \
    && cd ../.. \
    && sudo rm -rf gtsam

WORKDIR /home/$USERNAME
RUN git clone https://github.com/koide3/iridescence --recursive \
    && cd iridescence \
    && mkdir build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release \
    && make -j$(nproc) \
    && sudo make install \
    && cd ../.. \
    && sudo rm -rf iridescence
    
WORKDIR /home/$USERNAME
RUN git clone https://github.com/koide3/gtsam_points \
    && cd gtsam_points \
    && git checkout v1.2.0 \
    && mkdir build && cd build \
    && cmake .. -DBUILD_WITH_CUDA=ON \
    && make -j$(nproc) \
    && sudo make install \
    && cd ../.. \
    && sudo rm -rf gtsam_points

# glim using cmake method
WORKDIR /home/$USERNAME
RUN git clone --recursive https://github.com/koide3/glim.git /tmp/glim \
    && cd /tmp/glim \
    && git checkout v1.1.0 \
    && git submodule update --init --recursive \
    && mkdir build && cd build \
    && cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_WITH_CUDA=ON \
    && make -j$(nproc) \
    && sudo make install \
    && rm -rf /tmp/glim

# Build and install glim_ros v1.1.0 from source via CMake
WORKDIR /home/$USERNAME
RUN git clone --recursive https://github.com/koide3/glim_ros2.git /tmp/glim_ros2 \
    && cd /tmp/glim_ros2 \
    && git checkout v1.1.0 \
    && git submodule update --init --recursive \
    && mkdir build && cd build \
    && source /opt/ros/${ROS_DISTRO}/setup.bash \
    && cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
    && make -j$(nproc) \
    && sudo make install \
    && rm -rf /tmp/glim_ros2

RUN sudo ldconfig
# Set TERM and colorful prompt in bashrc
RUN echo 'export TERM="xterm-256color"' | sudo tee -a ~/.bashrc > /dev/null && \
    echo "export PS1='\\[\\033[01;32m\\]\\u@\\h:\\[\\033[01;34m\\]\\w\\$\\[\\033[00m\\] '" | sudo tee -a ~/.bashrc > /dev/null

COPY .tmux.conf /home/$USERNAME/.tmux.conf

# Environment variable for map folder
ENV MAP_DIR=/home/$USERNAME/wheelchair2/src/wheelchair2_navigation/maps

# handle default shell
SHELL ["/bin/bash", "-c"]
