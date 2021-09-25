# build environment
FROM node as build

WORKDIR /app

COPY package.json /app/package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install


COPY public /app/public
COPY src /app/src

RUN npm run build

# production environment
FROM nginx:latest
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

CMD ["nginx", "-g", "daemon off;"]