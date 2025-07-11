# Stage 1: Build React app
FROM node:18-alpine AS react-build

WORKDIR /app

# Copy package files first for better caching
COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci

COPY frontend/ .

RUN npm run build

# Stage 2: Serve React build (using lightweight nginx)
FROM nginx:alpine AS react-prod

# Remove default nginx content and copy build output
RUN rm -rf /usr/share/nginx/html/*

COPY --from=react-build /app/build /usr/share/nginx/html

# Copy custom nginx config if needed
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
