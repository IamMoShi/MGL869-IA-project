FROM node:22-alpine3.20 as web-app

WORKDIR /web-server

COPY package*.json ./
RUN npm install --production

COPY app/ app/
COPY .env ./

CMD ["npm", "start"]
