# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      dhcp6: no
      addresses: [$MGMT_IP/24]
      gateway4: 192.168.0.1
      nameservers:
        addresses: [8.8.8.8,8.8.4.4]
