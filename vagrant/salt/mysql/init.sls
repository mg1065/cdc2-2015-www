community-mysql-server:
  pkg.installed:
    - name: mariadb-server

mysqld:
  service.running:
    - require:
      - pkg: community-mysql-server
