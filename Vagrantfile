# -*- mode: ruby -*-
# vi: set ft=ruby :

# sample shell script
bootstrap = <<SCRIPT
  useradd -m mitkar --groups sudo
  su -c "printf 'cd /home/mitkar\nsudo su mitkar' >> .bash_profile" -s /bin/sh vagrant
SCRIPT

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  
  # GUI version
  config.vm.box = "ubuntu/focal64"
  # CLI version
  # config.vm.box = "geerlingguy/ubuntu2004"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Setting up private_network to have virtual host
  config.vm.network :public_network, ip: "192.168.0.10"
  config.vm.hostname = "vm-hostname"
  config.vm.define "vm-define"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
    config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
      vb.gui = true
      vb.name = "vb-name"
  #   # Customize the amount of memory on the VM:
      vb.memory = "4096"
      vb.customize ["modifyvm", :id, "--vram", "12"]
    end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
  sudo apt update -y
  sudo apt upgrade -y
  sudo apt autoremove -y
  sudo apt install ubuntu-desktop-minimal -y
  SHELL
end