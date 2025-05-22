FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

SHELL ["/bin/bash", "-c"]

WORKDIR /home
ENV CROWDSURFER_WORKSPACE=/home/CrowdSurfer
ENV CROWDSURFER_PATH=${CROWDSURFER_WORKSPACE}/src/CrowdSurfer

# Install required packages and clean up
RUN apt-get update -y \
    && apt-get install -y git wget python3-pip \
    && pip install gdown \
    && rm -rf /var/lib/apt/lists/*

# Clone repositories
RUN git clone https://github.com/Smart-Wheelchair-RRC/CrowdSurfer.git $CROWDSURFER_PATH

# Setup Python environment for CrowdSurfer
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv venv --python 3.10 --system-site-packages ${CROWDSURFER_PATH}/.venv \
    && uv sync --active --project ${CROWDSURFER_PATH}

# Download checkpoints
RUN mkdir -p ${CROWDSURFER_PATH}/checkpoints \
    && gdown https://drive.google.com/drive/folders/1HSRrbuwwNk9_C1WKN9qnStjemFLukO8s --folder -O ${CROWDSURFER_PATH}/checkpoints

# Source environments in bashrc
RUN echo "source ${CROWDSURFER_PATH}/.venv/bin/activate" >> /root/.bashrc

CMD ["/bin/bash", "-c"]
