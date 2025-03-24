# Use an official Node.js runtime as the base image
FROM node:22.14.0 as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Define the build argument to pass environment variables during build time
ARG VITE_API_URL

# Make the ARG available as an ENV variable
ENV VITE_API_URL=${VITE_API_URL}

# Build the Vue.js app
RUN npm run build

# Use a lightweight Nginx image to serve the built app
FROM nginx:alpine

# Copy the built app from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]