# Understanding the CI/CD workflows

> [!NOTE]
> At the moment, this workflow does not build for the ARM architecture. Please build these locally until Microsoft releases the feature for private repositories. [source one](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for-public-repositories), [source two](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#standard-github-hosted-runners-for--private-repositories). For now, Jetson builds done online will simply be skipped.

## Desired behaviour
1.  The user creates a new branch for their changes.
1.  The user commits their changes to the branch, with a relevant tag.
1.  The user pushes the branch to the remote repository.
1.  The CI/CD system detects the new tag and starts building the image.
1.  If the build is successful, the image is pushed to the GitHub Container Registry.
1.  The user can then pull the image from the registry and use it.

### Key features
-   Dependant images are built in the correct order.
-   Images are built with the correct tags.
-   The CI/CD system is triggered by tags, not pushes to branches or pull requests.
-   Upon any failure, the system will exit gracefully and not proceed with downstream dependant builds.

## Overview of the main workflow
This is a high-level understanding of the workflow described in [build.yaml](/.github/workflows/build.yaml).

1.  The workflow is triggered when a tag starting with `v` is pushed to the repository.

1.  Firstly, the workflow checks out the code from the repository and looks for changes. At a time, a change may be present in a full directory only. We do not test for individual Dockerfiles because certain images depend on others, and we want to build them in the correct order.

    Places tested for changes:
    -   `ROS2/AMD64x86/`: desktop images for AMD64x86 architecture
    -   `ROS2/Jetson`: edge-computing images for NVIDIA Jetson architecture (once implemented)
    -   `.github/workflows/`: GitHub Actions workflows

1.  Next, the workflow looks for the Git tag. If it finds a tag that starts with `v`, records this to a variable, so that it may be used later in the workflow.

1.  If changes were detected, the workflow proceeds to build the images. If any GitHub Action changes were detected, everything is rebuilt; otherwise only the changed images are rebuilt.

1.  The remainder of the build is split into five sections, which run in three steps (some run in parallel):

    | Step | Sections |
    | --- | --- |
    | 1 | - ROS2 base humble images (AMD64/x86) <br> - ROS2 base humble images (Jetson/ARM) |
    | 2 | - ROS2 humble_harmonic (AMD64/x86) |
    | 3 | - ROS2 wheelchair2_base images (AMD64/x86) <br> - ROS2 wheelchair2_base_jetson (depends on humble_jetson) |

    By default, all of these sections are configured as [matrix strategies](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow). Although some sections have only one entry, this allows for easy expansion in the future.

## Overview of the reusable workflow
It quickly became evident that several steps in the workflow were repetitive, so the majority of the actual work was refactored into a [reusable workflow](https://docs.github.com/en/actions/sharing-automations/reusing-workflows). This is described in [build-workflow.yaml](/.github/workflows/build-workflow.yaml), and is briefly explained below.

This workflow is triggered by the main workflow, and receives the following inputs:

| Input | Description | Default |
| --- | --- | --- |
| `build_context` | The build context for the Dockerfile | - |
| `image_name` | The target name of the image to build | - |
| `image_version` | The version tag of the image to build | - |
| `runs_on` | The GitHub runner to use for the build | `ubuntu-latest` |

First, code is checked out, [buildx is setup](https://github.com/docker/setup-buildx-action/tree/v3/), and [GHCR is authenticated](https://github.com/docker/setup-buildx-action/tree/v3/).

Finally, the actual image is built and (if successful) pushed to the GitHub Container Registry, using the [`docker/build-push-action`](https://github.com/docker/build-push-action/tree/v6/) action.


## Deeper dive into the main workflow
Here, we discuss only the potentially confusing parts of the main workflow, which is described in [build.yaml](/.github/workflows/build.yaml).

You are encouraged to read the [GitHub Actions documentation](https://docs.github.com/en/actions) for more information on how GitHub Actions work, how to write workflows, and reference for syntax. If you use VS Code to write workflows, the [GitHub Actions extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-github-actions) is useful.

### Checking for changes
We use the [`dorny/paths-filter`](https://github.com/dorny/paths-filter/tree/v2/) action to check for changes in the repository. This action allows us to specify paths to check for changes, and it will return a boolean value indicating whether any changes were detected.

These are stored as outputs of the `changes` job:

```yaml
outputs:
  ros2-amd64: ${{ steps.filter.outputs.ros2-amd64 }}
  ros2-jetson: ${{ steps.filter.outputs.ros2-jetson }}
  workflow: ${{ steps.filter.outputs.workflow }}
  image_version: ${{ steps.set_version.outputs.image_version }}
```

As described earlier, we check for changes in the three main directories:

```yaml
- name: Check for changes
  id: filter
  uses: dorny/paths-filter@v2
  with:
    filters: |
      ros2-amd64:
        - 'ROS2/AMD64x86/**'
      ros2-jetson:
        - 'ROS2/Jetson/**'
      workflow:
        - '.github/workflows/**'
```

### Setting the image version
This simply involves obtaining the Git tag and setting it as an environment variable for later use:

```yaml
- name: Set image version
  id: set_version
  run: |
    if [[ "${{ github.ref }}" == refs/tags/v* ]]; then
      echo "image_version=${{ github.ref_name }}" >> $GITHUB_OUTPUT
    fi
```

### Building the images
While there are several sections as described earlier, we shall dive deeper into one of these as exposition. Consider the "Stage 3: ROS2 wheelchair2_base images (AMD64/x86)" section.

```yaml
# Stage 3: ROS2 wheelchair2_base images (AMD64/x86)
ros2-wheelchair-base:
  needs: [changes, ros2-humble-base-amd64, ros2-humble-harmonic]
  if: ${{ needs.changes.outputs.ros2-amd64 == 'true' || needs.changes.outputs.workflow == 'true' }}
  name: ROS2 Wheelchair2 Base Images
  permissions:
    packages: write
    contents: read
  strategy:
    matrix:
      config:
        - { build_context: './ROS2/AMD64x86/wheelchair2_base', image_name: 'wheelchair2_base', image_version: "${{ needs.changes.outputs.image_version }}" }
        - { build_context: './ROS2/AMD64x86/wheelchair2_base_gazebo', image_name: 'wheelchair2_base_gazebo', image_version: "${{ needs.changes.outputs.image_version }}" }
  uses: ./.github/workflows/build-workflow.yaml
  with:
    build_context: ${{ matrix.config.build_context }}
    image_name: ${{ matrix.config.image_name }}
    image_version: ${{ matrix.config.image_version }}
    runs_on: ubuntu-latest
```

Let's break this down:
-   `needs`: This job depends on the `changes` job and the `ros2-humble-base-amd64` and `ros2-humble-harmonic` jobs. It will only run if these jobs are successful. This ensures that dependant images are built in the correct order.
-   `if`: This condition checks if there are changes in the `ROS2/AMD64x86/` directory or if there are changes in the workflows. If either condition is true, this job will run.
-   `permissions`: This job requires write access to packages (to push the built images) and read access to contents (to read the repository).
-   `strategy`: This defines a matrix strategy for the job. In this case, we have two configurations:
    -   `wheelchair2_base`: The base image for the wheelchair2 project.
    -   `wheelchair2_base_gazebo`: The base image for the wheelchair2 project with Gazebo support.
-   `uses`: This specifies that the job will use the reusable workflow defined in [build-workflow.yaml](/.github/workflows/build-workflow.yaml).
-   `with`: This passes the necessary parameters to the reusable workflow, including the build context, image name, image version, and the runner to use.

Note the matrix system:
```yaml
strategy:
  matrix:
    config:
      - { build_context: './ROS2/AMD64x86/wheelchair2_base', image_name: 'wheelchair2_base', image_version: "${{ needs.changes.outputs.image_version }}" }
      - { build_context: './ROS2/AMD64x86/wheelchair2_base_gazebo', image_name: 'wheelchair2_base_gazebo', image_version: "${{ needs.changes.outputs.image_version }}" }
```

In this system, we specify one or more configurations for the job. Each configuration corresponds to one resulting image. The reusable workflow will be run for each configuration, allowing us to build multiple images in parallel by just adding one more entry to the `config` list.

Please consult the [GitHub Actions documentation](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow) for more information on matrix strategies and syntax.