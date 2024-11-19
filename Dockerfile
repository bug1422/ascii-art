FROM python:3.11.4-slim

WORKDIR /app

COPY requirement.txt /app/

RUN pip install --no-cache-dir -r requirement.txt

COPY . /app/

EXPOSE 80

ENV NAME=ascii-art-converter

LABEL maintainer="bug1422 <thaiphamwang@gmail.com>"

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]
