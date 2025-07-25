FROM python:3.11-slim
ADD src/main.py .
RUN pip install paho-mqtt requests schedule
CMD [ "python", "-u", "./main.py" ]