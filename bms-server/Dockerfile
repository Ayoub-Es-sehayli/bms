FROM python:3.12.9-alpine AS pre-build

WORKDIR /bms

RUN apk add --update libpq-dev gcc
RUN pip install pdm

COPY --chown=1000:0 . .

RUN pdm install --prod

FROM pre-build AS dev

CMD ["pdm", "run", "fastapi", "run", "--port", "80", "bms"]

FROM pre-build AS testing

RUN pdm install -dG test

USER 1000
COPY --chown=1000:0 pytest.ini pytest.ini

CMD ["pytest"]

FROM pre-build AS build

RUN pdm build

FROM python:3.12.9-alpine AS production

ARG VERSION
WORKDIR /bms
COPY --from=build /bms/dist /bms

RUN pip install bms-$VERSION-py3-none-any.whl
RUN tar -xzf bms-$VERSION.tar.gz
RUN chown 1000:0 -R bms-$VERSION

USER 1000
WORKDIR /bms/bms-$VERSION

CMD ["fastapi", "run", "--port", "80", "bms"]
