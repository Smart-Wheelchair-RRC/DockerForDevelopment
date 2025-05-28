FROM noetic_gpu

# Ensure bash is used as the default shell to invoke .bashrc
SHELL ["/bin/bash", "-c"]
ENV ROS_DISTRO=noetic

RUN apt-get update -y \
    && apt-get install -y git wget cmake build-essential \
    && apt-get install -y libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev \
    && apt-get install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev at \
    && apt-get install -y liborocos-bfl-dev ros-noetic-navigation ros-noetic-geometry2 ros-noetic-geographic-info ros-noetic-robot-navigation \
    && apt-get install -y ros-noetic-ddynamic-reconfigure ros-noetic-librealsense2 ros-noetic-ros-numpy \
    && apt-get install -y git wget python3-pip python3-catkin-tools\
    && pip install gdown \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home
ENV WHEELCHAIR_WORKSPACE=/home/wheelchair_ws

# LIVOX SDK
RUN git clone https://github.com/Livox-SDK/Livox-SDK2.git \
    && mkdir Livox-SDK2/build \
    && cd Livox-SDK2/build \
    && cmake .. \
    && make -j \
    && make install \
    && cd /home \
    && rm -rf Livox-SDK2

# turtlebot noetic packages for simulation
RUN wget https://raw.githubusercontent.com/zzuxzt/turtlebot2_noetic_packages/master/turtlebot2_noetic_install.sh
    && sh turtlebot2_noetic_install.sh
    && sudo apt-get install ros-noetic-sophus

# Realsense SDK
RUN git clone https://github.com/IntelRealSense/librealsense.git \
    && mkdir librealsense/build \
    && cd librealsense/build \
    && cmake ../ \
    && make -j$(($(nproc)-1)) all \
    && make install \
    && cd /home \
    && rm -rf librealsense

# LIVOX ROS2 Drivers - Install and build first since it requires a separate build command
RUN git clone https://github.com/Livox-SDK/livox_ros_driver2.git $WHEELCHAIR_WORKSPACE/src/livox_ros_driver2 \
    && cd $WHEELCHAIR_WORKSPACE/src/livox_ros_driver2 \
    && source /opt/ros/${ROS_DISTRO}/setup.bash \
    && ./build.sh ROS1

# Wheelchair Packages
ENV WHEELCHAIR_PACKAGES=${WHEELCHAIR_WORKSPACE}/src/wheelchair

RUN git clone https://github.com/laksh-nanwani/wheelchair-camera-lidar.git \
    && mkdir -p $WHEELCHAIR_PACKAGES \
    && cp -R wheelchair-camera-lidar/workspace/src/* $WHEELCHAIR_PACKAGES \
    && rm -rf $WHEELCHAIR_PACKAGES/depthimage_to_laserscan \
    && rm -rf wheelchair-camera-lidar

RUN git clone https://github.com/laksh-nanwani/voronoi_planner.git $WHEELCHAIR_PACKAGES/voronoi_planner \
    && git clone https://github.com/frontw/dynamicvoronoi.git $WHEELCHAIR_PACKAGES/dynamicvoronoi \
    && git clone https://github.com/Smart-Wheelchair-RRC/FAST_LIO_LOCALIZATION2.git -b noetic --recursive $WHEELCHAIR_PACKAGES/FAST_LIO_LOCALIZATION2

# Load the PCD file
RUN gdown 1vdt7-NKDv4nZnFPBKbx8Y3MMlGgkP_kq -O $WHEELCHAIR_PACKAGES/FAST_LIO_LOCALIZATION2/PCD

WORKDIR $WHEELCHAIR_WORKSPACE

RUN source ${WHEELCHAIR_WORKSPACE}/devel/setup.bash \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y \
    && catkin_make

# Source environments in bashrc
RUN echo "source ${WHEELCHAIR_WORKSPACE}/devel/setup.bash" >> /root/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
