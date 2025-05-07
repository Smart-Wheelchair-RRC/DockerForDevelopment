FROM cuda_ros_docker

SHELL ["/bin/bash", "-c"]

WORKDIR /home

RUN apt-get update -y

RUN apt-get install git -y
RUN pip install gdown

RUN mkdir -p CrowdSurfer_ws/src

RUN git clone https://github.com/Smart-Wheelchair-RRC/CrowdSurfer_wheelchair_livox.git CrowdSurfer_ws/src/CrowdSurfer

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \ 
    uv venv --python 3.10 --system-site-packages CrowdSurfer_ws/src/CrowdSurfer/src/CrowdSurfer/.venv \
    && uv sync --active --project CrowdSurfer_ws/src/CrowdSurfer/src/CrowdSurfer

RUN echo "source /home/CrowdSurfer_ws/src/CrowdSurfer/src/CrowdSurfer/.venv/bin/activate" >> ~/.bashrc

RUN mkdir CrowdSurfer_ws/src/CrowdSurfer/src/CrowdSurfer/checkpoints
RUN gdown https://drive.google.com/drive/folders/1HSRrbuwwNk9_C1WKN9qnStjemFLukO8s --folder -O CrowdSurfer_ws/src/CrowdSurfer/src/CrowdSurfer/checkpoints

RUN rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["/bin/bash", "-c"]
