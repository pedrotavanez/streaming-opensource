FROM nginx:latest

RUN mkdir -p /opt/stream_cache/
COPY nginx.conf /etc/nginx/.
COPY headers.js /etc/nginx/.
COPY http.js /etc/nginx/.
CMD ["nginx", "-g", "daemon off;"]