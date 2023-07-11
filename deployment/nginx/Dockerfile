FROM node:16-alpine as build-stage

# Set working directory
WORKDIR /app

# Copy frontend files
COPY ./frontend/package.json .
COPY ./frontend .

# required for reading the product version
COPY ./.git ./.git

RUN apk update && apk upgrade && apk add --no-cache bash git openssh

# install node modules and build assets
RUN yarn install && yarn build

FROM nginx:mainline-alpine as prod-stage

RUN rm /etc/nginx/conf.d/default.conf

COPY ./deployment/nginx/nginx-portal.conf /etc/nginx/templates/nginx.conf.template

# overwrite the nginx.conf, use only for the initial server setup
# COPY ./deployment/nginx/nginx-cert.conf /etc/nginx/templates/nginx.conf.template

COPY --from=build-stage ./frontend_assets /frontend_assets/

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
