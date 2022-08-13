FROM python:3.8


RUN mkdir -p /usr/src/
WORKDIR /usr/src/

COPY . /usr/src/

RUN pip install  -r requirements.txt
#--no-cashe-dir

EXPOSE 8080

CMD ["python", "get_reddit_subs.py"]