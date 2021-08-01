FROM python:3.9-alpine
WORKDIR /code/server
RUN apk add --no-cache --virtual .tmp gcc libwebp-dev jpeg-dev zlib-dev musl-dev linux-headers
COPY requirements.txt requirements.txt
COPY .env.prod .env.prod
COPY wsgi.py wsgi.py
# RUN python3 -m venv env
# RUN source env/bin/activate
# RUN set -a; source .env.prod; set +a
RUN pip install -r requirements.txt
RUN apk del .tmp
RUN apk add libjpeg libwebp
EXPOSE 5000
COPY ./project ./project
RUN rm ./project/config.yaml
COPY prod-config/config.yaml ./project/config.yaml
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:handler", "--workers=4"]