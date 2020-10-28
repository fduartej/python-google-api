FROM ubuntu:16.04

RUN apt-get update \
&& apt-get install -y python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip

# Copiamos solamente el requirements.txt primero para crear el Docker Cache
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD [ "app.py" ]