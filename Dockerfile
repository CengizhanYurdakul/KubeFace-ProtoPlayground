FROM python:3.9 AS BASE

WORKDIR /code

# Copy repo with or without weights
WORKDIR /code
COPY . /code/

# Download necessary files
RUN wget https://folk.ntnu.no/haakohu/RetinaFace_mobilenet025.pth -P /root/.cache/torch/hub/checkpoints/

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get upgrade -y

# Install packages
RUN pip install --upgrade pip
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["python", "DetectionServer.py"]