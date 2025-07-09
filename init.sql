-- init.sql

CREATE USER bright_user WITH PASSWORD 'bright_pass';
CREATE DATABASE bright_db OWNER bright_user;
GRANT ALL PRIVILEGES ON DATABASE bright_db TO bright_user;

\echo '✔ init.sql exécuté avec succès'
