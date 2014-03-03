import os, requests, re
import xml.etree.ElementTree as ET
import dateutil.parser 
from flask import Flask, render_template
from werkzeug.routing import BaseConverter
from bs4 import BeautifulSoup
from collections import OrderedDict

app = Flask(__name__)
app.config['DEBUG'] = True

class RegexConverter(BaseConverter):
  def __init__(self, url_map, *items):
    super(RegexConverter, self).__init__(url_map)
    self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/<regex("[0-9]{4}"):postcode>/')
def main(postcode):
  if postcode in ['3825','3840','3842','3869','3870']:
    cfa_district = 'westandsouthgippsland'
    roads_region = 'gippsland'
    roads_municipality = 'latrobe'
  else:
    return "Sorry, dashboard only for Latrobe Valley at this time"
  return render_template("index.html",danger_forecast = OrderedDict(sorted(danger_rating(cfa_district).items())))

def danger_rating(district):
  r = requests.get('http://www.cfa.vic.gov.au/restrictions/%s-firedistrict_rss.xml' % district)# XML feed file/URL
  root = ET.fromstring(r.text)
  danger_forecast = {}
  for day in root.iter('item'):
    if 'Fire restrictions' in day.find('title').text:
      continue
    date = dateutil.parser.parse(day.find('title').text, fuzzy = True).date()
    short_date = day.find('title').text.split(',',1)[0]
    danger = get_danger(day.find('description').text, district)
    danger_forecast[date] = {'rating':danger,'short_date':short_date}
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
    return ratings[rating]
  else:
    return 'Error Getting Forecast'

