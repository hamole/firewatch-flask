firewatch-flask
===============

A port of the Firewatch Dashboard wordpress plugin developed by the RHoK team to a Flask application

## Usage ##
The dashboard for a postcode is accessed by appending the postcode to the main url.

For example, to get to the dashboard for Churchill(3842) you would visit
```
127.0.0.1:5000/3842/
``
A basic index page with a textbox input is also included

## Installation ##
Clone the repository, setup a fresh virtualenv and run
```
pip install -r requirements.txt
```
You can then run the Flask development server by running
```
python firewatch.py
```
Navigate to 127.0.0.1:5000 and you should see the index page.
