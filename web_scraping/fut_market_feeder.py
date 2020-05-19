import requests
from web_scraping.data_feed import PlayerFeed
from db.db_conn import create_db_session
from datetime import datetime

domain = 'https://www.futbin.com'
version = 20
proxy = "https://35.184.138.182:443"

proxies = {
 "http": "139.180.157.54:8080",
 "https": "139.180.157.54:8080",
}

# url = "https://httpbin.org/ip"
#
# r = requests.get(url, proxies=proxies)
#
# print(r.json())
feed = PlayerFeed(create_db_session(),domain, version)
# feed.get_html_soup('https://www.futbin.com/players?page=2', proxies=feed.get_new_proxy())
# feed.get_html_soup('https://www.futbin.com/players?page=2')
# feed = PlayerFeed(create_db_session(),domain, version, proxy)
#
start_time = datetime.now()
feed.get_number_of_sites()


time_elapsed = datetime.now() - start_time
#
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))