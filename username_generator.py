import requests
import re
from bs4 import BeautifulSoup

url = "https://myanimelist.net/users.php"

page = requests.get(url)
soup = BeautifulSoup(page.text)
users = soup.findAll("a", {'href': re.compile(r'\/profile\/.*')})

for user in users:
    if len(user.text) > 0:
        print(user.text)