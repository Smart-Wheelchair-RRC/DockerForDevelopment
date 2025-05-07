FROM crowdsurfer_base

RUN apt-get update -y
RUN apt-get install git wget cmake build-essential -y

WORKDIR /home

# LIVOX SDK

RUN git clone https://github.com/Livox-SDK/Livox-SDK2.git
RUN mkdir Livox-SDK2/build && cd Livox-SDK2/build \
    && cmake .. \
    && make -j \
    && make install

## Realsense SDK

RUN apt-get install libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev -y
RUN apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev at -y

RUN git clone https://github.com/IntelRealSense/librealsense.git
RUN mkdir librealsense/build && cd librealsense/build \
    && cmake ../ \
    && make -j$(($(nproc)-1)) all \
    && make install 

# LIVOX ROS2 Drivers

RUN git clone https://github.com/Livox-SDK/livox_ros_driver2.git CrowdSurfer_ws/src/livox_ros_driver2
RUN cd CrowdSurfer_ws/src/livox_ros_driver2 \
    && source /opt/ros/noetic/setup.bash \
    && ./build.sh ROS1

# Wheelchair Packages

RUN git clone https://github.com/laksh-nanwani/wheelchair-camera-lidar.git

RUN mkdir CrowdSurfer_ws/src/wheelchair \
    && cp -R wheelchair-camera-lidar/workspace/src/* CrowdSurfer_ws/src/wheelchair \
    && rm -rf CrowdSurfer_ws/src/wheelchair/depthimage_to_laserscan \
    && rm -rf wheelchair-camera-lidar

RUN git clone https://github.com/laksh-nanwani/voronoi_planner.git CrowdSurfer_ws/src/wheelchair/voronoi_planner
RUN git clone https://github.com/frontw/dynamicvoronoi.git CrowdSurfer_ws/src/wheelchair/dynamicvoronoi
RUN git clone https://github.com/Smart-Wheelchair-RRC/FAST_LIO_LOCALIZATION2.git -b noetic --recursive CrowdSurfer_ws/src/wheelchair/FAST_LIO_LOCALIZATION2

# Load the PCD file
RUN gdown 1vdt7-NKDv4nZnFPBKbx8Y3MMlGgkP_kq -O CrowdSurfer_ws/src/wheelchair/FAST_LIO_LOCALIZATION2/PCD

RUN apt-get install -y liborocos-bfl-dev ros-noetic-navigation ros-noetic-geometry2 ros-noetic-geographic-info ros-noetic-robot-navigation
RUN apt-get install ros-noetic-ros-numpy -y

RUN cd CrowdSurfer_ws \
    && rosdep install --from-paths src --ignore-src -r -y

RUN catkin_make

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /home/CrowdSurfer_ws

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]