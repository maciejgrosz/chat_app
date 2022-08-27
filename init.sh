#!/bin/bash

docker rm -f chat_roomdb
docker rm -f chat_room
docker build . -t chat_room_image:1.0 -f room_app/Dockerfile
docker run -itd -p 8000:5000 --name chat_room chat_room_image:1.0
docker run -itd --name chat_roomdb -p 3306:3306 -e MYSQL_ROOT_PASSWORD=pass mysql:8.0.30
sleep 20
docker exec -it chat_roomdb mysql -u root -ppass -e "CREATE USER 'app'@'172.17.0.2' IDENTIFIED WITH mysql_native_password BY 'pass';"
docker exec -it chat_roomdb mysql -u root -ppass -e "CREATE DATABASE chat_db;"
docker exec -it chat_roomdb mysql -u root -ppass -e "GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'app'@'172.17.0.2' WITH GRANT OPTION;"
docker exec -it chat_roomdb mysql -u root -ppass -D chat_db -e "CREATE TABLE chat (ID int,username varchar(30),message varchar(255),date varchar(255));"
