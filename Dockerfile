FROM python:3.12

LABEL maintainer='Alfred'

RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security/ bullseye-security main contrib non-free" >> /etc/apt/sources.list


RUN apt-get -y update && \
    apt-get -y install \
    vim \
    supervisor \
    nginx

ENV PYTHONUNBUFFERED 1

WORKDIR /fastft

COPY . /fastft

RUN mkdir /upload

RUN /usr/local/bin/python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN cp /fastft/config/supervisord.conf /etc/supervisor/supervisord.conf
RUN cp /fastft/config/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
RUN cp /fastft/config/nginx.conf /etc/nginx/nginx.conf

#CMD ["sh", "-c", "[ -e /var/run/supervisor.sock ] && unlink /var/run/supervisor.sock; exec supervisord -n"]
#CMD ["sh", "-c", "[ supervisorctl start gunicorn"]
#CMD ["sh", "-c", "[ nignx"]