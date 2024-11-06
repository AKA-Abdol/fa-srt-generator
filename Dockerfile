FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt upgrade
RUN apt install -y ffmpeg

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80"]