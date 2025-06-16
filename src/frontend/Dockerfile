# build stage
FROM node:latest AS build-stage
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .

RUN npm run build

# production stage
FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]