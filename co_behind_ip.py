#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:09:21 2020

@author: artemponomarev
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

#
#import time
#import datetime
#import yagmail
#import smtplib
#import base64
#
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from lxml import html
#from email import encoders
#from email.message import Message
#from email.mime.audio import MIMEAudio
#from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#
#def find_alert_date(src_str):
#
#    search_word1='<time>'
#    sub_index = src_str.find(search_word1)
#    src_str=src_str[sub_index+len(search_word1):]
#    search_word2='</time>'
#    sub_index = src_str.find(search_word2)
#    date=src_str[:-len(src_str) + sub_index]
#
#    return date
#
#def alert_extraction1(src_str):
#
#    search_word1='filters'
#    sub_index = src_str.find(search_word1)
#    src_str=src_str[sub_index+len(search_word1):]
#
#    search_word4='Previous'
#    sub_index = src_str.find(search_word4)
#    src_str=src_str[:-len(src_str)+sub_index]
#
#    src_str=src_str.replace("View all notifications                         Informational Message  Normal  Systems Affected  Critical Issue          Close",'')
#    src_str=src_str.replace('\n', ' ')
#    src_str=src_str[:-1]
#    src_str=src_str.replace('   ', ' ')
#
#    return src_str[:-1]
#
#def create_message(sender, to, subject, message_text):
#    """Create a message for an email.
#  Args:
#    sender: Email address of the sender.
#    to: Email address of the receiver.
#    subject: The subject of the email message.
#    message_text: The text of the email message.
#  Returns:
#    An object containing a base64url encoded email object.
#    """
#    message = MIMEText(message_text)
#    message['to'] = to
#    message['from'] = sender
#    message['subject'] = subject
#
#    return message.as_string()
#
#link_consolidated_tape_association = 'https://www.ctaplan.com/'
#print(link_consolidated_tape_association)
#link_alerts = "https://www.ctaplan.com/alerts#110000144324"
#print(link_alerts)
#client_email = 'artem_ponomarev@yahoo.com' # change this to the real client
#print(client_email)
#message_old=""
#browser = webdriver.Firefox()
#
#i=0
#while True:
#
#    message_old="" # comment this line to start monitoring new alerts only
## is the line is on, then the daemon sends the latest alert every min.
#
#    while True:
#
#        browser.get(link_alerts) #navigate to the page
#        innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
#     # this innerHTML trick is what scrapes JAVA-ridden webpage
#        f = open('CTA_full.html', 'w')
#        f.write(str(innerHTML))
#        f.close
#        date=find_alert_date(innerHTML)
#        print(date)
#        if date != '':
#            break
#
#    page = html.document_fromstring(innerHTML.replace('>','> ')) #parse innerHTML
#    fset = page.get_element_by_id("business-unit-history")
#    fset_text = fset.text_content()
#    alert=alert_extraction1(fset_text)
#    email="Alert Date: " + date +"\n" + alert + "\n\nBanzai!"
#    message=create_message("artemponomarevjetski@gmail.com", client_email, "News alert #"+str(i), email)
#    print("Emailed to client:\n" + message)
#    if message != message_old:
#        yagmail.SMTP('artemponomarevjetski@gmail.com').send(client_email, "News alert #"+str(i), message)
#    message_old = message
#
#    i+=1
#    print(i, datetime.datetime.now())
#    time.sleep(60)
