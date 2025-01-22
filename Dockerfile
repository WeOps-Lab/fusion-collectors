FROM ubuntu:22.04

RUN mkdir -p /fusion-collector
RUN mkdir -p /fusion-collector/cache
RUN mkdir -p /fusion-collector/log
RUN mkdir -p /fusion-collector/generated
RUN mkdir -p /fusion-collector/bin

WORKDIR /fusion-collector/bin/
ADD ./telegraf .

WORKDIR /fusion-collector
ADD ./sidecar_template.yml .

ADD entrypoint.sh .
RUN chmod -Rf 777 ./entrypoint.sh
RUN chmod -Rf 777 /fusion-collector
ENTRYPOINT ["/fusion-collector/entrypoint.sh"]

CMD ["/fusion-collector/bin/collector-sidecar", "-c", "/fusion-collector/sidecar.yml"]