## Hierarchy of Dockerfiles to be Built

1. **noetic_gpu** (base image: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04`)    
- Sets up the CUDA environment with ROS Noetic.
- Installs Python, pip, ROS Noetic packages, and other basic utilities.
- Prepares the container with the ros_entrypoint.sh for launching ROS.
```bash
docker build -t noetic_gpu -f ROS1/noetic_gpu/Dockerfile ROS1/noetic_gpu
```

2. **wheelchair1_base** (base image: `noetic_gpu`) 
```bash
docker build -t wheelchair1_base -f ROS1/wheelchair1_base/Dockerfile`
```

3. **crowdsurfer** (base image: `wheelchair1_base`)
```bash
docker build -t crowdsurfer -f ROS1/crowdsurfer/Dockerfile`
```

4. **crowdsurfer_only** (base image: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04`)
```bash
docker build -t crowdsurfer_only -f ROS1/crowdsurfer_only/Dockerfile
```