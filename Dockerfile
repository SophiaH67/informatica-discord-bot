FROM python:rc-buster
WORKDIR /app
COPY requirements.txt ./
RUN [ "pip", "install", "--no-cache-dir" ,"-r", "requirements.txt"]
RUN ["apt-get", "update", "-y"]
RUN ["apt-get", "install", "-y", "git"]
COPY . .
CMD [ "python", "main.py"]