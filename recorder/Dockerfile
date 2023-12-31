FROM python:3.11

WORKDIR /usr/app/src

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src src
ENTRYPOINT ["python", "-u", "src/main.py"]
