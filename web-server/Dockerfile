FROM node:22-alpine3.20

WORKDIR /web-server

COPY package*.json ./
RUN npm install --production

COPY backend/ ./backend/
COPY .env ./

CMD ["node", "backend/server.js"]
