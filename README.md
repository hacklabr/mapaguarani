# Mapa Guarany Yvyrupá

[![Join the chat at https://gitter.im/hacklabr/mapaguarani](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/hacklabr/mapaguarani?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Instalando Banco de Dados Posstgis

sudo apt-get install postgresql postgresql-contrib postgis postgresql-9.3-postgis-2.1 postgresql-9.3-postgis-2.1-scripts libpq-dev

sudo su - postgres

createuser mapaguarani
createdb -O mapaguarani template_postgis -E UTF-8
createlang plpgsql template_postgis
psql -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
psql -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql

psql
# aqui vai as querys executadas

createdb -T template_postgis mapaguarani

psql
# query para dar permissão para o banco mapaguarani ao usuário mapaguarani
# GRANT ALL PRIVILEGES ON DATABASE mapaguarani to mapaguarani;


## Dependências
sudo apt-get install build-essential git

git clone https://github.com/hacklabr/mapaguarani.git

sudo apt-get install python-virtualenv python3-dev

virtualenv -p /usr/bin/python3 mapaguarani-env
source mapaguarani-env/bin/activate
cd mapaguarani
pip install -r requirements/production.txt


## Geo pedendencies
sudo apt-get install binutils libproj-dev gdal-bin


Deloy

apt-get install nginx


apt-get install gunicorn