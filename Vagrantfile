$setup = <<SCRIPT
    sed -i '1i deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main restricted universe multiverse' /etc/apt/sources.list
    DEBIAN_FRONTEND=noninteractive apt-get update
SCRIPT

$dependencies = <<SCRIPT
    export DEBIAN_FRONTEND=noninteractive
    apt-get install -y postgresql postgresql-contrib postgis postgresql-9.3-postgis-2.1 postgresql-9.3-postgis-2.1-scripts libpq-dev
    apt-get install -y postgresql-server-dev-all plpython-9.3
    apt-get install -y build-essential git python-dev python3-dev libjpeg-dev zlib1g-dev python-virtualenv binutils libproj-dev gdal-bin
    apt-get install -y memcached

    # Needed to install Fiona via pip
    apt-get install -y libgdal-dev

    # install pg_schema_triggers
    git clone https://github.com/CartoDB/pg_schema_triggers.git
    cd pg_schema_triggers/
    make
    make install
    cd ..

    git clone https://github.com/CartoDB/cartodb-postgresql.git
    cd cartodb-postgresql
    make all install
    cd ..


    # Configure postgis
    sudo -u postgres createuser -d vagrant
    sudo -u vagrant createdb mapaguarani

    sudo -u postgres psql -d mapaguarani -c "CREATE EXTENSION postgis;"
    sudo -u postgres psql -d mapaguarani -c "CREATE EXTENSION schema_triggers;"
    sudo -u postgres psql -d mapaguarani -c "CREATE EXTENSION plpythonu;"
    sudo -u postgres psql -d mapaguarani -c "CREATE EXTENSION cartodb;"

SCRIPT

$virtualenv = <<SCRIPT

    # Python env
    # must run with vagrant user
    virtualenv -p /usr/bin/python3 mapaguarani-env
    source /home/vagrant/mapaguarani-env/bin/activate
    /home/vagrant/mapaguarani-env/bin/pip install -r /vagrant/requirements/local.txt

SCRIPT

$import_layers = <<SCRIPT
    # must run with vagrant user

    cd /vagrant
    # migrations
    /home/vagrant/mapaguarani-env/bin/python3 manage.py migrate
    # load initial data
    /home/vagrant/mapaguarani-env/bin/python3 manage.py loaddata fixtures/initial_data.json

    git clone https://github.com/hacklabr/camadas-cti /home/vagrant/camadas-cti
    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_lands_layer /home/vagrant/camadas-cti/terras_indigenas_final_importacao.shp
    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_village_layer /home/vagrant/camadas-cti/camada-aldeias-importacao.shp
    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_archaeological_layer /home/vagrant/camadas-cti/sitios.csv

    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_protected_areas_layer /home/vagrant/camadas-cti/Unidades_conservacao.shp

    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_countries_layer /home/vagrant/camadas-cti/limites/brasil.shp
    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_states_layer /home/vagrant/camadas-cti/limites/estados_brasileiros.shp
    /home/vagrant/mapaguarani-env/bin/python3 manage.py import_cities_layer /home/vagrant/camadas-cti/limites/municipios_brasil.shp

SCRIPT

$windshaft = <<SCRIPT

    apt-get install -y nodejs npm
    update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10
    apt-get install -y libmapnik2.2 redis-server node-node-redis
    apt-get install -y libcairo2-dev libpango1.0-dev libjpeg8-dev libgif-dev

SCRIPT

$maptiler = <<SCRIPT
    # must run with vagrant user
    git clone https://github.com/hacklabr/mapaguarani-tiler.git
    cd mapaguarani-tiler
    npm install
    cp config.vagrant.js config.js

SCRIPT

$runserver = <<SCRIPT
    # must run with vagrant user
    cd /vagrant
    /home/vagrant/mapaguarani-env/bin/python3 manage.py migrate

    tmux -2 new-session -d -s vagrant -n 'django'
    tmux send-keys "/home/vagrant/mapaguarani-env/bin/python3 manage.py runserver 0.0.0.0:8000" C-m

    # run the windshaft maptiles
    tmux new-window -t vagrant:1 -n 'windshaft'
    tmux send-keys -t vagrant:1 "node /home/vagrant/mapaguarani-tiler/app.js" C-m 

SCRIPT

Vagrant.configure('2') do |config|

    config.vm.box = 'ubuntu/trusty64'
    # config.vm.box_url = "http://files.vagrantup.com/" + config.vm.box + ".box"

    config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
    end

    config.ssh.forward_agent = true
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 8000, guest: 8000
    config.vm.network :forwarded_port, host: 4000, guest: 4000

    config.vm.provision "shell", inline: $setup
    config.vm.provision "shell", inline: $dependencies
    config.vm.provision "shell", inline: $virtualenv, privileged: false
    config.vm.provision "shell", inline: $import_layers, privileged: false
    config.vm.provision "shell", inline: $windshaft
    config.vm.provision "shell", inline: $maptiler, privileged: false
    config.vm.provision "shell",
            inline: $runserver,
            privileged: false,
            run: "always"
end
