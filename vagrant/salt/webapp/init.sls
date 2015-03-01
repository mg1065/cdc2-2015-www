cdcwebapp.service:
  file.managed:
    - name: /etc/systemd/system/cdcwebapp.service
    - source: salt://webapp/cdcwebapp.service
  service:
    - name: cdcwebapp
    - running
    - require:
      - file: cdcwebapp.service
      - service: mysqld

webapp_nginx_av:
  file.managed:
    - name: /etc/nginx/sites-available/cdcwebapp.conf
    - source: salt://webapp/nginx.conf
    - require:
      - file: /etc/nginx/sites-available

webapp_nginx_en:
  file.symlink:
    - name: /etc/nginx/sites-enabled/cdcwebapp.conf
    - target: /etc/nginx/sites-available/cdcwebapp.conf
    - require:
      - file: webapp_nginx_av
      - pkg: nginx
    - watch_in:
      - service: nginx

django:
  pip.installed:
    - name: django >= 1.7
    - require:
      - pkg: python-pip

MySQL-python:
  pip.installed:
    - require:
      - pkg: python-pip
      - pkg: mariadb-devel
      - pkg: gcc
      - pkg: redhat-rpm-config

dj-database-url:
  pip.installed:
    - require:
      - pkg: python-pip

mariadb-devel:
  pkg.installed

cdc:
  mysql_database.present: []
  mysql_user:
    - present
    - name: root
    - password_hash: '*11EFE3D56FB6AE7A199B1C6096139BEF7A313EA1'
    - require:
      - service: mysqld
      - mysql_database: cdc
