# Epilepsy Intelligence Platform — Viewer image (build with Vite, serve with nginx)
FROM node:20-alpine AS build
WORKDIR /app
COPY viewer/package*.json ./
RUN npm ci
COPY viewer/ ./
# The docs are globbed at build time, so they must be present in the build context.
COPY docs /docs
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
