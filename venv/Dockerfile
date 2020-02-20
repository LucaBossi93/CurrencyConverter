FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip setuptools
EXPOSE 5000
CMD python ./converter.py
