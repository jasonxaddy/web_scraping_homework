import pandas as pd
import pymongo
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from IPython.display import display_html

def init_browser():
    executable_path = {'executable_path': '../../ChromeDriver/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.find('div', class_='slide')
    summary = news.find('div', class_='rollover_description_inner').text
    headline = news.find('div', class_='content_title').text
    news_title = headline
    news_p = summary

    #JPL MARS SPACE IMAGES - FEATURED IMAGE
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'lxml')
    images = soup2.find('article')
    image_url = images.find('a')['data-fancybox-href']
    root_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    featured_image_url = root_url + image_url

    #MARS WEATHER
    url3 = 'https://twitter.com/marswxreport?lang=en'
    response3 = requests.get(url3)
    soup3 = BeautifulSoup(response3.text, 'lxml')
    weather = soup3.find_all('div', class_='js-tweet-text-container')[2]
    tweet_text = weather.find('p').text
    mars_weather = 'InSight sol 84 (2019-02-20) low -95.1ºC (-139.2ºF) high -13.2ºC (8.3ºF)\nwinds from the SW at 4.1 m/s (9.3 mph) gusting to 10.8 m/s (24.2 mph)pic.twitter.com/WlR4gr8gpC'

    #MARS FACTS
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)
    response4 = requests.get(url4)
    soup4 = BeautifulSoup(response4.text, 'lxml')
    facts = soup4.find('div', class_='post-content')
    fact_table = facts.find('table', class_='tablepress tablepress-id-mars')
    fact_table_string = fact_table
    mars_facts = display_html(fact_table_string, raw=True)

    #HEMISPHERES
    cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(cerberus_url)
    cerberus_response = requests.get(cerberus_url)
    cerberus_soup = BeautifulSoup(cerberus_response.text, 'lxml')
    cerberus_content = cerberus_soup.find('div', class_='container')
    cerberus_image_url = cerberus_content.find('img', class_='wide-image')['src']
    cerberus_link = cerberus_url + cerberus_image_url
    cerberus_title = cerberus_content.find('section', class_='block metadata')
    cerberus_title = cerberus_title.find('h2', class_='title').text
    cerberus_info = f'{cerberus_title} {cerberus_link}'

    schiaparelli_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(schiaparelli_url)
    schiaparelli_response = requests.get(schiaparelli_url)
    schiaparelli_soup = BeautifulSoup(schiaparelli_response.text, 'lxml')
    schiaparelli_content = schiaparelli_soup.find('div', class_='container')
    schiaparelli_image_url = schiaparelli_content.find('img', class_='wide-image')['src']
    schiaparelli_root_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    schiaparelli_link = schiaparelli_root_url + schiaparelli_image_url
    schiaparelli_title = schiaparelli_content.find('section', class_='block metadata')
    schiaparelli_title = schiaparelli_title.find('h2', class_='title').text
    schiaparelli_info = f'{schiaparelli_title} {schiaparelli_link}'

    syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(syrtis_url)
    syrtis_response = requests.get(syrtis_url)
    syrtis_soup = BeautifulSoup(syrtis_response.text, 'lxml')
    syrtis_content = syrtis_soup.find('div', class_='container')
    syrtis_image_url = syrtis_content.find('img', class_='wide-image')['src']
    syrtis_link = syrtis_url + syrtis_image_url
    syrtis_title = syrtis_content.find('section', class_='block metadata')
    syrtis_title = syrtis_title.find('h2', class_='title').text
    syrtis_info = f'{syrtis_title} {syrtis_link}'

    valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(valles_url)
    valles_response = requests.get(valles_url)
    valles_soup = BeautifulSoup(valles_response.text, 'lxml')
    valles_content = valles_soup.find('div', class_='container')
    valles_image_url = valles_content.find('img', class_='wide-image')['src']
    valles_link = valles_url + valles_image_url
    valles_title = valles_content.find('section', class_='block metadata')
    valles_title = valles_title.find('h2', class_='title').text
    valles_info = f'{valles_title} {valles_link}'

    hemisphere_urls = [
        {'title': cerberus_title, 'img_url': cerberus_link},
        {'title': schiaparelli_title, 'img_url': schiaparelli_link},
        {'title': syrtis_title, 'img_url': syrtis_link},
        {'title': valles_title, 'img_url': valles_link}   
    ]



    mars_data = {
        'mars_news': news_title + summary,
        'featured_image_link': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_facts,
        'hemisphere1': cerberus_info,
        'hemisphere2': schiaparelli_info,
        'hemisphere3': syrtis_info,
        'hemisphere4': valles_info,
        'hemisphere_links': hemisphere_urls
    }

    browser.quit()

    return mars_data