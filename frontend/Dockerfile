FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy all files first (including src/dataconnect-generated)
COPY . .

# Install dependencies
RUN pnpm install

EXPOSE 5173

CMD ["pnpm", "dev", "--host", "0.0.0.0"]