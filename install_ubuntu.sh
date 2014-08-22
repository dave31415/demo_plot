#!/bin/sh

#always update apt
sudo apt-get update
#install git 
sudo apt-get -y install git
#install pip and scientific python stuff
sudo apt-get -y install python-pip
sudo apt-get -y install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose 
#install other python stuff with pip 
sudo pip install flask vincent
#install apache and mod-wsgi
sudo apt-get -y install apache2 libapache2-mod-wsgi

#get a git repo
cd /var/www
git clone git@github.com:dave31415/demo_plot.git
cd demo_plot
cd
python deploy.py

sudo a2ensite sitename.com
sudo /etc/init.d/apache2 restart
