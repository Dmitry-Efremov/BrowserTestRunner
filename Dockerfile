FROM python:2.7-alpine

RUN apk add --no-cache vim build-base libffi-dev openssl-dev
RUN pip install requests retrying selenium futures azure-storage-blob

COPY ./lib/ /runner/lib
ADD https://s3.amazonaws.com/migration_platform/selenium/selenium-server-standalone-3.141.5.jar /runner/vendors/selenium-server-standalone-3.141.5.jar
COPY ./selenium-tests-runner.py /runner/selenium-tests-runner.py

ARG GIT_STATUS
ARG GIT_COMMIT
ARG IMAGE_TAG

ENV GIT_STATUS $GIT_STATUS
ENV GIT_COMMIT $GIT_COMMIT
ENV IMAGE_TAG $IMAGE_TAG

ENTRYPOINT [ "python", "/runner/selenium-tests-runner.py" ]
