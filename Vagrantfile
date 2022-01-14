# -*- mode: ruby -*-
# vi: set ft=ruby :

=begin
@description: Vagrantfile to deploy with custom user and no vagrant user
@resources:
  - https://www.virtualbox.org/manual/ch08.html#vboxmanage-cmd-overview
gsettings get | set | reset
gsettings list-schemas
gsettings list-recursively
gsettings list-keys org.gnome.desktop.interface
=end

servers=[
  {
    :hostname => "web",
    :ip => "192.168.0.6",
    :box => "chenhan/ubuntu-desktop-20.04",
    :box_version => "20200424",
    :ram => 1024,
    :vram => 128,
    :cpu => 2
  },
  {
    :hostname => "db",
    :ip => "192.168.0.7",
    :box => "chenhan/ubuntu-desktop-20.04",
    :box_version => "20200424",
    :ram => 1024,
    :vram => 128,
    :cpu => 2
  }
]

$ADDUSERSCRIPT = <<-SCRIPT
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo systemctl restart sshd
username=raktim
password=raktim
sudo useradd -p $(openssl passwd -crypt $password) -m -s /bin/bash $username
sudo usermod -aG sudo $username
#sudo apt install ubuntu-desktop-minimal -y
SCRIPT

$DELUSERSCRIPT = <<-SCRIPT
# removing user from '/etc/passwd' removes user from login screen
sudo usermod --expiredate 1 vagrant
sudo sed -i '/vagrant/d' /etc/passwd
sudo service gdm3 restart
# for proper cleanup run this command on first login
#sudo userdel -r vagrant
SCRIPT

$GUISCRIPT = <<-SCRIPT

cat > custom-gui.sh <<EOF
#gsettings get org.gnome.shell favorite-apps

#wallpaper_loc=/home/vagrant/wallpaper.png
#wget -O  "<image-link>"
wallpaper_loc="/usr/share/backgrounds/brad-huchteman-stone-mountain.jpg"
gsettings set org.gnome.desktop.background picture-uri file://

# Setting Scale
gsettings set org.gnome.desktop.interface text-scaling-factor 1.15
# Moving Taskbar to bottom
gsettings set org.gnome.shell.extensions.dash-to-dock dock-position 'BOTTOM'
# Setting theme
gsettings set org.gnome.desktop.interface gtk-theme 'Yaru-dark'
gsettings set org.gnome.desktop.interface cursor-theme 'DMZ-White'
# Setting Font
gsettings set org.gnome.desktop.wm.preferences titlebar-font 'FreeMono Bold 12'
gsettings set org.gnome.desktop.interface monospace-font-name 'FreeMono Bold 12'
gsettings set org.gnome.desktop.interface document-font-name 'FreeMono Bold 12'
gsettings set org.gnome.desktop.interface font-name 'FreeMono Bold 12'
EOF

sudo chmod +x custom-gui.sh
mv ./custom-gui.sh /home/raktim/custom-gui.sh

SCRIPT

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  servers.each do |machine|
      config.vm.define machine[:hostname] do |node|
          if Vagrant.has_plugin? "vagrant-vbguest"
            config.vbguest.no_install  = true
            config.vbguest.auto_update = false
            config.vbguest.no_remote   = true
          end
          node.vm.box = machine[:box]
          node.vm.box_version = machine[:box_version]
          node.vm.hostname = machine[:hostname]
          node.vm.network "public_network", ip: machine[:ip]
          node.vm.provider "virtualbox" do |vb|
              vb.gui = true
              # General.basic
              vb.customize ["modifyvm", :id, "--name", machine[:hostname]]
              # General.Advanced
              vb.customize ["modifyvm", :id, "--clipboard-mode", "bidirectional"]
              vb.customize ["modifyvm", :id, "--draganddrop", "bidirectional"]
              # System.Motherboard
              vb.customize ["modifyvm", :id, "--memory", machine[:ram]]
              # Display.Screen
              vb.customize ["modifyvm", :id, "--vram", machine[:vram]]
              vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
              vb.customize ["modifyvm", :id, "--accelerate3d", "on"]
              # VRDE = VirtualBox Remote Desktop Extension
              vb.customize ["modifyvm", :id, "--vrde", "off"]
          end
          node.vm.provision :shell, :inline => $ADDUSERSCRIPT, run: "always"
          node.vm.provision :shell, :inline => $GUISCRIPT, run: "always"
          node.vm.provision :shell, :inline => $DELUSERSCRIPT, run: "always"
      end
  end
end
