# Use a lightweight Nginx alpine image to serve static web client files
FROM nginx:alpine

# Copy all static html, css, and js files directly into Nginx's web root directory
COPY . /usr/share/nginx/html/

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose standard HTTP port 80
EXPOSE 80

ENTRYPOINT ["docker-entrypoint.sh"]