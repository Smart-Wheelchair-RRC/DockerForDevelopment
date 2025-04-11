## Hierarchy of Dockerfiles to be Built

1. **noetic_cuda11.8_x86** (base image: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04`)  
   *Call file name: `cuda_ros_docker`*  
   - Sets up the CUDA environment with ROS Noetic.
   - Installs Python, pip, ROS Noetic packages, and other basic utilities.
   - Prepares the container with the ros_entrypoint.sh for launching ROS.
   
   Docker build command:  
   `docker build -t cuda_ros_docker -f ROS1/noetic_cuda11.8_x86/dockerfile ROS1/noetic_cuda11.8_x86`

2. **ros1_crowdsurfer_base_x86** (base image: `cuda_ros_docker`)  
   *Call file name: `crowdsurfer_base`*  
   - Extends the CUDA-based image to include additional dependencies.
   - Installs extra packages and Python libraries needed for the Crowdsurfer base.
   - Serves as the foundation for further ROS1 development for crowdsurfer applications.
   
   Docker build command:  
   `docker build -t crowdsurfer_base -f ROS1/ros1_crowdsurfer_base_x86/dockerfile ROS1/ros1_crowdsurfer_base_x86`

3. **crowdsurfer_ros1_x86** (base image: `crowdsurfer_base`)  
   *Call file name: `crowdsurfer`*  
   - Clones and sets up robotics and simulation repositories.
   - Installs tools like gdown and additional ROS packages.
   - Configures a workspace for building and running the Crowdsurfer ROS1 application.
   
   Docker build command:  
   `docker build -t crowdsurfer -f ROS1/crowdsurfer_ros1_x86/dockerfile ROS1/crowdsurfer_ros1_x86`

4. **wheelchair1_crowdsurfer_x86** (base image: `crowdsurfer`)  
   *Call file name: `wheelchair1_crowdsurfer`*  
   - Builds on the Crowdsurfer container by integrating hardware drivers.
   - Installs and compiles Librealsense and Livox SDK2.
   - Clones and configures the wheelchair camera–lidar application.
   - Prepares the final image for running the complete wheelchair integration.
   
   Docker build command:  
   `docker build -t wheelchair1_crowdsurfer -f ROS1/wheelchair1_crowdsurfer_x86/dockerfile ROS1/wheelchair1_crowdsurfer_x86`