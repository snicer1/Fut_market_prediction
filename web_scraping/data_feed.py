from requests import request
from bs4 import BeautifulSoup
from typing import Any, Dict
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import exc
from market_prediction import models
from web_scraping import proxy_changer

class PlayerFeed():
    def __init__(self, session: Session, domain: str, version: int):
        self._session = session
        self.domain = domain
        self.version = version
        self.headers = {'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'User-Agent': 'Mozilla/5.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Referer': 'http://www.wikipedia.org/',
                        'Connection': 'keep-alive',}

    @staticmethod
    def format_player(
            futbin_id: int, name: str, player_id: int, position: str, age: int, club: str, nation: str, league: str, rating: int, level: str, skills: int,
            weak_foot: int,revision: str,foot: str, height: int, weight: int, def_wr: str, att_wr: str, added_on: str,
    ) -> Dict[str, Any]:
        player = {"futbin_id": futbin_id, "name": name, "player_id": player_id, "position": position, "age": age, "club": club, "nation": nation, "league": league, "rating": rating,"level": level,
                      "skills": skills, "weak_foot": weak_foot, "revision": revision, "foot": foot, "height": height, "weight": weight, "def_wr": def_wr, "att_wr": att_wr, "added_on": added_on,
        }
        return player

    @staticmethod
    def format_player_stats(
            futbin_id: int, pace: int,pace_acceleration: int, pace_sprintspeed: int, shooting: int, shooting_positioning: int,
            shooting_finishing: int, shooting_shotpower: int,shooting_longshots: int, shooting_volleys: int, shooting_penalties: int, passing: int, passing_vision: int, passing_crossing: int,
            passing_fkaccurancy: int,passing_shortpassing: int,passing_longpassing: int, passing_curve: int, dribbling: int, dribbling_agility: int, dribbling_balance: int, dribbling_reactions: int,
            dribbling_ballcontrol: int, dribbling_dribbling: int, dribbling_composure: int, defending: int, defending_interceptions: int, defending_headingaccuramcy: int, defending_defawareness: int,
            defending_standingtackle: int,defending_slidingtackle: int, physicality: int, physicality_jumping: int, physicality_stamina: int, physicality_strength: int, physicality_aggression: int,

    ) -> Dict[str, Any]:
        player_stats = {"futbin_id":futbin_id, "pace": pace, "pace_acceleration": pace_acceleration,"pace_sprintspeed": pace_sprintspeed,"shooting": shooting,
                        "shooting_positioning": shooting_positioning,"shooting_finishing": shooting_finishing,"shooting_shotpower": shooting_shotpower,"shooting_longshots": shooting_longshots,
                        "shooting_volleys": shooting_volleys,"shooting_penalties": shooting_penalties, "passing": passing,"passing_vision": passing_vision,"passing_crossing": passing_crossing,
                        "passing_fkaccurancy": passing_fkaccurancy,"passing_shortpassing": passing_shortpassing,"passing_longpassing": passing_longpassing,"passing_curve": passing_curve,
                        "dribbling": dribbling, "dribbling_agility": dribbling_agility, "dribbling_balance": dribbling_balance, "dribbling_reactions": dribbling_reactions,
                        "dribbling_ballcontrol": dribbling_ballcontrol,"dribbling_dribbling": dribbling_dribbling,"dribbling_composure": dribbling_composure,
                        "defending": defending, "defending_interceptions": defending_interceptions,"defending_headingaccuramcy": defending_headingaccuramcy,"defending_defawareness": defending_defawareness,
                        "defending_standingtackle": defending_standingtackle,"defending_slidingtackle": defending_slidingtackle,"physicality": physicality,
                        "physicality_jumping": physicality_jumping, "physicality_stamina": physicality_stamina,"physicality_strength": physicality_strength,"physicality_aggression": physicality_aggression,
                  }
        return player_stats

    @staticmethod
    def format_player_price(player_id: int, price: int, date_price: str,) -> Dict[str, Any]:
        player_price = {"player_id": player_id, "price": price, "date_price": date_price}
        return player_price

    def get_number_of_sites(self):
        page_number_max = 1
        url = f"{self.domain}/{self.version}/players"

        try:
            r = request(method='get', url=url,  headers=self.headers, timeout=8)
            html_soup = BeautifulSoup(r.text, 'html.parser')
            pages = html_soup.find_all('li', class_="page-item")
        except:
            print("Cannot find page_number_max")

        list_element = []

        for item in pages:
            list_element.append(item.text.replace("\n", ""))

        try:
            page_number_max = int(list_element[-2])
        except:
            print("Cannot find page_number_max")

        return page_number_max

    def clean_tables(self):
        try:
            self._session.execute(models.Player_stat.__table__.delete())
            self._session.execute(models.Player.__table__.delete())
            self._session.commit()
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)
            return False

        return True

    def full_refeed(self, feed_site_from, feed_site_to):
        proxy_handler = proxy_changer.Proxy_changer()
        proxies = proxy_handler.change_notworking_proxy()
        print(f'full_refeed in range: {feed_site_from}: {feed_site_to}')
        i = (feed_site_to - feed_site_from) + 1
        while (i != 0):
            player = []
            player_stat = []
            player_prices = []
            # print(f"I AM ON PAGE {feed_site_to + 1 - i}")
            # start_time = datetime.now()

            url = f'{self.domain}/{self.version}/players?page={feed_site_to + 1 - i}'

            players_container = []
            while players_container is None or len(players_container) == 0:
                try:
                    r = request(method='get', url=url, proxies=proxies, headers=self.headers, timeout=8)
                    if r.status_code == 403:
                        raise Exception
                    html_soup = BeautifulSoup(r.text, 'html.parser')
                    players_container = html_soup.find_all('a', class_='player_name_players_table')
                except:
                    proxies = proxy_handler.change_notworking_proxy(proxies)
                    continue

            for elem in players_container:
                futbin_id = int(elem['href'].split("/")[-2])
                name = elem.text
                url = self.domain + elem['href']
                info_content = []
                while info_content is None or len(info_content) == 0:
                    try:
                        r = request(method='get', url=url, proxies=proxies, headers=self.headers, timeout=8)
                        if r.status_code == 403:
                            raise Exception
                        html_soup = BeautifulSoup(r.text, 'html.parser')
                        info_content = html_soup.find('div', id='info_content')
                    except:
                        proxies = proxy_handler.change_notworking_proxy(proxies)
                        continue

                single_player_info, player_id = self.get_players_info(html_soup, futbin_id, name)
                if len(single_player_info) > 0:
                    player.append(single_player_info)
                else:
                    continue

                player_single_price = False

                while not player_single_price:
                    try:
                        player_single_price = self.get_player_prices(player_id, proxies)
                    except ValueError:
                        proxies = proxy_handler.change_notworking_proxy(proxies)
                        continue

                player_prices += player_single_price

                single_player_stat = self.get_players_stats(html_soup,futbin_id)
                if len(single_player_stat) > 0:
                    player_stat.append(single_player_stat)
                else:
                    continue


            try:
                self._session.execute(models.Player.__table__.insert(), player)
                self._session.commit()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print(error)

            try:
                self._session.execute(models.Player_price.__table__.insert(), player_prices)
                self._session.commit()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print(error)

            try:
                self._session.execute(models.Player_stat.__table__.insert(), player_stat)
                self._session.commit()
            except exc.SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                print(error)

            # time_elapsed = datetime.now() - start_time
            # print('Time of database insertion (hh:mm:ss.ms) {}'.format(time_elapsed))

            i -= 1
        return 1

    def incremental_feed(self, date_refeed_from):
        proxy_handler = proxy_changer.Proxy_changer()
        proxies = proxy_handler.change_notworking_proxy()
        url = f'{self.domain}/latest'
        r = request(method='get', url=url, headers=self.headers, timeout=8)
        html_soup = BeautifulSoup(r.text, 'html.parser')
        players_container = html_soup.find('tr', class_='player_tr_1')
        temp = players_container.find_all('td')
        table_with_content = []
        for elem in temp:
            table_with_content.append(elem.text.strip())
        print(table_with_content[-1])
        return 1

    def get_players_info(self, html_soup, futbin_id, name):
        can_be_inserted = True
        temp_list_player_info = []
        info_content = html_soup.find('div', id='info_content')
        player_info = info_content.find_all('td', class_='table-row-text')

        for elem in player_info:
            temp_list_player_info.append(elem.text.strip())

        player_id = int(html_soup.find("div", id= "page-info")['data-player-resource'])
        position = html_soup.find('div', class_='pcdisplay-pos').text
        age = int(temp_list_player_info[17][:2])
        club = temp_list_player_info[1]
        nation = temp_list_player_info[2]
        league = temp_list_player_info[3]
        rating = int(html_soup.find('div', class_='pcdisplay-rat').text)
        level = html_soup.find('div', id='Player-card')['data-level']
        skills = int(temp_list_player_info[4])
        weak_foot = int(temp_list_player_info[5])
        revision = temp_list_player_info[10]
        foot = temp_list_player_info[7]
        height = int(temp_list_player_info[8][:3])
        weight = int(temp_list_player_info[9])
        def_wr = temp_list_player_info[11]
        att_wr = temp_list_player_info[12]
        added_on = temp_list_player_info[13]

        player = ''

        if position == 'GK':
            can_be_inserted = False
        if can_be_inserted == True:
            player = self.format_player(futbin_id=futbin_id, name=name, player_id=player_id, position=position, age=age, club=club, nation=nation, league=league, rating=rating, level=level,
                                    skills=skills, weak_foot=weak_foot, revision=revision, foot=foot, height=height, weight=weight, def_wr=def_wr, att_wr=att_wr, added_on=added_on
                                    )

        return player, player_id

    def get_players_stats(self, html_soup, futbin_id):
        can_be_inserted = True
        temp_list_player_stat = []

        stat_content_sub = html_soup.find_all("div", {"class": ["row_sep_main", "sub_stat"]})

        for elem in stat_content_sub:
            try:
                temp_list_player_stat.append(int(elem.text.strip()[-2:]))
            except:
                print(f'Cannot find some of statistics of player with futbin_id = {futbin_id}')
                can_be_inserted = False

        player_stats = ''

        if can_be_inserted == True:
            player_stats = self.format_player_stats(futbin_id = futbin_id, pace = temp_list_player_stat[0]
                                                , pace_acceleration = temp_list_player_stat[1], pace_sprintspeed = temp_list_player_stat[2], shooting = temp_list_player_stat[3]
                                                , shooting_positioning = temp_list_player_stat[4], shooting_finishing = temp_list_player_stat[5]
                                                , shooting_shotpower = temp_list_player_stat[6],shooting_longshots = temp_list_player_stat[7]
                                                , shooting_volleys = temp_list_player_stat[8], shooting_penalties = temp_list_player_stat[9],  passing = temp_list_player_stat[10]
                                                , passing_vision = temp_list_player_stat[11], passing_crossing = temp_list_player_stat[12], passing_fkaccurancy = temp_list_player_stat[13]
                                                , passing_shortpassing = temp_list_player_stat[14], passing_longpassing = temp_list_player_stat[15], passing_curve = temp_list_player_stat[16]
                                                , dribbling = temp_list_player_stat[17], dribbling_agility = temp_list_player_stat[18], dribbling_balance = temp_list_player_stat[19]
                                                , dribbling_reactions = temp_list_player_stat[20], dribbling_ballcontrol = temp_list_player_stat[21]
                                                , dribbling_dribbling = temp_list_player_stat[22], dribbling_composure = temp_list_player_stat[23], defending = temp_list_player_stat[24]
                                                , defending_interceptions = temp_list_player_stat[25], defending_headingaccuramcy = temp_list_player_stat[26]
                                                , defending_defawareness = temp_list_player_stat[27] ,defending_standingtackle = temp_list_player_stat[28]
                                                , defending_slidingtackle = temp_list_player_stat[29], physicality = temp_list_player_stat[30], physicality_jumping = temp_list_player_stat[31]
                                                , physicality_stamina = temp_list_player_stat[32], physicality_strength = temp_list_player_stat[33]
                                                , physicality_aggression = temp_list_player_stat[34])

        return player_stats

    def get_player_prices(self, player_id, proxies):
        player_price = []
        url = f'{self.domain}/{self.version}/playerGraph?type=daily_graph&year=20&player={player_id}'
        try:
            r = request(method='get', url=url, proxies=proxies, headers=self.headers, timeout=8)
            data = r.json()
            if r.status_code == 403:
                raise Exception
        except:
            raise ValueError

        if len(data) == 0:
            raise ValueError

        for price in data['ps']:
            # There is extra zeroes in response.
            date = datetime.utcfromtimestamp(price[0] / 1000).strftime('%Y-%m-%d')
            price = price[1]

            player_price.append(self.format_player_price(player_id=player_id, price = price, date_price=date))

        return player_price