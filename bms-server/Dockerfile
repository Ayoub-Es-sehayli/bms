FROM python:3.12.9-alpine AS build

RUN apk add --update libpq-dev gcc
RUN pip install pdm

COPY . /bms
WORKDIR /bms

RUN pdm build

FROM python:3.12.9-alpine AS application

ARG VERSION
WORKDIR /bms
COPY --from=build /bms/dist /bms

RUN pip install bms-$VERSION-py3-none-any.whl
RUN tar -xzf bms-$VERSION.tar.gz
RUN chown 1000:0 -R bms-$VERSION

USER 1000
WORKDIR /bms/bms-$VERSION

CMD ["fastapi", "run", "--port", "8080", "bms"]

FROM application AS test-build

USER 0
RUN pip install pytest

USER 1000
COPY --chown=1000:0 pytest.ini pytest.ini

CMD ["pytest"]
