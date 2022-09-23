FROM --platform=${TARGETPLATFORM:-linux/amd64} openfaas/of-watchdog:0.7.7 as watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.7-slim-buster

WORKDIR /app
COPY requirements.txt   /app
COPY requestMediator.py /app
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
COPY abc.jpg           .

RUN chmod +x /usr/bin/fwatchdog && \
	chmod 777 /app/* && \
	pip install --user -r requirements.txt


ENV fprocess="python requestMediator.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
