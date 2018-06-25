
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import logging
import sys
import time
import getopt
import configparser
import json

WAIT_TIMEOUT = 10


def get_by_xpath(driver, xpath):
    """
    Get a web element through the xpath passed by performing a Wait on it.
    :param driver: Selenium web driver to use.
    :param xpath: xpath to use.
    :return: The web element
    """
    return WebDriverWait(driver, 7).until(
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
    return WebDriverWait(driver, 7).until(
        ec.presence_of_element_located(
            (By.CLASS_NAME, class_name)
        ))


def get_date(element):
    # return browser.find_element_by_xpath("./span[@class='']")
    # element.get_attribute("title")
    try:
        return get_by_xpath(element, ".//abbr").get_attribute("title")
    except:
        return None


def check_element(browser, xpath):
    try:
        element = browser.find_element_by_xpath(xpath)
        if(element.is_displayed()):
            return True
        else:
            return False
    except:
        return None


def get_me_gusta(element):
    # return browser.find_element_by_xpath("./span[@class='']")
    # element.get_attribute("title")
    return element.find_element_by_xpath(".//a[@class='_3emk _401_']").get_attribute("ajaxify")

def scrap_post(credentials, url):
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  logger.setLevel(level=logging.DEBUG)

  # Configure browser session
  wd_options = Options()
  wd_options.add_argument("--disable-notifications")
  wd_options.add_argument("--disable-infobars")
  wd_options.add_argument("--mute-audio")

  email = credentials.get('credentials', 'email')
  password = credentials.get('credentials', 'password')

  browser = webdriver.Chrome(chrome_options=wd_options)
  browser.get('https://www.facebook.com')

  logger.info('Log in - Searching for the email input')
  browser.find_element_by_id('email').send_keys(email)

  logger.info('Log in - Searching for the password input')
  browser.find_element_by_id('pass').send_keys(password)

  logger.info('Log in - Searching for the submit button')
  browser.find_element_by_id('loginbutton').click()

  logger.info('Log in - get the user name')
  user_name = browser.find_element_by_xpath(
      "//div[@class='linkWrap noCount']").text  # It works with _2s25 too

  # browser.get('https://www.facebook.com/groups/142114343040195/')
  browser.get('https://www.facebook.com/groups/%s/' %url)

  logger.info('Log in - Saving the username, which is: %s' % user_name)

  # Get text from all elements
  res = []
  end_string = ""
  i = 1
  while(i<=40):
      print("---------------------------------------------------  Post: ", i)
      browser.execute_script(
          "window.scrollTo(0, document.body.scrollHeight);")
      element = get_by_xpath(
          browser, "//div[@class='_4-u2 mbm _4mrt _5jmm _5pat _5v3q _4-u8' or @class='_5pbx userContent _3576'][%i]" % i)      
      # res.append(element)
      date = get_date(element)
      # me_gusta = get_me_gusta(element)
      try:
          title = element.find_element_by_xpath(
              ".//h5[@class='_14f3 _14f5 _5pbw _5vra']").text
      except:
          title = None
      try:
          message = element.find_element_by_xpath(
              ".//div[@class='_5pbx userContent _3ds9 _3576']").text
      except:
          message = None
      try:
          like = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Like') or contains(@aria-label, 'gusta')]").get_attribute("aria-label")
      except:
          like = None
      try:
          love = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Love') or contains(@aria-label, 'encanta')]").get_attribute("aria-label")
      except:
          love = None
      try:
          haha = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Haha') or contains(@aria-label, 'divierte')]").get_attribute("aria-label")
      except:
          haha = None
      try:
          wow = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Wow') or contains(@aria-label, 'asombra')]").get_attribute("aria-label")
      except:
          wow = None
      try:
          sad = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Sad') or contains(@aria-label, 'entristece')]").get_attribute("aria-label")
      except:
          sad = None
      try:
          angry = element.find_element_by_xpath(
              ".//div[@class='_3t53 _4ar- _ipn']/span[@class='_3t54']/a[contains(@aria-label, 'Angry') or contains(@aria-label, 'enoja')]").get_attribute("aria-label")
      except:
          angry = None
      try:
          comments = element.find_element_by_xpath(
              ".//div[@class='_ipo']//a[contains(text(), 'comentario') or contains(text(), 'comments')]").text
      except:
          comments = None
      try:
          shares = element.find_element_by_xpath(
              ".//div[@class='_ipo']//a[contains(text(), 'compartido') or contains(text(), 'shares')]").text
      except:
          shares = None
      try:
          views = element.find_element_by_xpath(
              ".//div[@class='_ipo']//a[contains(text(), 'Visto') or contains(text(), 'views')]").text
      except:
          views = None

      print("Titulo: ", title)
      print("Mensaje: ", message)
      print("Me gusta: ", like)
      print("Me entristece: ", love)
      print("Me divierte: ", haha)
      print("Me asombra: ", wow)
      print("Me entristece: ", sad)
      print("Me enoja: ", angry)
      print("Comentarios: ", comments)
      print("Compartido: ", shares)
      print("Vistas: ", views)
      i = i+1
      print("Fecha: ", date)

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
    opts, args = getopt.getopt(argv, "i:c:")
    if opts:
        for o, a in opts:
            if o == "-i":
                url = a
            if o == "-c":
                configPath = a
    if url and configPath:
        configObj = configparser.ConfigParser()
        configObj.read(configPath)
        email = configObj.get('credentials', 'email')
        password = configObj.get('credentials', 'password')
        # posts = scrap_post(credentials, url)
        scrap_post(configObj, url)
        # print((json.dumps(posts)))
    else:
        print('USAGE: ')
        print('facebook_post_scraper.py -c config.txt -i <ID GROUP\'S HERE>')

if __name__ == '__main__':
    main(sys.argv[1:])



