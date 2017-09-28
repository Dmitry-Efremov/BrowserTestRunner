FROM python:2.7-alpine

RUN pip install requests retrying selenium

COPY ./lib/ /runner/lib
COPY ./vendors/selenium-server-standalone-2.47.1.jar /runner/vendors/selenium-server-standalone-2.47.1.jar
COPY ./selenium-tests-runner.py /runner/selenium-tests-runner.py

ENTRYPOINT [ "python", "/runner/selenium-tests-runner.py" ]
