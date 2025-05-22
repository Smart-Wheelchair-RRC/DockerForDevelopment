FROM wheelchair1_base

SHELL ["/bin/bash", "-c"]

WORKDIR /home
ENV WHEELCHAIR_WORKSPACE=/home/wheelchair_ws
ENV CROWDSURFER_WORKSPACE=${WHEELCHAIR_WORKSPACE}/src/CrowdSurfer
ENV CROWDSURFER_PATH=${CROWDSURFER_WORKSPACE}/src/CrowdSurfer

# Install required packages and clean up
RUN apt-get update -y \
    && apt-get install -y git wget python3-pip \
    && pip install gdown \
    && rm -rf /var/lib/apt/lists/*

# Clone repositories
RUN git clone https://github.com/Smart-Wheelchair-RRC/CrowdSurfer.git $CROWDSURFER_WORKSPACE \
    && git clone https://github.com/TempleRAIL/robot_gazebo.git $WHEELCHAIR_WORKSPACE/src/robot_gazebo \
    && git clone https://github.com/Smart-Wheelchair-RRC/pedsim_ros_with_gazebo.git $WHEELCHAIR_WORKSPACE/src/pedsim_ros_with_gazebo

# Setup Python environment for CrowdSurfer
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv venv --python 3.10 --system-site-packages ${CROWDSURFER_PATH}/.venv \
    && uv sync --active --project ${CROWDSURFER_PATH}

# Download checkpoints
RUN mkdir -p ${CROWDSURFER_PATH}/checkpoints \
    && gdown https://drive.google.com/drive/folders/1HSRrbuwwNk9_C1WKN9qnStjemFLukO8s --folder -O ${CROWDSURFER_PATH}/checkpoints

# Install Turtlebot2 Noetic packages
RUN wget https://raw.githubusercontent.com/zzuxzt/turtlebot2_noetic_packages/master/turtlebot2_noetic_install.sh \
    && bash turtlebot2_noetic_install.sh \
    && rm turtlebot2_noetic_install.sh

WORKDIR ${WHEELCHAIR_WORKSPACE}

# Install ROS dependencies and build
RUN rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y \
    && catkin_make

# Source environments in bashrc
RUN echo "source ${CROWDSURFER_PATH}/.venv/bin/activate" >> /root/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["/bin/bash", "-c"]
