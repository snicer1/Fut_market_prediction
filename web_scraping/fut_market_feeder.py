#!/usr/bin/python

import sys
sys.path.append('../')

import logging
import multiprocessing
import time
from web_scraping.data_feed import PlayerFeed
from db.db_conn import create_db_session

domain = 'https://www.futbin.com'
version = 20

if_full_refeed = False

logging.basicConfig(filename=f'log/fut_{time.strftime("%Y%m%d-%H%M%S")}.log',
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    level=logging.DEBUG)

def full_refeed(processes_amount: int):
    feed.clean_tables()
    sites_amount = feed.get_number_of_sites()
    #sites_amount = 110
    site_amount_per_process = sites_amount // processes_amount
    feed_site_from = 1
    feed_site_to = site_amount_per_process + sites_amount % processes_amount

    process_counter = 0
    processes = []
    while process_counter != processes_amount:
        logging.debug(f'feeder started in range: {feed_site_from}: {feed_site_to}')
        p = multiprocessing.Process(target=feed.full_refeed, args=(feed_site_from, feed_site_to))
        p.start()
        processes.append(p)
        feed_site_from = feed_site_to + 1
        feed_site_to += site_amount_per_process
        process_counter += 1

    for process in processes:
        process.join()

def incremental_feed():
    feed.incremental_feed(1)

    return 1

if __name__ == "__main__":
    feed = PlayerFeed(create_db_session(), domain, version)

    if len(sys.argv) == 2:
        try:
            arg_processes_amount = int(sys.argv[1])
            if_full_refeed = True
        except:
            if_full_refeed = False

    if if_full_refeed == True:
        full_refeed(arg_processes_amount)
    else:
        incremental_feed()
