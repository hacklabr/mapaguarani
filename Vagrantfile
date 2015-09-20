$setup = <<SCRIPT
    DEBIAN_FRONTEND=noninteractive apt-get update
SCRIPT

$dependencies = <<SCRIPT
    export DEBIAN_FRONTEND=noninteractive
    apt-get install -y postgresql postgresql-contrib postgis postgresql-9.3-postgis-2.1 postgresql-9.3-postgis-2.1-scripts libpq-dev
    apt-get install -y build-essential git python-dev python3-dev libjpeg-dev zlib1g-dev python-virtualenv binutils libproj-dev gdal-bin

    # Configure postgis
    su postgres -c "createuser vagrant"
    su postgres -c "createdb -O vagrant template_postgis -E UTF-8"
    su postgres -c "createlang plpgsql template_postgis"
    su postgres -c "psql -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql"
    su postgres -c "psql -d template_postgis -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql"

    su postgres -c "createdb -T template_postgis mapaguarani"
    echo "GRANT ALL PRIVILEGES ON DATABASE mapaguarani to vagrant;" | su postgres -c "psql"

    # Python env
    su vagrant -c "virtualenv -p /usr/bin/python3 mapaguarani-env"
    su vagrant -c "source mapaguarani-env/bin/activate"
    su vagrant -c "pip install -r /vagrant/requirements/local.txt"

SCRIPT

$runserver = <<SCRIPT

    cd /vagrant
    echo | su vagrant -c "pwd"
    su vagrant -c "/home/vagrant/mapaguarani-env/bin/python3 manage.py migrate"
    su vagrant -c "/home/vagrant/mapaguarani-env/bin/python3 manage.py runserver 0.0.0.0:8000 &"

SCRIPT

Vagrant.configure('2') do |config|

    config.vm.box = 'ubuntu/trusty64'
    # config.vm.box_url = "http://files.vagrantup.com/" + config.vm.box + ".box"

    config.ssh.forward_agent = true
    # Forward the dev server port
    config.vm.network :forwarded_port, host: 8000, guest: 8000
    config.vm.network :forwarded_port, host: 4000, guest: 4000

    config.vm.provision "shell", inline: $setup
    config.vm.provision "shell", inline: $dependencies
    config.vm.provision "shell", inline: $runserver,
            run: "always"
end
