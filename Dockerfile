FROM python:slim

ENV TV_PATH=/tv \
    CONF=/config/tvclean.conf \
    LOG=/config/tvclean.log \
    EXCLUDE=.jpg,.db \
    CRON="0 0 * * *" \
    PUID=1000 \
    GUID=1000 \
    TZ=Europe/London

WORKDIR /app

COPY main.py requirements.txt .

RUN groupadd -g ${GUID} tvclean &&\
    useradd  -m -u ${PUID} -g tvclean tvclean &&\
    chown -R tvclean:tvclean /app &&\
    rm /etc/localtime &&\
    ln -s /usr/share/zoneinfo/${TZ} /etc/localtime

USER tvclean

RUN pip install -r requirements.txt &&\
    rm requirements.txt

CMD ["python3", "./main.py"]
