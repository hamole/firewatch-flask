import os, requests, re, dateutil.parser, sqlite3
import xml.etree.ElementTree as ET
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.routing import BaseConverter
from bs4 import BeautifulSoup
from collections import OrderedDict
app = Flask(__name__)
app.config['DEBUG'] = True

class RegexConverter(BaseConverter):
  def __init__(self, url_map, *items):
    super(RegexConverter, self).__init__(url_map)
    self.regex = items[0]

utf8_parser = ET.XMLParser(encoding='utf-8')

app.url_map.converters['regex'] = RegexConverter

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method=='POST':
    if request.form['postcode']:
      conn = sqlite3.connect('postcodes.sqlite')
      conn.row_factory = sqlite3.Row #Return rows as dicts
      c = conn.cursor()
      c.execute("SELECT * from postcodes WHERE postcode = %s"%request.form['postcode'])
      result = c.fetchone()
      if result is None:
        return render_template("index.html", error = 'Postcode not found. Please enter a valid Victorian postcode')
      else:
        return redirect(url_for('main',postcode=result['postcode']))
  else:
    return render_template("index.html")

@app.route('/<regex("[0-9]{4}"):postcode>/')
def main(postcode):
  conn = sqlite3.connect('postcodes.sqlite')
  conn.row_factory = sqlite3.Row #Return rows as dicts
  c = conn.cursor()
  c.execute("SELECT * from postcodes WHERE postcode = %s"%postcode)
  result = c.fetchone()
  if result is None:
    return "Sorry, postcode not supported or not found"
  else:
    forecast = OrderedDict(sorted(danger_rating(result['cfa_district_url']).items()))
    today_date, today_conditions  = forecast.popitem(last=False)
    return render_template("dashboard.html",
      danger_forecast = forecast,
      today = today_conditions,
      data = result,
      temperature_unit = 'c')

def danger_rating(district):
  r = requests.get('http://www.cfa.vic.gov.au/restrictions/%s-firedistrict_rss.xml' % district)# XML feed file/URL
  root = ET.fromstring(r.text)
  danger_forecast = {}
  for day in root.iter('item'):
    if 'Fire restrictions' in day.find('title').text:
      continue
    date = dateutil.parser.parse(day.find('title').text, fuzzy = True).date()
    short_date = day.find('title').text.split(',',1)[0]
    dangercode, danger = get_danger(day.find('description').text, district)
    danger_forecast[date] = {'ratingcode': dangercode,'rating':danger,'short_date':short_date}
  return danger_forecast

def get_danger(text, district):
  ratings = {
    'codered':'Code Red', 
    'extreme':'Extreme', 
    'severe':'Severe', 
    'veryhigh':'Very High',
    'high':'High',
    'lowtomoderate':'Low to Moderate',
    'low-moderate':'Low - Moderate',
    'noforecast':'No Forecast',
  }
  rating = False
  html = BeautifulSoup(text)
  images = html.find_all("img", src=True)
  for image in images:
    if district in image['src']:
      rating = image['src'].split('/')[-1].split('.')[0]
  if rating:
    return (rating, ratings[rating])
  else:
    return ('error','Error Getting Forecast')

if __name__ == '__main__':
    app.run()