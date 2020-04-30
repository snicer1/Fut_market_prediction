import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, List
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.exc import NoResultFound

class PlayerFeed():
    def __init__(self, session: Session, domain: str, version: int):
        self._session = session
        self.domain = domain
        self.version = version

    @staticmethod
    def format_ingredient(
            id: int,
            name: str,
            carbs: float,
            protein: float,
            fat: float,
            kcal: int,
    ) -> Dict[str, Any]:
        ingredient = {
            "id": id,
            "name": name,
            "carbs": carbs,
            "protein": protein,
            "fat": fat,
            "kcal": kcal,
        }
        return ingredient


    def full_refeed(self):
        page_number_max = 1
        i = page_number_max
        players = {}
        while (i != 0):
            url = f'{self.domain}/{self.version}/players?page={i}'
            print(url)
            response = requests.get(url, headers={'Cache-Control': 'no-cache'})
            html_soup = BeautifulSoup(response.text, 'html.parser')
            players_container = html_soup.find_all('a', class_='player_name_players_table')
            for player in players_container:
                futbin_id = int(player['href'].split("/")[-2])
                name = player.text
                url = self.domain + player['href']
                self.get_players_stat(url)
            i -= 1
        return player

    def get_players_stat(self, url):
        player_stat = {}
