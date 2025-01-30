FROM python:3.12.8-alpine

COPY dist/ /bms/

WORKDIR /bms

ARG VERSION
RUN pip install bms-$VERSION-py3-none-any.whl
RUN tar -xzf bms-$VERSION.tar.gz

WORKDIR /bms/bms-$VERSION

CMD ["python", "-m", "bms"]
