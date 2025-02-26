# DockerForROS2Development
Docker images for Easy ROS2 development with the wheelchair.
- The humble image contains the base ROS2 humble build with basic dependencies.  
- The wheelchair base image takes in humble image and adds Livox and Realsense SDK's and few other basic ROS2 packages.  
## Humble Image
```bash
docker pull ghcr.io/smart-wheelchair-rrc/humble:latest
```

```bash
docker build -t ghcr.io/smart-wheelchair-rrc/humble -f humble/Dockerfile humble --build-arg USERNAME="wheelchair2"
```

## Wheelchair2 base Image
```bash
docker pull ghcr.io/smart-wheelchair-rrc/wheelchair_base:latest
```

```bash
docker build -t ghcr.io/smart-wheelchair-rrc/wheelchair2_base -f wheelchair2_base/Dockerfile wheelchair2_base --build-arg USERNAME="wheelchair2"
```

## Create Tag and Push

> Always create tags from the master branch

```bash
git checkout master
git pull
# Replace X.X.X with the version number
git tag vX.X.X
git push origin --tags
```

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

## Credits 
https://github.com/soham2560/DockerForROS2Development

