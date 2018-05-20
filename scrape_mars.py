from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time 

def scrape():
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Scrape NASA featured Mars image

    nasa_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.click_link_by_id('full_image')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    browser.click_link_by_partial_href('/spaceimages/images/largesize')

    featured_image_url = browser.url
    print(featured_image_url)

    #Scrape Mars weather
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(1)
    mars_weather = soup.find('p', class_='js-tweet-text').text

    print(most_recent_mars_weather)

    #Scrape facts table

    mars_facts_url = 'https://space-facts.com/mars/#facts'
    browser.visit(mars_facts_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    facts_table_scrape = soup.find('table', class_='tablepress-id-mars')

    facts_df = pd.read_html(str(facts_table_scrape))[0]
    facts_conversion_table = facts_df.to_html()

    #Scrape images - the large ones - I'm really not sure why we want giant TIFFs, but the client is always right! (Yeah but I grabbed the JPEGs too anyway because I am not sure the client is really 100% right in this case. They can have their TIFF URLs but to save myself the time of making updates later I'm going to also add some JPEGs to the dictionary. Just in case.)

    hemispheres_images_home_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_images_home_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_links = soup.find_all('a', class_='product-item')

    all_links = []
    hemi_dict = {}

    for link in set(hemisphere_links):
        current_link = link.get('href')
        all_links.append(current_link)
        
    unique_links = list(set(all_links))

    for i in range(len(unique_links)):
        browser.visit(f'https://astrogeology.usgs.gov{unique_links[i]}')
        time.sleep(5)
        hemi_title_raw = soup.find('h2', class_='title').text
        hemi_title_final = hemi_title_raw.replace(' Enhanced', '')
        tiff_url = browser.find_link_by_text('Original')['href']
        jpeg_url = browser.find_link_by_text('Sample')['href']
        hemi_dict['title'] = hemi_title_final
        hemi_dict['tiff_url'] = tiff_url
        hemi_dict['img_url'] = jpeg_url

