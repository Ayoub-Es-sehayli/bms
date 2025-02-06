FROM python:3.12.8-alpine

ARG VERSION
RUN apk add --update libpq-dev gcc

COPY dist/ /bms/

WORKDIR /bms

RUN pip install bms-$VERSION-py3-none-any.whl

RUN tar -xzf bms-$VERSION.tar.gz
RUN chown 1000:0 -R bms-$VERSION

USER 1000
WORKDIR /bms/bms-$VERSION

CMD ["fastapi", "run", "bms"]
