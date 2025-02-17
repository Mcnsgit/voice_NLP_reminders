-- Create application user and database
CREATE USER taskmanager WITH PASSWORD 'taskmanager' CREATEDB;
CREATE DATABASE taskmanager_db WITH OWNER taskmanager;
GRANT ALL PRIVILEGES ON DATABASE taskmanager_db TO taskmanager;
\c taskmanager_db
GRANT ALL ON SCHEMA public TO taskmanager;