FROM nginx:alpine

# Copy static frontend files
COPY index.html /usr/share/nginx/html/index.html

# Custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
