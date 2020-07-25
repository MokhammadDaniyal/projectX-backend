FROM node:12.18-alpine
RUN mkdir -p /usr/src/app
RUN apk update
RUN apk add python3 py3-pip && pip3 install requests && pip3 install beautifulsoup4 && pip3 install simplejson && pip3 install scraperapi-sdk
ENV NODE_ENV development
WORKDIR /usr/src/app
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install && mv node_modules ../
COPY . .
EXPOSE 3000
CMD npm start