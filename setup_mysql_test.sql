-- Reset a MySQL server for the development of the project
-- Usage: cat 'setup_mysql_test' | sudo mysql;
DROP DATABASE IF EXISTS nervenex_test_db;
CREATE DATABASE IF NOT EXISTS nervenex_test_db;
CREATE USER IF NOT EXISTS 'nervenex_test'@'localhost' IDENTIFIED BY 'nervenex_test_pwd';

GRANT ALL PRIVILEGES ON nervenex_test_db.* TO 'nervenex_test'@'localhost' WITH GRANT OPTION;
GRANT SELECT ON performance_schema.* TO 'nervenex_test'@'localhost';
