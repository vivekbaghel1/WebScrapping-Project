# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import pandas as pd
import requests

# initialize the browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Scrape function
def scrape():
    browser = init_browser()

    #Dictionary to store the data
    data_mars = {}

    # NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')

    # New Title
    news_title = soup.find('div',class_='content_title').text

    # New Header
    news_p = soup.find('div', class_='rollover_description_inner').text

    #browser.quit()

    # JPL Mars Space Images - Featured Image
    # ------------------------------------------
    # Visit the url for JPL Featured Space. 
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Save a complete url string for this image
     
    urlimg = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(urlimg)

    #time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')

    img_url = soup.find('img', class_='thumb')['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+img_url
    
    #browser.quit()

    # Mars Weather
    # ---------------
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
    # Save the tweet text for the weather report as a variable called mars_weather

    tweet_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(tweet_url)

    #time.sleep(1)

    html = browser.html

    # Scrape the tweet from the webpage
    twt_res = bs(html,'html.parser')
    twt_wea = twt_res.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # Extract the 2nd tweet from the webpage
    wheather_tweet = twt_wea[1].text
    wheather_tweet = wheather_tweet.replace('pic.twitter.com/WlR4gr8gpC','')

    # Store in mars_weather
    mars_weather = wheather_tweet

    #browser.quit()

    # ---
    # Mars Facts
    # -----------
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet
    # including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string

    fact_url = 'https://space-facts.com/mars/'
    browser.visit(fact_url)

    #time.sleep(1)

    # Use Pandas to read html file.
    fact = pd.read_html(fact_url)
    fact_df = pd.DataFrame(fact[0])
    fact_df = fact_df.rename(columns={0:'Description',1: 'Values'})
    fact_df = fact_df.set_index('Description')
    df_to_html = fact_df.to_html(classes='mars_scrape_info')
    df_to_html = df_to_html.replace("\n"," ")
    
    #browser.quit()

    # Mars Hemispheres
    # -----------------
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)

    #time.sleep(1)

    html = browser.html

    soup = bs(html, 'html.parser')
    
    # list to store the image and urls.
    hemis_image = []

    for x in range(4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[x].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        image1 = soup.find('img',class_='wide-image')['src']
        image_title = soup.find('h2', class_='title').text
        image1_url = 'https://astrogeology.usgs.gov' + image1
        img_dict = {'title':image_title, 'image_url':image1_url}
        hemis_image.append(img_dict)
        browser.back()

    data_mars = {
        'New_Title': news_title,
        'New_Heading': news_p,
        'Feature_Image': featured_image_url,
        'Weather': mars_weather,
        'Facts': df_to_html,
        'Hemisphere': hemis_image
    }

    browser.quit()

    return data_mars


