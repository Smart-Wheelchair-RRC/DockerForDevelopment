# Docker for ROS Development

This repository provides ROS1 and ROS2 Docker images for easy development with the wheelchair.

This documentation is split into four parts:

- [List of features and images](#list-of-ros2-features-and-images)
- [Instructions for everyone (GHCR authentication)](#authenticating-to-github-container-registry)
- [How to use an image](#pulling-an-image)
- [How to build an image](#building-an-image)

> [!NOTE]
> This repository uses GitHub Actions for CI/CD. Further documentation on how we have implemented this is available in the [CI/CD documentation](/.github/workflows/README.md).

## List of ROS2 Features and Images

| Image name | Base image | Intended target | Features |
| --- | --- | --- | --- |
| `humble` | [`ubuntu:jammy`](https://hub.docker.com/_/ubuntu) | x86\_64 laptop | - ROS2 Humble Hawksbill packages <br> - non-root user |
| `humble_gpu` | [`nvidia/cuda:12.2.2-devel-ubuntu22.04`](https://hub.docker.com/r/nvidia/cuda) | x86\_64 laptop | - ROS2 Humble Hawksbill packages <br> - CUDA <br> - CuDNN <br> - non-root user |
| `wheelchair2_base` | `humble` | x86\_64 laptop | - Realsense SDK <br> - Livox SDK |
| `wheelchair_2_base_gazebo` | `humble_gpu` | x86\_64 laptop | - ros2\_control <br> - RGLGazeboPlugin <br> - Nvidia Optix for gz-sim <br> - Realsense SDK <br> - Livox SDK <br> - Gazebo Harmonic |
| `humble_jetson` | [`nvcr.io/nvidia/l4t-jetpack`](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-jetpack) | Jetson (ARM64) | - ROS2 Humble Hawksbill packages <br> - non-root user |
| `wheelchair2_base_jetson` | `humble_jetson` | Jetson (ARM64) | - Realsense SDK <br> - Livox SDK |

> [!CAUTION]
> The ROS1 images are currently **under development** and have not been heavily tested. They may be unstable or contain significant bugs.

## Authenticating to GitHub Container Registry
To pull or push images to the GitHub Container Registry, you need to authenticate using a personal access token (PAT) with the `write:packages` and `repo` scopes.

Brief steps are given below, but you can find more detailed instructions in the [GitHub documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic).
1.  Create a personal access token (PAT) with the required scopes.
2.  Log in to the GitHub Container Registry using the following command:

    ```bash
    echo <YOUR_PAT> | docker login ghcr.io -u <YOUR_GITHUB_USERNAME> --password-stdin
    ```

3.  Verify that you are logged in by running:

    ```bash
    docker info
    ```

### Debugging
If docker throws the error even after restarting the Docker daemon:

```txt
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

You can try the following steps:

1.  Docker networking requires IP forwarding. Check if it's enabled:
    ```bash
    sysctl net.ipv4.ip_forward
    ```

1.  If it returns `0`, enable it with:

    ```bash
    sudo sysctl -w net.ipv4.ip_forward=1
    ```

1.  Then restart the Docker daemon:

    ```bash
    sudo systemctl restart docker
    ```

### Git clones inside the Dockerfile
When we're building a package from a GitHub repository, we only need the latest commits. We achieve this using the `--depth=1` option in the `git clone` command. This option tells Git to clone only the latest commit, which is sufficient for building the package.

Moreover, Git usually doesn't print logs to stdout when run in a container, but these are very useful for debugging. We enable these using the `--progress --verbose` flags.

Therefore, a complete `git clone` command would look like this:

```bash
git clone --depth=1 --progress --verbose <repository_url>
```

As an example:

```bash
git clone --depth=1 --progress --verbose https://github.com/rtarun1/Livox-SDK2.git 
```

## Pulling an image

To download a pre-built image from GitHub Container Registry (ghcr.io), use the following command:

```bash
docker pull ghcr.io/smart-wheelchair-rrc/<image_name>:<tag>
```

Replace `<image_name>` with the desired image name (e.g., `humble`, `wheelchair2_base`). For example:

```bash
docker pull ghcr.io/smart-wheelchair-rrc/humble:v3.0
```

> [!IMPORTANT]
> Please be mindful of the tag you are pulling. The `latest` tag is not used in this repository, so you need to provide a specific version tag (e.g., `v3.0`).

## Building an image
Since this repository uses CI/CD builds, certain considerations must be taken into account when building images:

1.  **Dependant images**

    Certain images depend on other images. For example, `wheelchair2_base_gazebo` depends on `humble_gpu`. If you want to build `wheelchair2_base_gazebo`, you need to build `humble_gpu` first.

    You can specify the dependant image using the `BASE_IMAGE` argument in the Dockerfile. For example, when building `wheelchair2_base_gazebo`, you should specify the base image as follows:

    ```bash
    --build-arg BASE_IMAGE=ghcr.io/smart-wheelchair-rrc/humble_gpu:v3.0
    ```

    Again, please be mindful of the tag you are using. If you update a base image, and you want the changes to reflect in the dependant image, you need to rebuild the dependant image **with the correct tag of the base image**.

1.  **Online builds must be tagged**

    The CI/CD system **will not initiate builds** if the image is not tagged. Moreover, your tag must follow the [SemVer](https://semver.org/spec/v2.0.0.html) format. For example: `v3`, `v3.0`, `v3.1.0`. So your tag names must start with `v` and be followed by a version number.

    Once a commit has been tagged and pushed to the repository, the CI/CD system will automatically build the image and push it to the GitHub Container Registry. It will attempt to do this regardless of the branch you are on.

1.  **Building locally**

    If you want to build locally, you're free to use any tags you like, however you should be mindful of dependant images and their tags. You can build an image using the following command:

    ```bash
    docker build --build-arg BASE_IMAGE=<base_image>:<tag> -t ghcr.io/smart-wheelchair-rrc/<image_name>:<tag> -f <path/to/Dockerfile> <build_context>
    ```

    Replace `<image_name>` with the desired image name, `<tag>` with the version tag, and `<build_context>` with the directory containing the Dockerfile. For example, to build the `humble` image:

    ```bash
    docker build --build-arg BASE_IMAGE=ubuntu:jammy -t ghcr.io/smart-wheelchair-rrc/humble:v3.0 -f ROS2/humble/Dockerfile ROS2/humble
    ```

1.  **Pushing the image**

    After building the image, you can push it to the GitHub Container Registry using the following command:

    ```bash
    docker push ghcr.io/smart-wheelchair-rrc/<image_name>:<tag>
    ```

    For example, to push the `humble` image:

    ```bash
    docker push ghcr.io/smart-wheelchair-rrc/humble:v3.0
    ```

> [!IMPORTANT]
> Avoid using the `latest` tag.

> [!NOTE]
> For your convenience, a [JSON file](combinations.json) containing with all compatible images and their tags is available in the repository. Additionally, you can use the provided [Python script](build.py) to automatically generate the build command for any image you want to build.
>
> ```bash
> python3 build.py <image_name> <tag>
> ```
>
> Example:
> ```bash
> python3 build.py wheelchair2_base_gazebo v3.0
> ```
> Outputs:
> ```bash
> docker build --build-arg BASE_IMAGE=ghcr.io/smart-wheelchair-rrc/humble_gpu:v3.1 -t ghcr.io/smart-wheelchair-rrc/wheelchair2_base_gazebo:v3.0 -f ROS2/wheelchair2_base_gazebo/Dockerfile ROS2/wheelchair2_base_gazebo
> ```

### Explanation of the `docker build` command

The [`docker build` command](https://docs.docker.com/reference/cli/docker/buildx/build/) is used to create a Docker image from a Dockerfile. Here's a breakdown of the command and its arguments:

```bash
docker build --build-arg BASE_IMAGE=<base_image>:<tag> -t ghcr.io/smart-wheelchair-rrc/<image_name>:<tag> -f <path/to/Dockerfile> <build_context>
```

| Argument | Value | Example | Description |
| --- | --- | --- | --- |
| `--build-arg` | `BASE_IMAGE=<base_image>:<tag>` | `BASE_IMAGE=ghcr.io/smart-wheelchair-rrc/humble_gpu:v3.0` | Specifies the base image to use for building the Docker image. This is useful for images that depend on other images. |
| `-t` | `ghcr.io/smart-wheelchair-rrc/<image_name>:<tag>` | `ghcr.io/smart-wheelchair-rrc/humble:v3.0` | Tags the image with the specified name and version tag. |
| `-f` | `<path/to/Dockerfile>` | `ROS2/AMD64x86/humble/Dockerfile` | Specifies the path to the Dockerfile to use for building the image. |
|  | `<build_context>` | `ROS2/AMD64x86/humble` | The build context, which is the directory containing the Dockerfile and any other files needed for the build. |

### Recommendations for tagging images
Suggestions for filling in the SemVer version tag.

Let us assume that the latest image before you start working is `v3.14`. Therefore, the next image you target to release will be `v3.15`.

However, the CI/CD workflow requires that you tag every commit where you want to build an image AND GitHub requires commit tags to be unique. If you wish to use the online builds to test your changes, you can use the `dev*` tags. For example, you can tag your commit as `dev3.15.0` or `dev3.15.1`. This way, you can test your changes without affecting the main versioning scheme.

When you are ready to release the next version (most likely a merge commit), you can tag it as `v3.15.0` or `v3.15`. This will trigger the CI/CD workflow to build the image with the correct version tag.

> [!NOTE]
> - `v*` tags only work on the `master` branch.
> - `dev*` tags can be used on any branch (including `master`).
> - While the `latest` tag is supported on the `master` branch, it is **not recommended** to use it. Instead, prefer specific version tags like `v3.15` or `v3.15.0`.
>
> Both tags will trigger the workflow and push the image to GHCR.

### Git clones inside the Dockerfile
When we're building a package from a GitHub repository, we only need the latest commits. We achieve this using the `--depth=1` option in the `git clone` command. This option tells Git to clone only the latest commit, which is sufficient for building the package.

Moreover, Git usually doesn't print logs to stdout when run in a container, but these are very useful for debugging. We enable these using the `--progress --verbose` flags.

Therefore, a complete `git clone` command would look like this:

```bash
git clone --depth=1 --progress --verbose <repository_url>
```

As an example:

```bash
git clone --depth=1 --progress --verbose https://github.com/rtarun1/Livox-SDK2.git 
```


## Acknowledgements
This work is inspired by the work of [soham2560](https://github.com/soham2560/DockerForROS2Development).
