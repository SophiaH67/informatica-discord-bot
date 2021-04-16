FROM python:rc-buster
WORKDIR /app
COPY requirements.txt ./
RUN [ "pip", "install", "--no-cache-dir" ,"-r", "requirements.txt"]
RUN [ "bash", "-c", "apt update -y && apt install -y libmecab-dev" ]
COPY . .
CMD [ "python", "main.py"]