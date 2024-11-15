FROM python:3.12

LABEL maintainer='Alfred'

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get -y update && \
    apt-get -y install \
    vim \
    supervisor \
    nginx

ENV PYTHONUNBUFFERED 1

WORKDIR /fastft

COPY . /fastft

RUN /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

RUN cp /fastft/config/supervisord.conf /etc/supervisor/supervisord.conf
RUN cp /fastft/config/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
RUN cp /fastft/config/nginx.conf /etc/nginx/nginx.conf

#CMD ["sh", "-c", "[ -e /var/run/supervisor.sock ] && unlink /var/run/supervisor.sock; exec supervisord -n"]
#CMD ["sh", "-c", "[ supervisorctl start gunicorn"]
#CMD ["sh", "-c", "[ nignx"]