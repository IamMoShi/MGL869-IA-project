FROM node:22-slim

WORKDIR /backend

COPY package*.json ./
RUN npm install --production

COPY . .

CMD ["node", "server.js"]