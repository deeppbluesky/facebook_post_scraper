
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime
import configparser
import logging
import getopt
import time
import sys
import csv
import json

WAIT_TIMEOUT = 7

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# Configure browser session
wd_options = Options()
wd_options.add_argument("--disable-notifications")
wd_options.add_argument("--disable-infobars")
wd_options.add_argument("--start-maximized")
wd_options.add_argument("--mute-audio")

browser = webdriver.Chrome(chrome_options=wd_options)

def get_by_xpath(driver, xpath):
    """
    Get a web element through the xpath passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param xpath: xpath to use.
    :return: The web element
    """
    return WebDriverWait(driver, WAIT_TIMEOUT).until(
        ec.presence_of_element_located(
            (By.XPATH, xpath)
        ))


def get_by_class_name(driver, class_name):
    """
    Get a web element through the class_name passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param class_name: class_name to use.
    :return: The web element
    """
    return WebDriverWait(driver, WAIT_TIMEOUT).until(
        ec.presence_of_element_located(
            (By.CLASS_NAME, class_name)
        ))

# --------------- Get the date from current post ---------------
def get_date(element):
    try:
        return get_by_xpath(element, ".//abbr").get_attribute("title")
    except:
        return 'None'

# --------------- Write all posts into CSV format ---------------
def write_posts(posts, now):
    # Prep CSV Output File
    csvOut = 'posts_%s.csv' % now.strftime("%Y-%m-%d_%H%M")
    writer = csv.writer(open(csvOut, 'w', encoding="utf-8"))
    writer.writerow(['date', 'title', 'message', 'like', 'love', 'haha', 'wow', 'sad', 'angry', 'comments', 'shares', 'views'])

    # Write friends to CSV File
    for post in posts:
        writer.writerow([post['date'], post['title'], post['message'], post['like'], post['love'], post['haha'], post['wow'], 
        post['sad'], post['angry'], post['comments'], post['shares'], post['views']])

    print("Successfully saved to %s" % csvOut)

# Log in and navigate to group's page
def fb_login(credentials, id_group):
    email = credentials.get('credentials', 'email')
    password = credentials.get('credentials', 'password')
    browser.get('https://www.facebook.com')

    logger.info('Log in - Searching for the email input')
    browser.find_element_by_id('email').send_keys(email)

    logger.info('Log in - Searching for the password input')
    browser.find_element_by_id('pass').send_keys(password)

    logger.info('Log in - Searching for the submit button')
    browser.find_element_by_id('loginbutton').click()

    logger.info('Log in - get the user name')
    user_name = browser.find_element_by_xpath(
        "//div[@class='linkWrap noCount']").text

    # browser.get('https://www.facebook.com/groups/142114343040195/')
    browser.get('https://www.facebook.com/groups/%s/' % id_group)

    logger.info('Log in - Searching the username, which is: %s' % user_name)

# --------------- Scrap all posts ---------------
def scrap_post(credentials, id_group, limit):
  now = datetime.now()
  fb_login(credentials, id_group)

  # Get text from all elements
  posts = []
  end_string = ""
  i = 1
  while(True):
      if(limit):
          if(i > int(limit)):
                break
      print("---------------------------------------------------  Post: ", i)

      # Scroll to bottom
      browser.execute_script(
          "window.scrollTo(0, document.body.scrollHeight);")

      # Trying to get the post
      try:
          element = get_by_xpath( 
              browser, "//div[@class='_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8' or @class='_5pbx userContent _3576'][%i]" % i)      
      except:
          continue
      
      # Get the date from current post
      date = get_date(element)

      # trying to get the reactions for current post
      try:
          title = element.find_element_by_xpath(
              ".//h5[@class='_14f3 _14f5 _5pbw _5vra']").text
      except:
          title = 'None'
      try:
          message = element.find_element_by_xpath(
              ".//div[@class='_5pbx userContent _3ds9 _3576']").text
      except:
          message = 'None'
      try:
          like = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Like') or contains(@aria-label, 'gusta')]").get_attribute("aria-label")
      except:
          like = 'None'
      try:
          love = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Love') or contains(@aria-label, 'encanta')]").get_attribute("aria-label")
      except:
          love = 'None'
      try:
          haha = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Haha') or contains(@aria-label, 'divierte')]").get_attribute("aria-label")
      except:
          haha = 'None'
      try:
          wow = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Wow') or contains(@aria-label, 'asombra')]").get_attribute("aria-label")
      except:
          wow = 'None'
      try:
          sad = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Sad') or contains(@aria-label, 'entristece')]").get_attribute("aria-label")
      except:
          sad = 'None'
      try:
          angry = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Angry') or contains(@aria-label, 'enoja')]").get_attribute("aria-label")
      except:
          angry = 'None'

      # Trying to get the number of comments, shares and views for current post
      try:
          comments = element.find_element_by_xpath(
              ".//div[@class='_ipo']//a[contains(text(), 'comentario') or contains(text(), 'comments')]").text
      except:
          comments = 'None'
      try:
          shares = element.find_element_by_xpath(
              ".//div[@class='_ipo']//a[contains(text(), 'compartido') or contains(text(), 'shares')]").text
      except:
          shares = 'None'
      try:
          views = element.find_element_by_xpath(
              ".//div[@class='_ipo']//a[contains(text(), 'Visto') or contains(text(), 'views')]").text
      except:
          views = 'None'

      # Saving the current post into list of posts
      posts.append({
          'date': date,
          'title': title.encode('utf-8', 'ignore'), #to prevent CSV writing issues
          'message': message.encode('utf-8', 'ignore'),
          'like': like,
          'love': love,
          'haha': haha,
          'wow': wow,
          'sad': sad,
          'angry': angry,
          'comments': comments,
          'shares': shares,
            'views': views
          })
      write_posts(posts, now)    

      # Showing data from current post
      print("Titulo: ", title)
      print("Fecha: ", date)
      print("Mensaje: ", message)
      print("Me gusta: ", like)
      print("Me encanta: ", love)
      print("Me divierte: ", haha)
      print("Me asombra: ", wow)
      print("Me entristece: ", sad)
      print("Me enoja: ", angry)
      print("Comentarios: ", comments)
      print("Compartido: ", shares)
      print("Vistas: ", views)
      i = i+1     

      # Trying if is the end
      try:
          end_string = browser.find_element_by_xpath(
              "//span[@class='fcg' and contains(text(), 'creó el grupo')] | //span[@class='fcg' and contains(text(), 'created the group')]").text
          if("creó el grupo" in end_string):
              break
      except:
          continue

def main(argv):
    filePath = ''
    configPath = ''
    limit = ''
    opts, args = getopt.getopt(argv, "l:c:")
    if opts:
        for o, a in opts:
            if o == "-l":
                limit = a
            if o == "-c":
                configPath = a
    if configPath:
        configObj = configparser.ConfigParser()
        configObj.read(configPath)
        email = configObj.get('credentials', 'email')
        password = configObj.get('credentials', 'password')
        id_group = configObj.get('group', 'id')
        
        scrap_post(configObj, id_group, limit)
    else:
        print('USAGE: ')
        print('python facebook_post_scraper.py -c config.txt')

if __name__ == '__main__':
    main(sys.argv[1:])



