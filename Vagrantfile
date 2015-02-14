# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/fedora-21"

  config.vm.network "forwarded_port", guest: 80, host: 8080

  config.vm.synced_folder ".", "/srv/www/ISU2CDC15-WWW"

  # For masterless salt
  config.vm.synced_folder "vagrant/salt/", "/srv/salt/"

  config.vm.provision :salt do |salt|
      salt.minion_config = "vagrant/salt_minion"
      salt.run_highstate = true
  end

  # config.vm.provider "virtualbox" do |vb|
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end

end
