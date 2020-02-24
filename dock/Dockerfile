FROM node:10

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY . ./

RUN npm install

# Running the application
EXPOSE 5000
CMD [ "node", "app.js" ]
