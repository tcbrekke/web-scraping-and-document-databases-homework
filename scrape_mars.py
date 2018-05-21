from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time 

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():

    browser = init_browser()
    rollup_dict = {}

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
    rollup_dict['featured_image_url'] = featured_image_url

    #Scrape Mars weather
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    time.sleep(2)
    mars_weather = browser.find_by_css('p.js-tweet-text').text

    rollup_dict['mars_weather'] = mars_weather

    #Scrape facts table

    mars_facts_url = 'https://space-facts.com/mars/#facts'
    browser.visit(mars_facts_url)

    time.sleep(2)
    facts_table_scrape = soup.find('table', class_='tablepress-id-mars')

    facts_df = pd.read_html(str(facts_table_scrape))
    facts_conversion_table = facts_df.to_html()

    rollup_dict['facts'] = facts_conversion_table

    #Scrape images - the large ones - I'm really not sure why we want giant TIFFs, but the client is always right! (Yeah but I grabbed the JPEGs too anyway because I am not sure the client is really 100% right in this case. They can have their TIFF URLs but to save myself the time of making updates later I'm going to also add some JPEGs to the dictionary. Just in case.)

    hemispheres_images_home_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_images_home_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_links = soup.find_all('a', class_='product-item')

    all_links = []
    hemi_list = []

    #Find URLs of image pages, store them
    for link in set(hemisphere_links):
        current_link = link.get('href')
        all_links.append(current_link)

    #Eliminate duplicates
    unique_links = list(set(all_links))

    #Loop through image pages pulling down URLs for jpeg and tiff, as well as page titles (minus 'enhanced' for clarity) and add them to a list of dictionaries
    for i in range(len(unique_links)):
        hemi_dict = {}
        browser.visit((f'https://astrogeology.usgs.gov{unique_links[i]}'))
        time.sleep(2)
        hemi_title_raw = browser.find_by_css('h2.title').text
        hemi_title_final = hemi_title_raw.replace(' Enhanced', '')
        tiff_url = browser.find_link_by_text('Original')['href']
        jpeg_url = browser.find_link_by_text('Sample')['href']
        hemi_dict['title'] = hemi_title_final
        hemi_dict['tiff_url'] = tiff_url
        hemi_dict['img_url'] = jpeg_url
        hemi_list.append(hemi_dict)
    
    rollup_dict['hemisphere_images'] = hemi_list

    browser.quit()

    return rollup_dict