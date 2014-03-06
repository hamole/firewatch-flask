import csv, requests, json, sqlite3
import xml.etree.ElementTree as ET

vicroads_url = {
  'Colac Otway':'/barwon/colac-otway',
  'Corangamite':'/barwon/corangamite',
  'Geelong':'/barwon/geelong',
  'Glenelg':'/barwon/glenelg',
  'Moyne':'/barwon/moyne',
  'Queenscliffe':'/barwon/queenscliffe',
  'Southern Grampians':'/barwon/southern-grampians',
  'Surf Coast':'/barwon/surf-coast',
  'Warrnambool':'/barwon/warrnambool',
  'Bass Coast':'/gippsland/bass-coast',
  'Baw Baw':'/gippsland/baw-baw',
  'East Gippsland':'/gippsland/east-gippsland',
  'French Island':'/gippsland/french-island',
  'Latrobe':'/gippsland/latrobe',
  'Mount Baw Baw':'/gippsland/mount-baw-baw',
  'South Gippsland':'/gippsland/south-gippsland',
  'Wellington':'/gippsland/wellington',
  'Ararat':'/grampians/ararat',
  'Ballarat':'/grampians/ballarat',
  'Golden Plains':'/grampians/golden-plains',
  'Hepburn':'/grampians/hepburn',
  'Hindmarsh':'/grampians/hindmarsh',
  'Horsham':'/grampians/horsham',
  'Moorabool':'/grampians/moorabool',
  'Northern Grampians':'/grampians/northern-grampians',
  'Pyrenees':'/grampians/pyrenees',
  'West Wimmera':'/grampians/west-wimmera',
  'Yarriambiack':'/grampians/yarriambiack',
  'Alpine':'/hume/alpine',
  'Benalla':'/hume/benalla',
  'Falls Creek':'/hume/falls-creek',
  'Indigo':'/hume/indigo',
  'Lake Mountain':'/hume/lake-mountain',
  'Mansfield':'/hume/mansfield',
  'Mitchell':'/hume/mitchell',
  'Moira':'/hume/moira',
  'Mount Buller':'/hume/mount-buller',
  'Mount Hotham':'/hume/mount-hotham',
  'Mount Stirling':'/hume/mount-stirling',
  'Murrindindi':'/hume/murrindindi',
  'Shepparton':'/hume/shepparton',
  'Strathbogie':'/hume/strathbogie',
  'Towong':'/hume/towong',
  'Wangaratta':'/hume/wangaratta',
  'Wodonga':'/hume/wodonga',
  'Bendigo':'/loddon-mallee/bendigo',
  'Buloke':'/loddon-mallee/buloke',
  'Campaspe':'/loddon-mallee/campaspe',
  'Central Goldfields':'/loddon-mallee/central-goldfields',
  'Gannawarra':'/loddon-mallee/gannawarra',
  'Loddon':'/loddon-mallee/loddon',
  'Macedon Ranges':'/loddon-mallee/macedon-ranges',
  'Mildura':'/loddon-mallee/mildura',
  'Mount Alexander':'/loddon-mallee/mount-alexander',
  'Swan Hill':'/loddon-mallee/swan-hill',
  'Default':'/melbourne-metropolitan/'
}

mallee = 'Buloke Shire Gannawarra Shire Mildura Rural City Swan Hill Rural City Yarriambiack Shire'
wimmera = 'Hindmarsh Shire Horsham Rural City Northern Grampians Shire West Wimmera Shire Yarriambiack'
south_west = 'Ararat Rural City Colac Otway Shire Corangamite Shire Glenelg Shire Moyne Shire Pyrenees Shire Southern Grampians Shire Warrnambool City'
northern_country = 'Campaspe Shire Greater Bendigo City Greater Shepparton City Loddon Shire Moira Shire Strathbogie Shire'
north_central = 'Central Goldfields Shire Lake Mountain  Resort (Unincorporated) Mitchell Shire Mount Alexander Shire Murrindindi Shire'
central = 'Ballarat City Banyule City Bass Coast Shire Bayside City Boroondara City Brimbank City Cardinia Shire Casey City Darebin City Frankston City French Island (Unincorporated) Glen Eira City Golden Plains Shire Greater Dandenong City Greater Geelong City Hepburn Shire Hobsons Bay City Hume City Kingston City Knox City Macedon Ranges Shire Manningham City Maribyrnong City Maroondah City Melbourne City Melton Shire Monash City Moonee Valley City Moorabool Shire Moreland City Mornington Peninsula Shire Nillumbik Shire Port Phillip City Queenscliffe Borough Stonnington City Surf Coast Shire Whitehorse City Whittlesea City Wyndham City Yarra City Yarra Ranges Shire'
north_east = 'Alpine Shire Benalla Rural City Falls Creek  Resort (Unincorporated) Indigo Shire Mansfield Shire Mount Buller  Resort (Unincorporated) Mount Hotham  Resort (Unincorporated) Mount Stirling  Resort (Unincorporated) Towong Shire Wangaratta Rural City Wodonga City'
east_gippsland = 'East Gippsland'
west_south_gippsland = 'Baw Baw Shire Latrobe City Mount Baw Baw  Resort (Unincorporated) South Gippsland Shire Wellington Shire'

cfa_districts = {
  'Malle':mallee,
  'Wimmera':wimmera,
  'South West':south_west,
  'Northern Country':northern_country,
  'North Central':north_central,
  'Central':central,
  'North East':north_east,
  'East Gippsland':east_gippsland,
  'West and South Gippsland':west_south_gippsland,
}
lat_longs = {}
seen_postcodes = []
with open('AU.txt','rU') as csvfile:
  reader = csv.reader(csvfile,delimiter='\t')
  for row in reader:
    if len(row) > 2 and row[1] not in lat_longs and row[1] not in seen_postcodes:
      lat_longs[row[1]] = {'latitude':row[-3],'longitude':row[-2]}
      url = '''http://query.yahooapis.com/v1/public/yql?q=select%%20*%%20from%%20geo.placefinder%%20where%%20text%%3D"%s%%2C%s"%%20and%%20gflags%%3D"R"'''%(row[-3],row[-2])
      resp = requests.get(url)
      root = ET.fromstring(resp.content)
      woeid = root.findtext('.//woeid')
      lat_longs[row[1]]['woeid'] = woeid
      postcode = row[1]
      seen_postcodes.append(postcode)

conn = sqlite3.connect('postcodes.sqlite')
c = conn.cursor()
seen_postcodes = []
with open('LocalityFinder.csv','rU') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    council = row['Municipality\n\nName'].rsplit(' ',2)[0]
    postcode = row['Post\n\nCode']
    if council in vicroads_url:
      url = vicroads_url[council]
    else:
      url = vicroads_url['Default'] + council.lower().replace(' ','-')
    for district, councils in cfa_districts.items():
      if council in councils:
        cfa_district = district
        cfa_district_url = "".join(cfa_district.lower().split())
    if postcode not in seen_postcodes:
      query = "INSERT INTO postcodes VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(postcode,cfa_district,lat_longs[postcode]['woeid'],council,lat_longs[postcode]['latitude'],lat_longs[postcode]['longitude'],url,cfa_district_url)
      c.execute(query)
      seen_postcodes.append(postcode)
    print 'Postcode: %s, Council: %s, URL: %s, CFA: %s' %(postcode,council,url, cfa_district)
    print 'Lat: %s, Long: %s, WOEID: %s' %(lat_longs[postcode]['latitude'],lat_longs[postcode]['longitude'], lat_longs[postcode]['woeid'])
conn.commit()
conn.close()