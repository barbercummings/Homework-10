# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

# Create init_browser function

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

# Create scrape_info function

def scrape_info():
    browser = init_browser()

    # mars news scraping

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    categories = soup.find('ul', class_='item_list').find_all('li')

    titles_list = []
    paragraphs_list = []

    for category in categories:
        title = category.find('h3')
        titles_list.append(title.text)
        paragraph = category.find('div', class_="rollover_description_inner")
        paragraphs_list.append(paragraph.text)
    
    news_title = titles_list[0]
    news_p = paragraphs_list[0]

    print(f'Title: {news_title}, Paragraph: {news_p}')

    # Mars featured image scraping

    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    url_2_short = 'https://www.jpl.nasa.gov/'

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    image_url = soup.find('div', class_='carousel_items').find('article')['style']
    
    image = image_url.split()
    image = image[1]
    image = image.split("'")
    featured_image_url = image[1]
    mars_img = url_2_short + featured_image_url

    # Mars weather twitter scrape

    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').contents[0]
    mars_weather

    # Mars facts table scrape using pandas

    url_4 = 'https://space-facts.com/mars/'
    browser.visit(url_4)

    tables = pd.read_html(url_4)
    tables

    df = tables[1]
    df = df.set_index(df[0])
    df = df.drop([0], axis = 1)
    df = df.rename(columns={1: "Value"})
    df.index.name='Description'
    df

    html_table = df.to_html(classes="table table-stripped")
    html_table
    print(html_table)

    # Mars hemisphere enhanced image scrape

    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)

    hemis = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere',
        'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']
    
    hemisphere_titles = []

    for name in hemis:
        browser.visit(url_5)
        browser.click_link_by_partial_text(f'{name} Enhanced')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('ul').find('li').find('a')['href']
        img_url = f"{img_url}"
        hemisphere_titles.append({"title": name, "img_url": img_url})
        
    cerb = hemisphere_titles[0]['img_url']
    schia = hemisphere_titles[1]['img_url']
    syrt = hemisphere_titles[2]['img_url']
    val = hemisphere_titles[3]['img_url']

    # Building final dictionary to be sent to Mongo


    mars_data = {
        "Title_1": news_title,
        "Paragraph_1": news_p,
        "featured_image": mars_img, 
        "mars_weather_3": mars_weather,
        "mars_table_4": html_table, 
        "cerb_image": cerb,
        "schia_image": schia,
        "syrt_image": syrt,
        "val_image": val
        }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data