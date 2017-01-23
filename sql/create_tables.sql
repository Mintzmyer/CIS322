DROP DATABASE if exists lost;
CREATE DATABASE lost
	WITH OWNER osnapdev;
\connect lost
DROP TABLE if exists products;
CREATE TABLE products ( product_pk serial PRIMARY KEY, vendor varchar(25), description varchar(50), alt_description varchar(50));

DROP TABLE if exists assets;
CREATE TABLE assets ( asset_pk serial PRIMARY KEY, product_fk integer, asset_tag varchar(10), description varchar(50), alt_description varchar(50));

DROP TABLE if exists vehicles;
CREATE TABLE vehicles ( vehicles_pk serial PRIMARY KEY, asset_fk integer);

DROP TABLE if exists facilities;
CREATE TABLE facilities ( facilities_pk serial PRIMARY KEY, facility_fk integer, fcode varchar(10), common_name varchar(25), location varchar(25));
	
DROP TABLE if exists asset_at;
CREATE TABLE asset_at ( asset_fk integer, facility_fk integer, arrive_dt timestamp, depart_dt timestamp);

DROP TABLE if exists convoys;
CREATE TABLE convoys ( convoy_pk serial PRIMARY KEY, request varchar(10), source_fk integer, dest_fk integer, depart_dt timestamp, arrive_dt timestamp);

DROP TABLE if exists used_by;
CREATE TABLE used_by ( vehicle_fk integer, convoy_fk integer);

DROP TABLE if exists asset_on;
CREATE TABLE asset_on ( asset_fk integer, convoy_fk integer, load_dt timestamp, unload_dt timestamp);

DROP TABLE if exists users;
CREATE TABLE users ( user_pk serial PRIMARY KEY, username varchar(25), active boolean);

DROP TABLE if exists roles;
CREATE TABLE roles ( role_pk serial PRIMARY KEY, title varchar(25));

DROP TABLE if exists user_is;
CREATE TABLE user_is ( user_fk integer, role_fk integer);

DROP TABLE if exists user_supports;
CREATE TABLE user_supports ( user_fk integer, facility_fk integer);

DROP TABLE if exists levels;
CREATE TABLE levels ( level_pk serial PRIMARY KEY, abbrv varchar(10), comments varchar(25));

DROP TABLE if exists compartments;
CREATE TABLE compartments ( compartment_pk serial PRIMARY KEY, abbrv varchar(10), comments varchar(25));

DROP TABLE if exists security_tags;
CREATE TABLE security_tags ( tag_pk serial PRIMARY KEY, level_fk integer, compartment_fk integer, user_fk integer, product_fk integer, asset_fk integer);

