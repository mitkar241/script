# -*- mode: ruby -*-
# vi: set ft=ruby :

servers=[
  {
    :hostname => "web",
    :ip => "192.168.0.6",
    :box => "chenhan/ubuntu-desktop-20.04",
    :box_version => "v20200424",
    :ram => 1024,
    :cpu => 2
  },
  {
    :hostname => "db",
    :ip => "192.168.0.7",
    :box => "chenhan/ubuntu-desktop-20.04",
    :box_version => "v20200424",
    :ram => 1024,
    :cpu => 2
  }
]

Vagrant.configure("2") do |config|
  servers.each do |machine|
      config.vm.define machine[:hostname] do |node|
          node.vm.box = machine[:box]
          node.vm.box_version = machine[:box_version]
          node.vm.hostname = machine[:hostname]
          node.vm.network "public_network", ip: machine[:ip]
          node.vm.provider "virtualbox" do |vb|
              vb.gui = true
              vb.customize ["modifyvm", :id, "--name", machine[:hostname]]
              vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
          end
          node.vm.provision :shell, :inline => "sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config; sudo systemctl restart sshd;", run: "always"
          node.vm.provision :shell, :inline => "username=raktim; password=raktim; sudo useradd -p $(openssl passwd -crypt $password) -m -s /bin/bash $username; sudo usermod -aG sudo $username", run: "always"
          node.vm.provision :shell, :inline => "sudo usermod --expiredate 1 vagrant", run: "always"
          #node.vm.provision :shell, :inline => "sudo apt install ubuntu-desktop-minimal -y", run: "always"
      end
  end
end
