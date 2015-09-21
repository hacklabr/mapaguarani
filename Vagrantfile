$setup = <<SCRIPT
    DEBIAN_FRONTEND=noninteractive apt-get update
SCRIPT

$dependencies = <<SCRIPT
    export DEBIAN_FRONTEND=noninteractive
    apt-get install -y postgresql postgresql-contrib postgis postgresql-9.3-postgis-2.1 postgresql-9.3-postgis-2.1-scripts libpq-dev
    apt-get install -y build-essential git python-dev python3-dev libjpeg-dev zlib1g-dev python-virtualenv binutils libproj-dev gdal-bin

    # Needed to install Fiona via pip
    apt-get install -y libgdal-dev

    # Configure postgis
    su postgres -c "createuser vagrant"
    su postgres -c "createdb -O vagrant template_postgis -E UTF-8"
    su postgres -c "createlang plpgsql template_postgis"
    su postgres -c "psql -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql"
    su postgres -c "psql -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql"

    su postgres -c "createdb -T template_postgis mapaguarani"
    echo "GRANT ALL PRIVILEGES ON DATABASE mapaguarani to vagrant;" | su postgres -c "psql"

SCRIPT

$virtualenv = <<SCRIPT

    # Python env
    # must run with vagrant user
    virtualenv -p /usr/bin/python3 mapaguarani-env
    source /home/vagrant/mapaguarani-env/bin/activate
    /home/vagrant/mapaguarani-env/bin/pip install -r /vagrant/requirements/local.txt

SCRIPT

$runserver = <<SCRIPT
    # must run with vagrant user
    cd /vagrant
    /home/vagrant/mapaguarani-env/bin/python3 manage.py migrate
    /home/vagrant/mapaguarani-env/bin/python3 manage.py runserver 0.0.0.0:8000 &

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
    npm install request
    npm install underscore
    npm install windshaft
    # FIXME for some reason, it only get done in second time
    npm install windshaft
    cp config.vagrant.js config.js
    node app.js &
SCRIPT

Vagrant.configure('2') do |config|

    config.vm.box = 'ubuntu/trusty64'
    # config.vm.box_url = "http://files.vagrantup.com/" + config.vm.box + ".box"

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
    end

    config.ssh.forward_agent = true
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 8000, guest: 8000
    config.vm.network :forwarded_port, host: 4000, guest: 4000

    config.vm.provision "shell", inline: $setup
    config.vm.provision "shell", inline: $dependencies
    config.vm.provision "shell", inline: $virtualenv, privileged: false
    config.vm.provision "shell", inline: $windshaft
    config.vm.provision "shell",
            inline: $maptiler,
            privileged: false,
            run: "always"
    config.vm.provision "shell",
            inline: $runserver,
            privileged: false,
            run: "always"
end
