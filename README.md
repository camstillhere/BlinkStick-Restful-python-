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

## Launch a browser

Open the second link pointing to a /web/ folder

http://192.168.1.112:80/web/index.html

With this site you can run a number of tests to ensure that your blinkstick is functioning.

You can watch the api's being called and see how it works.

When you are ready to start integrating it into your projects download the postman examples:

https://github.com/camstillhere/BlinkStick-Restful-python-/raw/main/BlinkStick%20Cameron.postman_collection.json
