FROM node:22 AS build

# Set working directory
WORKDIR /app

# Copy environment file for build-time usage
COPY .env .env

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Use Nginx to serve the built app
FROM nginx:alpine

# Copy built files to the default Nginx public folder
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
