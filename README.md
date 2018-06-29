# Facebook Post Scraper
This script can scrape posts from a Facebook's group. 
It save a CSV file. It requires Python 3, <a href='http://selenium-python.readthedocs.io/installation.html'>Selenium Webdriver</a> and Chrome browser.

## Installation
You'll need to have python, pip, and [Google Chrome](https://www.google.com/chrome/) installed to use this tool. Once that's all set up:

1. Clone this repository
2. `cd` into the cloned folder 
3. `pip install -r requirements.txt`

## Set up its config.txt file
Fill your email, password of Facebook's profile and Facebook's group ID.
```
[credentials]
email=foo@bar.com
password=secret
[group]
id=675848676543890
```

### Run the script
1. `cd app`
2. Run ```python facebook_post_scraper.py -c config.txt```
3. Optionally you can pass the second parameter that limits the number of posts
   `python facebook_post_scraper.py -c config.txt -l 40`
4. It will open a browser window and will fill your username & password automatically.
5. You should see your Facebook's group page scroll to the bottom.
6. A CSV file will be created with the data (posts_YYYY-MM-DD_HHMM.csv)
