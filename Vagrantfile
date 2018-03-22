
$dependencies = <<SCRIPT
    # export DEBIAN_FRONTEND=noninteractive

    apt-get install -y update
    apt-get install -y postgresql postgresql-contrib postgis libpq-dev postgresql-server-dev-all
    apt-get install -y postgresql-9.5-postgis-2.2 postgresql-9.5-postgis-scripts postgresql-plpython-9.5
    apt-get install -y build-essential git python-dev python3-dev libjpeg-dev zlib1g-dev python-virtualenv binutils libproj-dev gdal-bin
    apt-get install -y memcached

    # Needed to install Fiona via pip
    apt-get install -y libgdal-dev

    # Needed by GDAL (django-spillway)
    # sudo add-apt-repository ppa:ubuntugis/ppa
    # sudo apt update
    # sudo apt upgrade # if you already have gdal 1.11 installed
    # sudo apt install gdal-bin python-gdal python3-gdal

    # Configure postgis
    sudo -u postgres createuser -d ubuntu
    sudo -u ubuntu createdb mapaguarani

    sudo -u postgres psql -d mapaguarani -c "CREATE EXTENSION postgis;"

SCRIPT

$virtualenv = <<SCRIPT

    # needed to install gdal
    # export CPLUS_INCLUDE_PATH=/usr/include/gdal
    # export C_INCLUDE_PATH=/usr/include/gdal
    # pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

    # Python env
    # must run with ubuntu user
    virtualenv -p /usr/bin/python3 mapaguarani-env
    source /home/ubuntu/mapaguarani-env/bin/activate

    /home/ubuntu/mapaguarani-env/bin/pip install -r /vagrant/requirements/local.txt

SCRIPT

$import_layers = <<SCRIPT
    # must run with ubuntu user

    cd /vagrant
    # migrations
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py migrate
    # load initial data
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py loaddata fixtures/initial_data.json

    git clone https://github.com/hacklabr/camadas-cti /home/ubuntu/camadas-cti
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_lands_layer /home/ubuntu/camadas-cti/terras_indigenas_final_importacao.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_village_layer /home/ubuntu/camadas-cti/camada-aldeias-importacao.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_archaeological_layer /home/ubuntu/camadas-cti/sitios.csv

    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_village_layer /home/ubuntu/camadas-cti/PYARGBOL/Argentina_aldeiasguarani1.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_village_layer /home/ubuntu/camadas-cti/PYARGBOL/BOL_aldeiasguarani.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_village_layer /home/ubuntu/camadas-cti/PYARGBOL/Paraguai_aldeiasguarani.shp

    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_village_layer /home/ubuntu/camadas-cti/timbira/Aldeia_Timbira2.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_village_layer /home/ubuntu/camadas-cti/javari/aldeias_javari_site.shp

    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_protected_areas_layer /home/ubuntu/camadas-cti/Unidades_conservacao.shp

    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_countries_layer /home/ubuntu/camadas-cti/limites/brasil.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_countries_layer /home/ubuntu/camadas-cti/limites/al/paises-al.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_countries_layer /home/ubuntu/camadas-cti/limites/al/departamientos-al.shp

    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_states_layer /home/ubuntu/camadas-cti/limites/estados_brasileiros.shp
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py import_cities_layer /home/ubuntu/camadas-cti/limites/municipios_brasil.shp

SCRIPT

$windshaft = <<SCRIPT

    apt-get install -y nodejs npm
    update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10
    apt-get install -y libmapnik2.2 redis-server node-node-redis
    apt-get install -y libcairo2-dev libpango1.0-dev libjpeg8-dev libgif-dev

SCRIPT

$maptiler = <<SCRIPT
    # Tiler dependencies (npm package node-mapinik - https://github.com/mapnik/node-mapnik#depends) for ubuntu < 16.04
    # TODO: remove this when update to 16.04 xenial
    # sudo add-apt-repository ppa:ubuntu-toolchain-r/test
    # sudo apt-get update -y
    # sudo apt-get install -y libstdc++-5-dev

    # must run with ubuntu user
    git clone https://github.com/hacklabr/mapaguarani-tiler.git
    cd mapaguarani-tiler
    npm install
    cp config.vagrant.js config.js

SCRIPT

$runserver = <<SCRIPT
    # must run with ubuntu user
    cd /vagrant
    /home/ubuntu/mapaguarani-env/bin/python3 manage.py migrate

    tmux -2 new-session -d -s ubuntu -n 'django'
    tmux send-keys "/home/ubuntu/mapaguarani-env/bin/python3 manage.py runserver_plus 0.0.0.0:8000" C-m

    # run the windshaft maptiles
    tmux new-window -t ubuntu:1 -n 'windshaft'
    tmux send-keys -t ubuntu:1 "node /home/ubuntu/mapaguarani-tiler/app.js" C-m

SCRIPT

Vagrant.configure('2') do |config|

    config.vm.box = 'ubuntu/xenial64'
    # config.vm.box = 'ubuntu/trusty64'
    # config.vm.box_url = "http://files.vagrantup.com/" + config.vm.box + ".box"

    config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
    end

    # config.ssh.forward_agent = true
    # config.ssh.username = "vagrant"
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 8000, guest: 8000
    config.vm.network :forwarded_port, host: 4000, guest: 4000

    config.vm.provision "shell", inline: $setup
    config.vm.provision "shell", inline: $dependencies
    config.vm.provision "shell", inline: $virtualenv, privileged: false
    # config.vm.provision "shell", inline: $import_layers, privileged: false
    config.vm.provision "shell", inline: $windshaft
    config.vm.provision "shell", inline: $maptiler, privileged: false
    config.vm.provision "shell",
            inline: $runserver,
            privileged: false,
            run: "always"
    # config.vm.synced_folder "../mapaguarani-tiler/", "/home/ubuntu/mapaguarani-tiler/", create: true
    # config.vm.synced_folder "../camadas-cti/", "/home/ubuntu/camadas-cti/", create: true
    # config.vm.synced_folder "../geodjango-boundaries/", "/home/ubuntu/geodjango-boundaries/", create: true
    # config.vm.synced_folder "../django-spillway/", "/home/ubuntu/django-spillway/", create: true
    # config.vm.synced_folder "../django-moderation/", "/home/ubuntu/django-moderation/", create: true
    # config.vm.synced_folder "../greenwich/", "/home/ubuntu/greenwich/", create: true

end
