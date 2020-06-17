import requests
import random
from bs4 import BeautifulSoup

class Proxy_changer():
    def __init__(self):
        self.list_of_proxies = []

    def get_new_list_of_proxies_sslproxies(self):
        url = 'https://www.sslproxies.org/'
        response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        html_soup = BeautifulSoup(response.text, 'html.parser')
        content = html_soup.find('table', id='proxylisttable')

        for row in content.tbody:
            if len(self.list_of_proxies) == 800:
                break

            proxy_all_info = row.find_all('td')
            temp_table = []
            for line in proxy_all_info:
                temp_table.append(line.text)


            self.list_of_proxies.append(f'{temp_table[0]}:{temp_table[1]}')

        return True

    def get_new_list_of_proxies_freeproxy(self):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        html_soup = BeautifulSoup(response.text, 'html.parser')
        content = html_soup.find('table', id='proxylisttable')

        for row in content.tbody:
            if len(self.list_of_proxies) == 80:
                break

            proxy_all_info = row.find_all('td')
            temp_table = []
            for line in proxy_all_info:
                temp_table.append(line.text)

            if temp_table[6] == 'yes':
                self.list_of_proxies.append(f'{temp_table[0]}:{temp_table[1]}')

        return True

    def change_notworking_proxy(self, actual_proxy=''):

        if len(self.list_of_proxies) == 0:
            self.get_new_list_of_proxies_sslproxies()

        number = random.randint(0, len(self.list_of_proxies) - 1)

        new_proxy = self.list_of_proxies[number]


        proxies = {
            "http": f"{new_proxy}",
            "https": f"{new_proxy}",
        }

        return proxies

