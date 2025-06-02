FROM ubuntu:jammy

# basic args
ARG ROS_DISTRO=humble
ARG USERNAME=wheelchair2
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Add the following labels
LABEL org.opencontainers.image.description="Docker Development Container"
LABEL org.opencontainers.image.title="ROS2Dev"
LABEL org.opencontainers.image.vendor="Tarun R"
LABEL org.opencontainers.image.source="https://github.com/Smart-Wheelchair-RRC/DockerForDevelopment"
LABEL maintainer="tarun.ramak@gmail.com"
LABEL org.opencontainers.image.licenses="MIT"

# handle default shell
SHELL ["/bin/bash", "-c"]
ENV SHELL=/bin/bash

# setup timezone
RUN echo 'Asia/Kolkata' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

# install packages
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    dirmngr \
    gnupg2 \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# enable the universe repository
# info: https://help.ubuntu.com/community/Repositories/Ubuntu
RUN add-apt-repository universe

# Setup the ROS 2 apt repository
# Guidance source 1: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html#setup-sources
# Guidance source 2: https://discourse.ros.org/t/ros-signing-key-migration-guide/43937
# Guidance source 3: https://github.com/osrf/docker_images/commit/13a4d90a845353eb95146b9c016b8fd933e272e0
RUN     apt update && apt install curl -y \
    &&  export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}') \" \
    &&  curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb" \
    &&  install /tmp/ros2-apt-source.deb

# setup environment
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Create non root user with sudo privilege
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

ENV ROS_DISTRO=$ROS_DISTRO

# install ros2 packages
RUN sudo apt-get update --allow-releaseinfo-change && sudo apt-get install -y --no-install-recommends \
    ros-$ROS_DISTRO-desktop \
    && sudo rm -rf /var/lib/apt/lists/*

# setup entrypoint
COPY ./ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]

# install bootstrap tools
RUN sudo apt-get update --allow-releaseinfo-change && sudo apt-get install --no-install-recommends -y \
    build-essential \
    git \
    bash-completion \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-rosdep \
    python3-vcstool \
    python3-pip \
    && sudo rm -rf /var/lib/apt/lists/*

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