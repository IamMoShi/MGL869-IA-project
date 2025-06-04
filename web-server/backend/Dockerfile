FROM node:22-slim

WORKDIR /app

COPY package*.json ./

RUN apt update && apt install -y curl && npm install

COPY . .

CMD ["node", "server.js"]