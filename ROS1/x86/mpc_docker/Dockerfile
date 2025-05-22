FROM noetic_gpu

RUN apt-get update -y

WORKDIR /home

RUN apt-get update && apt-get install -y python3-pip git
RUN pip3 install casadi numpy matplotlib
RUN git clone https://github.com/Smart-Wheelchair-RRC/casadi-mpc.git /tmp/casadi-mpc
CMD ["bash"]

# Set the working directory in the container
#WORKDIR /app

# Copy the environment file into the container
#COPY mpc_environment.yaml /app/mpc_environment.yaml

# Create the conda environment using the provided YAML file
#RUN conda env create -f mpc_environment.yaml && conda clean -afy

# Use the new environment for subsequent commands
#SHELL ["conda", "run", "-n", "mpc", "/bin/bash", "-c"]

# Copy the rest of the application code into the container
#COPY . /app

# Set default command (adjust according to your application entry point)
#CMD ["python", "mpc/agent.py"]
