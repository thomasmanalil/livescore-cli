from bs4 import BeautifulSoup
import requests, re, os

#function which returns boolean true if the ping test results positive false if negative test
def check_ping(hostname):
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        return True
    else:
        return False

#main webscrapping code which take the url to scrap and returns the rows of data
def get_livescore(url,scrapping_class):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    _rows = soup.find_all(class_=scrapping_class)
    return _rows
