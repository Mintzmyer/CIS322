-- Wipe table clean, create user tables
DROP TABLE if exists users;

-- serialized pk for continuity with username change 
-- max username and password length is 16 chars
-- roles referenced with foregin key to relational roles table
CREATE TABLE users ( user_pk serial PRIMARY KEY, username varchar(16), password varchar(16), role_fk integer);

-- Remove roles, create table anew
DROP TABLE if exists roles;

-- Relational table for users - Create roles required in spec
CREATE TABLE roles ( role_pk serial PRIMARY KEY, title varchar(18));
INSERT INTO roles (title) values ('Facilities Officer');
INSERT INTO roles (title) values ('Logistics Officer');

-- Remove/create assets table. Set 'arbitrary length' description to 50 chars
DROP TABLE if exists assets;
CREATE TABLE assets (asset_pk serial PRIMARY KEY, tag varchar(16), description varchar(50));

-- Remove/create facilities table
DROP TABLE if exists facilities;
CREATE TABLE facilities (facility_pk serial PRIMARY KEY, name varchar(32), code varchar(6));
INSERT INTO facilities (name, code) VALUES ('Disposed', 'Trash');

-- Remove/create asset_location table
DROP TABLE if exists asset_location;
-- Create relational table for assets and their location (facility)
CREATE TABLE asset_location (asset_fk integer, facility_fk integer, arrival date, departure date);

-- Remove/create transfer_request table
DROP TABLE if exists transfer_request;
-- Create table for transfer requests
-- Grouped data on larger request here
-- Mostly logical/beaurocratic process for overall 'Shipment Order'
CREATE TABLE transfer_request (request_pk serial PRIMARY KEY, requester_fk integer, date_requested date, approver_fk integer, date_approved date);

-- Remove/create asset_transfers table
DROP TABLE if exists asset_transfers;
-- Create relational table for assets in transfer requests
-- Grouped data for individual assets here
-- Entire request inventory may need to be shipped separately
CREATE TABLE asset_transfers (request_fk integer, asset_fk integer, source_fk integer, load date, destination_fk integer, unload date, scheduler_fk integer);
