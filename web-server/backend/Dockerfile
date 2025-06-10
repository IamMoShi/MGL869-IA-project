FROM node:20

WORKDIR /backend

COPY package.json package-lock.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]