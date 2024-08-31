# Use the official Node.js image as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

COPY . .

# Install the dependencies
RUN npm install

# Run the application in development mode
CMD ["npm", "run", "dev"]
