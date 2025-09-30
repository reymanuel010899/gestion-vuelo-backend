##### gestion-vuelo-backend #####
----- clonar repositorio -----
cd gestion-vuelo-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sqlite3 db.sqlite3 < data.sql
python3 manage.py runserver 



##### crear la base de datos en postgres pero no temdra data ########

sudo -i -u postgres
psql
CREATE DATABASE gestion_vuelo;
CREATE USER gestion_vuelo_user;
\c gestion_vuelo;
ALTER ROLE gestion_vuelo_user WITH PASSWORD 'reymanuel010899';
GRANT ALL PRIVILEGES ON DATABASE gestion_vuelo TO gestion_vuelo_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO gestion_vuelo_user;
exit
exit
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver