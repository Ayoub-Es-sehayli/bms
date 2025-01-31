FROM python:3.12.8-alpine

COPY dist/ /bms/

WORKDIR /bms

ARG VERSION
RUN pip install bms-$VERSION-py3-none-any.whl

RUN tar -xzf bms-$VERSION.tar.gz
RUN chown 1000:0 -R bms-$VERSION

USER 1000
WORKDIR /bms/bms-$VERSION

CMD ["python", "-m", "bms"]
