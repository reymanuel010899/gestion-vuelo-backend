# Gestion Vuelo Backend

Este es el backend del proyecto **Gestion Vuelo**.  

---

## 🔹 Clonar y ejecutar el proyecto (SQLite por defecto)

```bash
# Clonar repositorio
git clone https://github.com/reymanuel010899/gestion-vuelo-backend.git
cd gestion-vuelo-backend

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones y aplicarlas
python3 manage.py makemigrations
python3 manage.py migrate

# Ejecutar servidor
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