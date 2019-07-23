#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 10:52:33 2019

@author: manzar
"""
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
url = "https://www.saudiexports.sa/en/ExportersDirectory"

wb = webdriver.Chrome()
wb.get(url)
links = []
for i in range(1, 208):
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    link = soup.findAll('div', {'class': 'btndiv'})
    if(i == 207):
        ran = 4
    else:
        ran = 6
    for i in range(ran):
        print(urljoin(url, link[i].a.attrs['href']))
        links.append(urljoin(url, link[i].a.attrs['href']))
    
    xpath_main = '//*[@id="ctl00_ctl57_g_f2bc2d7e_98a3_4e34_b4a5_352428e82453_ctl00_lvExportersPager"]/a['
    page = soup.findAll('div', {'class': 'paging'})
    a = page[0].findAll('a')
    xpath = xpath_main + str(len(a)) + ']'
    wb.find_element_by_xpath(xpath).click()
    
header = "Company name, Email, Telephne, website\n"
file = open('assignment.csv', 'a')
file.write(header)
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    content = soup.findAll('div', {'class': 'comntxt greenColor'})
    try:
        data = content[1].findAll('a', {'target': '_blank'})
        web = data[0].attrs['href']
    except:
        web = 'NaN'
    
    name = soup.findAll('div', {'class': 'event-data col-sm-6 profile'})
    name = name[0].h3.text.lstrip()
    try:
        contact = soup.findAll('div', {'class': 'ContactBox'})
        contact = contact[0].contents[1::2]
        try:
            email = contact[-1].text.replace('\r\n', '').lstrip()
        except:
            email = 'NaN'
        
        try:
            tel = contact[-2].text.replace('\r\n', '').lstrip()
        except:
            tel = 'NaN'
    except:
        tel = 'NaN'
        email = 'NaN'
    
    print(name, email, tel, web)
    file.write(name.replace(',', '') + ', ' + email + ', ' + tel + ', ' + web + '\n')
file.close()