DROP DATABASE if exists lost;
CREATE DATABASE lost
	WITH OWNER osnapdev;
\connect lost
DROP TABLE if exists products;
CREATE TABLE products ( product_pk integer, vendor varchar(25), description varchar(50), alt_description varchar(50));
DROP TABLE if exists assets;
CREATE TABLE assets ( asset_pk integer, product_fk integer, asset_tag varchar(10), description varchar(50), alt_description varchar(50));






