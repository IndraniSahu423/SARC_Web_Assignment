FROM node:20-alpine AS build

WORKDIR /app

ARG VITE_AUTH_URL=http://localhost:8002
ARG VITE_PORTAL_URL=http://localhost:8001
ENV VITE_AUTH_URL=${VITE_AUTH_URL}
ENV VITE_PORTAL_URL=${VITE_PORTAL_URL}

COPY package.json /app/
COPY package-lock.json /app/
RUN npm ci

COPY . /app/
RUN chmod +x ./node_modules/.bin/vite || true
RUN node ./node_modules/vite/bin/vite.js build

FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
