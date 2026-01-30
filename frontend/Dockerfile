FROM node:20-alpine

WORKDIR /app

# Install only package.json first for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the files
COPY . .

EXPOSE 5173

# Entrypoint will check for new packages
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
