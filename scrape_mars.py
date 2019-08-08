# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

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

    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    image_url = soup.find('div', class_='carousel_items').find('article')['style']
    
    image = image_url.split()
    image = image[1]
    image = image.split("'")
    featured_image_url = image[1]
    featured_image_url

    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').contents[0]
    mars_weather

    url_4 = 'https://space-facts.com/mars/'
    browser.visit(url_4)

    tables = pd.read_html(url_4)
    tables

    df = tables[1]
    df = df.transpose()
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    df

    html_table = df.to_html()
    html_table

    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)

    hemis = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere',
        'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']
    
    hemisphare_titles = []

    for name in hemis:
        browser.visit(url_5)
        browser.click_link_by_partial_text(f'{name} Enhanced')
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('ul').find('li').find('a')['href']
        img_url = f"{img_url}"
        #hemisphare_titles.append({f"title\": \"{name}\", \"img_url\": \"{img_url}\""})
        hemisphare_titles.append({"title": name, "img_url": img_url})
        
    hemisphare_titles

    mars_data = {f'Title_1: {news_title}, Paragraph_1: {news_p}, 
    featured_image_url_2: {featured_image_url}, mars_weather_3: {mars_weather},
    mars_table_4: {tables}, mars_table_4: {html_table},
    mars_titles_5: {hemisphare_titles}'}