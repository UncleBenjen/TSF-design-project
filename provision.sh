#!/usr/bin/env bash
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "~~ Provisioning environment for CAAT web application ~~"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
apt-get -y update

# PYTHON
# ~~ Install dependencies ~~
sudo apt-get -y build-dep python3.2
sudo apt-get -y install libreadline-dev libncurses5-dev libssl1.0.0 tk8.5-dev zlib1
# ~~ Download and extract Python3.3 ~~
wget http://python.org/ftp/python/3.3.0/Python-3.3.0.tgz
tar xvfz Python-3.3.0.tgz
# ~~ Configure and Install Python3.3 ~~
cd Python-3.3.0
./configure --prefix=/opt/python3.3
make
sudo make install

# ~~ Create VirtualEnv and install Pip
/opt/python3.3/bin/pyvenv ~/py33
source ~/py33/bin/activate
wget http://python-distribute.org/distribute_setup.py
python distribute_setup.py
easy_install pip

# DJANGO & Other Dependencies
# Assuming python3.3 and pip were correctly installed, and the virtual env is activated:
pip install django
pip install Pillow
pip install reportlab
pip install xlrd

# APACHE
apt-get update
apt-get install -y apache2
rm -rf /var/www
ln -fs /vagrant /var/www

# MYSQL

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "~~ Provisioning complete ~~"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~"