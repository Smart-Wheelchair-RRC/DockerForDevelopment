FROM nvidia/cuda:12.2.2-base-ubuntu22.04



# basic args
ARG ROS_DISTRO=humble
ARG USERNAME=container_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Add metadata labels
LABEL org.opencontainers.image.description="Docker Development Container"
LABEL org.opencontainers.image.title="RRC Humble"
LABEL org.opencontainers.image.vendor="Tarun R"
LABEL org.opencontainers.image.source="https://github.com/Smart-Wheelchair-RRC/DockerForDevelopment"
LABEL maintainer="tarun.ramak@gmail.com"
LABEL org.opencontainers.image.licenses="MIT"

# configure bash shell
SHELL ["/bin/bash", "-c"]
ENV SHELL=/bin/bash

# set ROS distro env
ENV ROS_DISTRO=$ROS_DISTRO
ENV GZ_VERSION=harmonic

# setup locales
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# setup timezone
RUN echo 'Asia/Kolkata' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime

# install packages
COPY aptPkgs.list /tmp/aptPkgs.list
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    dirmngr \
    gnupg2 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Setup ROS Apt sources
RUN curl -L -s -o /tmp/ros2-apt-source.deb https://github.com/ros-infrastructure/ros-apt-source/releases/download/1.1.0/ros2-apt-source_1.1.0.jammy_all.deb \
    && echo "1600cb8cc28258a39bffc1736a75bcbf52d1f2db371a4d020c1b187d2a5a083b /tmp/ros2-apt-source.deb" | sha256sum --strict --check \
    && apt-get update \
    && apt-get install /tmp/ros2-apt-source.deb \
    && rm -f /tmp/ros2-apt-source.deb \
    && rm -rf /var/lib/apt/lists/*

# install packages
COPY aptPkgs.list /tmp/aptPkgs.list
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    $(cat /tmp/aptPkgs.list) \
    ros-$ROS_DISTRO-desktop \
    && rm -rf /var/lib/apt/lists/*

# Create non root user with sudo privilege
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

# setup entrypoint
COPY ./ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]

# bootstrap rosdep
RUN sudo rosdep init && \
    rosdep update --rosdistro $ROS_DISTRO

# setup colcon mixin and metadata
RUN sudo colcon mixin add default \
    https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml && \
    sudo colcon mixin update && \
    sudo colcon metadata add default \
    https://raw.githubusercontent.com/colcon/colcon-metadata-repository/master/index.yaml && \
    sudo colcon metadata update

RUN sudo pip3 install -U \
    argcomplete

# echo sources
RUN echo 'source /usr/share/bash-completion/bash_completion' | sudo tee -a ~/.bashrc > /dev/null && \
    echo 'source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash' | sudo tee -a ~/.bashrc > /dev/null && \
    echo "source /opt/ros/${ROS_DISTRO}/setup.bash" | sudo tee -a ~/.bashrc > /dev/null && \
    echo 'eval "$(register-python-argcomplete3 ros2)"' | sudo tee -a ~/.bashrc > /dev/null && \
    echo 'eval "$(register-python-argcomplete3 colcon)"' | sudo tee -a ~/.bashrc > /dev/null



# Install gazebo harmonic from osrf
RUN sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && sudo apt-get update \
    && sudo apt-get install -y gz-harmonic \
    && sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update && sudo apt-get install -y ros-$ROS_DISTRO-ros-gzharmonic

RUN sudo bash -c 'wget https://raw.githubusercontent.com/osrf/osrf-rosdep/master/gz/00-gazebo.list -O /etc/ros/rosdep/sources.list.d/00-gazebo.list' \
    && rosdep update \
    && rosdep resolve gz-harmonic 

WORKDIR /home/$USERNAME/gz_ros2_control_ws/src
RUN git clone --depth=1 --progress --verbose https://github.com/ros-controls/gz_ros2_control -b $ROS_DISTRO . \
    && export GZ_VERSION=harmonic \
    && rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y --skip-keys="ros_gz_bridge ros_gz_sim" 

WORKDIR /home/$USERNAME/gz_ros2_control_ws
RUN source /opt/ros/$ROS_DISTRO/setup.bash \
    && colcon build \
    && echo "source ~/gz_ros2_control_ws/install/setup.bash" | sudo tee -a ~/.bashrc > /dev/null  

RUN sudo mkdir -p /opt/nvidia/
COPY NVIDIA-OptiX-SDK-7.2.0-linux64-x86_64/ /opt/nvidia/NVIDIA-OptiX-SDK-7.2.0-linux64-x86_64/
ENV OptiX_INSTALL_DIR=/opt/nvidia/NVIDIA-OptiX-SDK-7.2.0-linux64-x86_64/

WORKDIR /home/$USERNAME
RUN git clone --depth=1 --progress --verbose https://github.com/RobotecAI/RGLGazeboPlugin.git \
    && cd RGLGazeboPlugin \
    && mkdir build && cd build \
    && cmake .. && sudo make -j && sudo make install

# Environment variable for RGLGazeboPlugin
ENV GZ_GUI_PLUGIN_PATH=/home/$USERNAME/RGLGazeboPlugin/install/RGLVisualize
ENV GZ_SIM_SYSTEM_PLUGIN_PATH=/home/$USERNAME/RGLGazeboPlugin/install/RGLServerPlugin
ENV RGL_PATTERNS_DIR=/home/$USERNAME/RGLGazeboPlugin/lidar_patterns