# DockerForROS2Development
Docker images for Easy ROS2 development with the wheelchair 

## Humble Image
```bash
# Pull
docker pull ghcr.io/smart-wheelchair-rrc/humble:latest
```

```bash
# Build
docker build -t ghcr.io/smart-wheelchair-rrc/humble -f humble/Dockerfile humble --build-arg USERNAME="wheelchair2"
```

## Wheelchair2 base Image
```bash
# Pull
docker pull ghcr.io/smart-wheelchair-rrc/wheelchair_base:latest
```

```bash
# Build
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

## Credits 
https://github.com/soham2560/DockerForROS2Development

