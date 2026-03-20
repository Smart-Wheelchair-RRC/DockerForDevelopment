FROM nvcr.io/nvidia/l4t-jetpack:r36.2.0

# basic args
ARG ROS_DISTRO=humble
ARG USERNAME=container_user
ARG USER_UID=1002
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

# Perform all root-level system modifications first
USER root

# 1. Resolve GID conflicts for Jetson hardware groups (video=44, render=104)
RUN EXISTING_RENDER_GROUP=$(getent group 104 | cut -d: -f1) && \
    if [ ! -z "$EXISTING_RENDER_GROUP" ] && [ "$EXISTING_RENDER_GROUP" != "render" ]; then \
        groupmod -g 9904 "$EXISTING_RENDER_GROUP"; \
    fi && \
    groupmod -g 44 video || true && \
    groupmod -g 104 render || true

# 2. Robust User Creation: Check if name/UID/GID exists before creating
RUN if getent passwd $USERNAME; then \
        usermod -u $USER_UID $USERNAME && \
        groupmod -g $USER_GID $USERNAME || true; \
    else \
        # Evict GID 1002 if it's taken by a system group (like 'nvidia')
        EXISTING_VAL_GROUP=$(getent group $USER_GID | cut -d: -f1); \
        if [ ! -z "$EXISTING_VAL_GROUP" ]; then groupmod -g 9992 "$EXISTING_VAL_GROUP"; fi; \
        groupadd --gid $USER_GID $USERNAME && \
        useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi && \
    # Grant sudo and hardware access
    usermod -aG sudo,video,render,i2c $USERNAME && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# setup entrypoint
COPY ./ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

USER $USERNAME

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