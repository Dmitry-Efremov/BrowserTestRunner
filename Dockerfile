FROM python:2.7-alpine

RUN pip install requests retrying selenium futures
RUN apk add --no-cache vim

COPY ./lib/ /runner/lib
COPY ./vendors/selenium-server-standalone-2.47.1.jar /runner/vendors/selenium-server-standalone-2.47.1.jar
COPY ./selenium-tests-runner.py /runner/selenium-tests-runner.py

ARG GIT_STATUS
ARG GIT_COMMIT
ARG IMAGE_TAG

ENV GIT_STATUS $GIT_STATUS
ENV GIT_COMMIT $GIT_COMMIT
ENV IMAGE_TAG $IMAGE_TAG

ENTRYPOINT [ "python", "/runner/selenium-tests-runner.py" ]
