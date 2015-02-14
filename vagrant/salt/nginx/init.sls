nginx:
  pkg:
    - installed
  service:
    - running
    - watch:
      - pkg: nginx

/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx/nginx.conf
    - require:
      - pkg: nginx

/etc/nginx/sites-enabled:
  file.directory:
    - require:
      - pkg: nginx

/etc/nginx/sites-available:
  file.directory:
    - require:
      - pkg: nginx
