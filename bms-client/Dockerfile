FROM node:22-alpine AS pre-build

WORKDIR /bms/bms-client

COPY package.json .

RUN npm i

FROM pre-build AS dev

COPY . .
CMD npm run dev

FROM pre-build AS build

COPY . .
CMD npm run build

FROM node:22-alpine AS production

COPY --from=build /bms/bms-client/dist /bms/bms-client

RUN npm i -g serve

WORKDIR /bms/bms-client

CMD serve -p $CLIENT_PORT .
