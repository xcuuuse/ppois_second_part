from math import ceil
from src.model.player_repo import PlayerRepository
from src.model.player import Player
from src.model.xml_sax import XMLSax
from src.model.xml_dom import XMLDom
from typing import List


class PlayerController:
    def __init__(self):
        self.__repo = PlayerRepository()
        self.__current_page = 1
        self.__per_page = 10

    def get_total(self):
        return self.__repo.count()

    def get_total_pages(self):
        total = self.get_total()
        return max(1, ceil(total / self.__per_page))

    def get_current_page(self):
        players = self.__repo.get_page(self.__current_page, self.__per_page)
        return players, self.__current_page, self.get_total_pages(), self.get_total()

    def next_page(self):
        if self.__current_page < self.get_total_pages():
            self.__current_page += 1

    def previous_page(self):
        if self.__current_page > 1:
            self.__current_page -= 1

    def first_page(self):
        self.__current_page = 1

    def last_page(self):
        self.__current_page = self.get_total_pages()

    def players_per_page(self, per_page: int):
        self.__per_page = per_page
        self.__current_page = 1 # хз насчет этого

    def add_player_to_database(self, player: Player):
        self.__repo.add(player)

    def add_many_players(self, players: List[Player]):
        self.__repo.add_many(players)

    def search_by_name_date(self, last_name=None, first_name=None, patronymic=None, date=None):
        return self.__repo.search_by_name_date(last_name, first_name, patronymic, date)

    def search_by_team_or_city(self, team=None, city=None):
        return self.__repo.search_by_team_or_city(team, city)

    def search_by_position_or_squad(self, position=None, squad=None):
        return self.__repo.search_by_position_or_squad(position, squad)

    def delete_by_name_date(self, last_name=None, first_name=None, patronymic=None, date=None):
        return self.__repo.delete_by_name_date(last_name, first_name, patronymic, date)

    def delete_by_team_or_city(self, team=None, city=None):
        return self.__repo.delete_by_team_or_city(team, city)

    def delete_by_position_or_squad(self, position=None, squad=None):
        return self.__repo.delete_by_position_or_squad(position, squad)

    def clear_database(self):
        self.__repo.clear()

    def save_to_xml(self, filename: str):
        players = self.__repo.get_all()
        XMLDom.save_to_xml(players, filename)

    def read_from_xml(self, filename):
        players = XMLSax.load_from_xml(filename)
        self.__repo.clear()
        self.__repo.add_many(players)
        self.__current_page = 1
