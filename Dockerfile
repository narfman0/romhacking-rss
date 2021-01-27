FROM python:alpine

RUN pip install romhacking-rss

CMD ["romhacking_rss"]
