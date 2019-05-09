import json
import re
import requests
import time

from bs4 import BeautifulSoup

def get_usernames():

	# Scrapes the MAL recent users page in order to capture usernames
	url = "https://myanimelist.net/users.php"

	page = requests.get(url)
	soup = BeautifulSoup(page.text)
	users = soup.findAll("a", {'href': re.compile(r'\/profile\/.*')})
	
	return users

# Function to clean the HTML table text into a list containing tuples of the format
# (anime_id, watched_percentage, score)
# watched_percentage is calculated as num_watched_episodes / anime_num_episodes
# Note: An unscored anime is calculated as a 0 by MAL

def clean(anime_list):
    cleaned_list = []
    for anime in anime_list:
        anime_id = anime.get('anime_id', None)
        
        num_watched = anime.get('num_watched_episodes', 0)
        num_episodes = anime.get('anime_num_episodes', 1)
        watched_percentage = num_watched / num_episodes
        
        score = anime.get('score', 0)
        
        cleaned_list.append((anime_id, watched_percentage, score))
        
    return cleaned_list

def scrape(user):
	# Skips all of the NavigableStrings
	user_url = "https://myanimelist.net/animelist/" + user.text + "/load.json?status=7&offset=0"
	user_page = requests.get(user_url)
	user_json = json.loads(user_page.text)
      
	anime_list = clean(user_json)
	return anime_list
        			
def main():
	users = get_usernames()
	for user in users:
		if len(user) > 0:
			anime_list = scrape(user)
			#TODO: store the anime lists somehow, database?

if __name__ == '__main__':
	main()
	