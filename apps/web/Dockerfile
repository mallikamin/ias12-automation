FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source code
COPY . .

# Run dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
