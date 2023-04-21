FROM locustio/locust:2.15.1

WORKDIR /home/locust

ADD . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8089
EXPOSE 5557

ENTRYPOINT ["bash", "run.sh"]