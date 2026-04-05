FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Default for local development
ENV VITE_API_URL=http://127.0.0.1:8080

CMD ["npm", "run", "dev"]
