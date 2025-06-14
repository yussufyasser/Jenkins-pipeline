FROM python:3.8-slim


RUN mkdir /home/app

COPY . /home/app/

WORKDIR /home/app

RUN apt-get update


RUN apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx


RUN pip install opencv-python

RUN pip install -r requirements.txt

RUN pip install ultralytics


EXPOSE 5052

CMD ["python", "english_service.py"]
