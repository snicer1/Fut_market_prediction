from web_scraping.data_feed import PlayerFeed
from db.db_conn import create_db_session
from datetime import datetime

domain = 'https://www.futbin.com'
version = 20

feed = PlayerFeed(create_db_session(),domain, version)

start_time = datetime.now()
feed.full_refeed()
time_elapsed = datetime.now() - start_time

print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))