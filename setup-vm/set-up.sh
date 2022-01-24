#!/bin/bash

##########
# @description
##########
# purpose : setup environment for computes
# arguments : sequential - HOSTNAME MGMT_IP

##########
# setup static DNS
##########
sudo mv etc/hosts /etc/hosts
# sudo mv etc/resolv.conf /etc/resolv.conf

##########
# set static IP address
##########
export MGMT_IP=$2
perl -pe 's|\$([A-Za-z_]+)|$ENV{$1}|g' etc/netplan/01-netcfg.yaml.template.sh > etc/netplan/01-netcfg.yaml
unset MGMT_IP
sudo mv etc/netplan/01-netcfg.yaml /etc/netplan/01-netcfg.yaml
sudo netplan apply

##########
# check Internet connectivity
##########
# to be added

##########
# package refresh
##########
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y

##########
# git packages
##########
# git should be already installed
sudo apt install git -y

##########
# essential packages
##########
sudo apt install build-essential -y
sudo apt install python3 -y

##########
# set hostname
##########
export HOSTNAME=$1
sudo hostnamectl set-hostname $HOSTNAME
unset HOSTNAME

##########
# set bash as default shell
##########
# check current shell and update if needed
sudo mv etc/default/useradd /etc/default/useradd

##########
# setup bash prompt
##########
sudo mv etc/skel/.bashrc /etc/skel/.bashrc
sudo mv etc/skel/.profile /etc/skel/.profile

##########
# network related packages
##########
sudo apt install curl -y
sudo apt install net-tools -y

##########
# SSH related packages
##########
sudo apt install openssh-server -y
sudo apt install openssh-client -y

##########
# create new user
##########
# to be added

##########
# jenkins related packages
##########
sudo apt install default-jre -y
sudo mkdir /home/mitkar/jenkins_remote_directory

##########
# docker related packages
##########
sudo apt install docker.io -y
sudo usermod -aG docker mitkar

##########
# package refresh
##########
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
