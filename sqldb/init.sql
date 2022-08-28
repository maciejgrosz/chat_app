CREATE USER 'app'@'172.27.0.2' IDENTIFIED WITH mysql_native_password BY 'pass';
CREATE DATABASE IF NOT EXISTS chat_db;
USE chat_db
CREATE TABLE IF NOT EXISTS chat (ID int, username varchar(30), message varchar(255), date varchar(255));
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'app'@'172.27.0.2' WITH GRANT OPTION;
