FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod 644 /etc/nginx/nginx.conf

RUN mkdir -p /usr/share/nginx/html/static/media

COPY static /usr/share/nginx/html/static
RUN chmod -R 755 /usr/share/nginx/html/static
RUN chmod -R 755 /usr/share/nginx/html/static/media
