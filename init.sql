-- init.sql
-- Supprime l'utilisateur s'il existe déjà (facultatif)
DROP DATABASE IF EXISTS bright_db;
DROP USER IF EXISTS bright_user;

-- Création de l'utilisateur et de la base
CREATE USER bright_user WITH PASSWORD 'bright_pass';
CREATE DATABASE bright_db OWNER bright_user;
GRANT ALL PRIVILEGES ON DATABASE bright_db TO bright_user;