# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Define a function called scrape_all to 1. Initialize the browser; 2. Create a data dictionary; 3. End the WebDriver and return the scraped data.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": img_url,
      "facts": facts,
      "last_modified": timestamp,
      "hemispheres": hemisphere_image_urls
      }
    
    # Stop webdriver and return data
    browser.quit()
    return data

# Defining the function to visit the Mars news website
def mars_news(browser):

    # Screape Mars news
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    slide_elem = news_soup.select_one('div.list_text')

    return news_title, news_p

# Defining the function to visit the JPL Space Images Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add a try//except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Defining the function for Mars Facts
def mars_facts():

    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
      return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


####### NEW #######
# Defining the function for hemispheres
def hemisphere(browser):

    # 1. Use browser to visit the URL 
    url ='https://marshemispheres.com/'
    browser.visit(url + 'index.html')

    # 2. Create a list to hold the images and titles.
    # hemispheres = hemi_soup.find_all("div", class_="item")
    hemisphere_image_urls = []   

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        browser.find_by_css('a.product-item img')[i].click()
        hemi_data = hemipshere_scraping(browser.html)
        hemi_data['img_url'] = url + hemi_data['img_url']
        
        # Append hemisphere list
        hemisphere_image_urls.append(hemi_data)
        browser.back()
    
    return hemisphere_image_urls

def hemipshere_scraping(html_text):
    # Parse html data with soup
    hemi_soup = soup(html_text, 'html.parser')
        
    # Add a try/except for error handling
    try:
        # Find the relative image url
        title_element = hemi_soup.find('h2', class_='title').get_text()
        sample_element = hemi_soup.find('a', text='Sample').get('href')

    except AttributeError:
        title_element = None
        sample_element = None

    hemisphere = {"title": title_element, "img_url": sample_element}

    return hemisphere

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())