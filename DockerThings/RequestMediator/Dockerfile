FROM --platform=${TARGETPLATFORM:-linux/amd64} openfaas/of-watchdog:0.7.7 as watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.7-slim-buster

WORKDIR /home/app/
COPY requirements.txt   .
COPY index.py .
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
COPY abc.jpg           .

RUN chmod +x /usr/bin/fwatchdog && \
	chmod 777 /home/app/* && \
	pip install --user -r requirements.txt


ENV fprocess="python index.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
