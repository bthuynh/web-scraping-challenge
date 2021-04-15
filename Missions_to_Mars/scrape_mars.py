import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    """ Mars News """
    browser = init_browser()
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(1)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    news_title = news_soup.find('div', class_="content_title").get_text()
    news_paragraph = news_soup.find('div', class_="article_teaser_body").get_text()
    browser.quit()
    print(f'News Title: {news_title}\nNews Paragraph: {news_paragraph}')

    """ JPL Mars Space Images - Featured Image """
    browser = init_browser()
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)
    time.sleep(1)
    browser.click_link_by_partial_text("FULL IMAGE")
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    image_url = image_soup.find('img', class_="headerimage fade-in").get("src")
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_url}'
    browser.quit()
    print(featured_image_url)

    """ Mars Facts """
    facts_url = "https://space-facts.com/mars/"
    facts_tables = pd.read_html(facts_url)
    mars_facts_df = facts_tables[1]
    mars_facts_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    mars_facts = mars_facts_df.to_html(header=True, index=True)
    browser.quit()

    """ Mars Hemispheres """
    browser = init_browser()
    astrogeo_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeo_url)
    time.sleep(1)

    hemi_image_urls = []
    links = browser.find_by_css("a.product-item h3")

    for hemi in range(len(links)):
        hemisphere_data = {}
        browser.find_by_css("a.product-item h3")[hemi].click()
        hemi_title = hemisphere_data["title"] = browser.find_by_css("h2.title").text
        sample_element = browser.links.find_by_text("Sample").first
        hemi_url = hemisphere_data["img_url"] = sample_element["href"]
        hemi_image_urls.append(hemisphere_data)
        browser.back()
        print(f'Hemi Title: {hemi_title}\nHemi Image URL: {hemi_url}')

    browser.quit()

    """ MongoDB Mars Data Dictionary"""
    mars_data = {
    'news_title': news_title,
    'news_paragraph': news_paragraph,
    'featured_image_url': featured_image_url,
    'mars_facts': mars_facts,
    'hemisphere_image_urls': hemi_image_urls,
    }
    
    browser.quit()
    return mars_data