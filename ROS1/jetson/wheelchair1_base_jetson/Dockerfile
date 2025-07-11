FROM noetic_base

# Add the following labels
LABEL org.opencontainers.image.description="Wheelchair1-Jetson"
LABEL org.opencontainers.image.title="Wheelchair1BaseJetson"
LABEL org.opencontainers.image.source="https://github.com/Smart-Wheelchair-RRC/DockerForDevelopment"
LABEL org.opencontainers.image.licenses="MIT"
# handle default shell
SHELL ["/bin/bash", "-c"]


RUN apt-get update -y

WORKDIR /home/wheelchair

####################
# Librealsense
#####################

RUN apt-get install libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev -y
RUN apt-get install git wget cmake build-essential -y

RUN apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev at -y

RUN git clone https://github.com/IntelRealSense/librealsense.git

WORKDIR /home/wheelchair/librealsense

RUN mkdir build

WORKDIR /home/wheelchair/librealsense/build

RUN cmake ../
RUN make uninstall && make clean && make && make install
#####################

WORKDIR /home/wheelchair

#####################
# Livox SDK2
#####################

RUN git clone https://github.com/Livox-SDK/Livox-SDK2.git

WORKDIR /home/wheelchair/Livox-SDK2
RUN mkdir build

WORKDIR /home/wheelchair/Livox-SDK2/build
RUN cmake .. && make -j && make install
#####################

WORKDIR /home/wheelchair

#####################
# Livox Ros Driver2
#####################

RUN mkdir -p /home/wheelchair/ws_livox/src

# WORKDIR /home/ws_livox/src

RUN git clone https://github.com/Livox-SDK/livox_ros_driver2.git ws_livox/src/livox_ros_driver2

WORKDIR /home/wheelchair/ws_livox/src/livox_ros_driver2

RUN source /opt/ros/noetic/setup.bash && ./build.sh ROS1
#####################

WORKDIR /home/wheelchair

#####################
# Wheelchair1 repo
#####################

RUN git clone https://github.com/laksh-nanwani/wheelchair-camera-lidar.git

WORKDIR /home/wheelchair/wheelchair-camera-lidar/workspace/src/dependencies

RUN git clone https://github.com/laksh-nanwani/voronoi_planner.git
RUN git clone https://github.com/frontw/dynamicvoronoi.git

# WORKDIR /home/wheelchair-camera-lidar/workspace

RUN apt-get install -y liborocos-bfl-dev ros-noetic-navigation ros-noetic-geometry2 ros-noetic-geographic-info ros-noetic-robot-navigation

WORKDIR /home/wheelchair/wheelchair-camera-lidar/workspace

RUN rosdep install --from-paths src --ignore-src -r -y

RUN source /opt/ros/noetic/setup.bash && catkin_make
#####################

# RUN sed -i "source /home/wheelchair/wheelchair-camera-lidar/workspace/devel/setup.bash" ~/.bashrc
RUN rm -rf /var/lib/apt/lists/*

USER wheelchair
WORKDIR /home/wheelchair
RUN echo "source /home/ws_livox/devel/setup.bash" >> ~/.bashrc
RUN echo "/home/wheelchair/wheelchair-camera-lidar/workspace/setup.bash" >> ~/.bashrc


ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
