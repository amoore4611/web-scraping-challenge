#imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

#scrape all function
def scrape_all():
    #set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # the goal is to return a json that has all the necessary data, so taht it can be loaded into MongoDB

    #the goal is to return a json that has all of the necessary data, so that it can be loaded into MongoDB

    #get the information from the news page
    news_title, news_p = scrape_news(browser)

    #build the dictionary using the information from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_p,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    #stop the webdriver 
    browser.quit()

    #display output
    return marsData

#scrape the mars news page
def scrape_news(browser):
    # go to the Mars NASA news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')

    slide_elm = nasa_soup.select_one('div.list_text')
    #grabs the title
    result = nasa_soup.find('div', class_='content_title')
    news_title = result.get_text()

    #grabs the paragraph for the headline
    p = nasa_soup.find('div', class_='article_teaser_body')
    news_p = p.get_text()

    #return the title and the paragraphs
    return news_title, news_p

#scrape through the featured image page
def scrape_feature_img(browser):
    # URL of Mars Space Image page to be scraped
    space_url = 'https://spaceimages-mars.com/'
    browser.visit(space_url)

    #find and click the full image button
    mars_image_link = browser.find_by_tag('button')[1]
    mars_image_link.click()

    # Parse HTML with Beautiful Soup
    html = browser.html
    mars_image_soup = bs(html, 'html.parser')

    #find the image url
    mars_image_rel = mars_image_soup.find('img', class_ = 'fancybox-image').get('src')

    #Use the base url to create am absolute url
    mars_image_url = f'https://spaceimages-mars.com/{mars_image_rel}'

    #return the image URL
    return mars_image_url

#scrape through the facts page
def scrape_facts_page(browser):
    #vist URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    #parse the resulting html with soup
    html = browser.html
    fact_soup = bs(html, 'html.parser')

    #find the facts location
    factslocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factslocation.find('table') #grab the html code for the fact table

    #create an empty string
    facts = ""

    #add the text to the empty string and then return 
    facts += str(factTable)

    return facts


#scrape through the hemispheres pages
def scrape_hemispheres(browser):
    #base url
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)

    #Create a list to hold images and titles
    hemispheres_image_urls = []

    #set up the loop
    for i in range(4):
        #loops through each of the pages
        #hemisphere info dictionary 
        hemisphere_info = {}
        browser.find_by_css('a.product-item img')[i].click()
        #find the sample anchor tag and extract the href
        sample_anchor = browser.links.find_by_text('Sample').first
        hemisphere_info["img_url"] = sample_anchor['href']
        #get the hemisphere titles
        hemisphere_info["title"] = browser.find_by_css('h2.title').text
        #append urls to list
        hemispheres_image_urls.append(hemisphere_info)

        #navigate back to homepage
        browser.back()

    #return the hemispheres url with the titles
    return hemispheres_image_urls

#set up as a flask app
if __name__ == "__main__":
    print(scrape_all())