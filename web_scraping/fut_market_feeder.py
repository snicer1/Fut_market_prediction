from web_scraping.data_feed import PlayerFeed

domain = 'https://www.futbin.com'
version = 20

feed = PlayerFeed(domain, version)
feed.full_refeed()