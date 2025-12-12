FROM nginx:alpine

COPY ./ /usr/share/nginx/html

EXPOSE 80

# Mantiene Nginx corriendo en primer plano
CMD ["nginx", "-g", "daemon off;"]
