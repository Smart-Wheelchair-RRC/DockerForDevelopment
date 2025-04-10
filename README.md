# DockerForROS2Development
Docker images for Easy ROS1 and ROS2 development with the wheelchair.

## Available Images

The following Docker images are available:

-   `humble`:  Based on `ubuntu:jammy`, this image includes ROS 2 Humble Hawksbill packages and a non-root user for enhanced security.
-   `wheelchair2_base`:  Extends the `humble` image and includes Realsense and Livox SDK's
-   `humble_jetson`:  Based on `ubuntu:jammy for ARM64`, this image includes ROS 2 Humble Hawksbill packages and a non-root user for enhanced security.
-   `wheelchair2_base_jetson`:  Extends the `humble_jetson` image and includes Realsense and Livox SDK's 

**Important Note:** The `ROS1` images are currently **under development** and have not been heavily tested.  They may be unstable or contain significant bugs.
 
 
## Usage

### 1. Pulling an Image

To download a pre-built image from GitHub Container Registry (ghcr.io), use the following command:

```bash
docker pull ghcr.io/smart-wheelchair-rrc/<image_name>:latest
```

Replace `<image_name>` with the desired image name (e.g., `humble`, `wheelchair2_base`). For example:

```bash
docker pull ghcr.io/smart-wheelchair-rrc/humble:latest
```

### 2. Building an Image (Optional)

If you prefer to build the image locally from the Dockerfile, clone this repository and navigate to the root directory.  Then, use the following command:

```bash
docker build -t ghcr.io/smart-wheelchair-rrc/<image_name> -f <image_name>/Dockerfile <image_name>
```

Again, replace `<image_name>` with the appropriate image name. For example, to build the `humble` image:

```bash
docker build -t ghcr.io/smart-wheelchair-rrc/humble -f humble-garden/Dockerfile humble
```

**Explanation of the `docker build` command:**

*   `docker build`: The command to build a Docker image.
*   `-t ghcr.io/smart-wheelchair-rrc/<image_name>`:  Tags the image with the specified name and registry path.
*   `-f <image_name>/Dockerfile`: Specifies the path to the Dockerfile to use for building the image.
*   `<image_name>`:  The build context, which is the directory containing the Dockerfile and any other files needed for the build.

### 3. Pushing an Image (For Contributors)

If you have made changes to the Dockerfile and want to contribute by pushing the updated image to the registry, use the following command:

```bash
docker push ghcr.io/smart-wheelchair-rrc/<image_name>:latest
```

**Note:**  You need to be authenticated with `ghcr.io` and have the appropriate permissions to push images to the `smart-wheelchair-rrc` repository.

### Debugging 

>The docker throws " Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running? " error, even after restarting docker, do the following:

- Docker networking requires IP forwarding. Check if it's enabled:
    ```bash
    sysctl net.ipv4.ip_forward
    ```
- If it returns 0, enable it with:
    ```bash
    sudo sysctl -w net.ipv4.ip_forward=1
    ```
- Then restart Docker:
    ```bash
    sudo systemctl restart docker
    ```

## Acknowledgements

This work is inspired by the work of [soham2560](https://github.com/soham2560/DockerForROS2Development).

