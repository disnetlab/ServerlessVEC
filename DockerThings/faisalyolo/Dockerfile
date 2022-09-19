FROM --platform=${TARGETPLATFORM:-linux/amd64} openfaas/of-watchdog:0.7.7 as watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.7-slim-buster

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)

# RUN apk --no-cache add openssl-dev ${ADDITIONAL_PACKAGE}
# RUN apt install -y openssl-dev ${ADDITIONAL_PACKAGE}
RUN apt-get install openssl ${ADDITIONAL_PACKAGE}

# Uncomment if you want to use native modules
#RUN apt-get -qy update && apt-get -qy install gcc make

# Add non root user
# RUN addgroup -S app && adduser app -S -G app
RUN addgroup --system app && adduser app --system --ingroup app
RUN chown app /home/app

#USER app
ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .
COPY yolov3-tiny.txt     .
COPY yolov3-tiny.cfg     .
COPY yolov3-tiny.weights .

USER root
RUN pip install -r requirements.txt

RUN apt-get -qy update
# https://askubuntu.com/questions/1339558/cant-build-dockerfile-for-arm64-due-to-libc-bin-segmentation-fault
RUN apt install -y libc-bin
RUN apt install -y libgl1 libglib2.0-0 libsm6 libxrender1 libxext6
RUN apt install -y net-tools iputils-ping curl ethtool iputils-ping iproute2
RUN chmod 777 -R /tmp
COPY abc.jpg           .
COPY coldStart.sh .
RUN chmod 777 coldStart.sh

RUN chown -R app:app *

# Build the function directory and install any user-specified components
#USER app

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt	.
RUN pip install --user -r requirements.txt

#install function code
#USER root

COPY function/   .
#RUN chown -R app:app ../

# ARG TEST_COMMAND=tox
# ARG TEST_ENABLED=false
# RUN if [ "$TEST_ENABLED" == "false" ]; then \
#     echo "skipping tests";\
#     else \
#     eval "$TEST_COMMAND"; \
#     fi

WORKDIR /home/app/

#configure WSGI server and healthcheck
#USER root

ENV fprocess="python index.py"
#ENV fprocess="python -m http.server --bind 0.0.0.0 80"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
