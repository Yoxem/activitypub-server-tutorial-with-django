# activitypub-server-tutorial-with-django
Activitypub server tutorial demo with Django in Python

modified from https://github.com/timmot/activity-pub-tutorial, and read it
to know how it works similarly.

(C) 2022 Timothy and Yoxem, under MIT License.


Server config files in Nginx:

```

server {
server_name orig.social;


    location / {
            proxy_pass http://127.0.0.1:8080;
        }

    listen 443 ssl; # managed by Certbot
    ssl_certificate [fullchain.pem]; # managed by Certbot
    ssl_certificate_key [privkey.pem]; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = orig.social) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


listen 80;
server_name orig.social;
return 404; # managed by Certbot

```
