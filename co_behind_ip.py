#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:09:21 2020

@author: artemponomarev

go from a domain name to the IP, to company's website, to 
company's name, to its geographic location (in any order)...

output is HTML....
"""

from ip2geotools.databases.noncommercial import DbIpCity
import folium

myIP = '2600:1700:3681:2400:d519:59d2:4879:349f'

inputIPdict = {
    '73.93.153.42' : 'https://www.coworkiing.com/',
    '157.130.196.214' : 'http://wework.com/',
    '199.52.9.62' : 'https://www.ey.com/',
    '144.178.28.64' : 'https://www.apple.com/',
    '144.178.28.1' : 'https://www.apple.com/',
    '136.146.65.33' : 'https://www.salesforce.com/',
    '104.193.168.14' : None
}

RESPONSE = DbIpCity.get(myIP, api_key='free')

print(RESPONSE.ip_address)
print()
print(RESPONSE.city)
print()
print(RESPONSE.region)
print()
print(RESPONSE.country)
print()
print(RESPONSE.latitude)
print()
print(RESPONSE.longitude)
print()
print(RESPONSE.to_json())
print()
print(RESPONSE.to_xml())
print()
print(RESPONSE.to_csv(','))


folium_map = folium.Map(location=[RESPONSE.latitude,RESPONSE.longitude],
                        zoom_start=12)


#FastMarkerCluster(data=list(zip(df['latitude'].values, df['longitude'].values))).add_to(folium_map)
#folium.LayerControl().add_to(folium_map)
folium_map.save('index.html')
#from IPython.core.display import HTML
#HTML('index.html')
