FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Default for local development
ENV VITE_API_URL=http://localhost:8000

CMD ["npm", "run", "dev"]
