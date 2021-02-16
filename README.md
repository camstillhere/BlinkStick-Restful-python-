# BlinkStick-Restful-python-
Pure python based RESTful for blinkstick

## Reason
I built another repo which did this all with Java... but the raspberry pi implementation of HIDAPI was impossible to install!
This repo is pure python and it calls on the same librarys that the blinkstick projects themselves run on so it should be far more stable going forward too.
This is designed to be run as a purely headless server that allows you to controll the blinksticks attached with a REST server

# installation

Install https://github.com/arvydas/blinkstick-python

sudo apt-get install python-pip
sudo pip install blinkstick

### optional
sudo blinkstick --add-udev-rule

## Then install dependencies for this script

sudo pip install flask

### optional 
flask run --host=0.0.0.0

mkdir blinkstickREST
cd blinkstickREST
wget "https://github.com/camstillhere/BlinkStick-Restful-python-/releases/download/1.0.0/blinkstickRestful.py"
python blinkstickRestful.py

## Automatically booting and running the blinkstick server
