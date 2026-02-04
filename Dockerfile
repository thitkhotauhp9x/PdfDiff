FROM python:3.13-alpine
LABEL authors="manhdt"

RUN apk add --no-cache imagemagick ghostscript

COPY ./dist ./dist
RUN pip install ./dist/pdfdiff-0.1.0-py3-none-any.whl  --break-system-packages
RUN rm -rf ./dist
CMD ["python3"]
