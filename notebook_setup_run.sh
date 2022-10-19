#!/bin/sh
apt update

apt install sudo

mkdir -p /usr/share/man/man1

sudo apt install  -y default-jre

sudo apt install  -y python3

sudo apt-get install  -y python3-pip

export PATH=/opt/conda/bin:$PATH in ~/.bashrc

activate base

conda install -y pip

pip install -r requirements.txt


#how to execute the script
#bash notebook_setup_run.sh