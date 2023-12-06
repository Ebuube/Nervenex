-- Reset a MySQL server for the development of the project
-- Usage: cat 'setup_mysql_dev' | sudo mysql;
DROP DATABASE IF EXISTS nervenex_dev_db;
CREATE DATABASE IF NOT EXISTS nervenex_dev_db;
CREATE USER IF NOT EXISTS 'nervenex_dev'@'localhost' IDENTIFIED BY 'nervenex_dev_pwd';

GRANT ALL PRIVILEGES ON nervenex_dev_db.* TO 'nervenex_dev'@'localhost' WITH GRANT OPTION;
GRANT SELECT ON performance_schema.* TO 'nervenex_dev'@'localhost';
