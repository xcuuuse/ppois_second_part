from sqlalchemy import or_, select, delete, func
from .database import Session
from .player import Player
from typing import List


class PlayerRepository:
    def __init__(self):
        self.session = Session()

    def add(self, player: Player):
        self.session.add(player)
        self.session.commit()

    def add_many(self, players: List[Player]):
        self.session.add_all(players)
        self.session.commit()

    def search_by_name_date(self, last_name=None, first_name=None, patronymic=None, birth_date=None):
        query = select(Player)
        if birth_date:
            query = query.where(Player.birth_date == birth_date)
        results = self.session.scalars(query).all()
        if last_name:
            results = [result for result in results if last_name.lower() in result.last_name.lower()]
        if first_name:
            results = [result for result in results if first_name.lower() in result.first_name.lower()]
        if patronymic:
            results = [result for result in results if patronymic.lower() in result.patronymic.lower()]
        return results

    def search_by_position_or_squad(self, position=None, squad=None):
        conditions = []
        query = select(Player)
        if position:
            conditions.append(Player.position == position)
        if squad:
            conditions.append(Player.squad == squad)
        if conditions:
            query = query.where(or_(*conditions))
        return self.session.scalars(query).all()

    def search_by_team_or_city(self, team=None, city=None):
        conditions = []
        query = select(Player)
        if team:
            conditions.append(Player.team == team)
        if city:
            conditions.append(Player.city == city)
        if conditions:
            query = query.where(or_(*conditions))
        return self.session.scalars(query).all()

    def delete_by_name_date(self, last_name=None, first_name=None, patronymic=None, birth_date=None):
        query = delete(Player)

        if last_name:
            query = query.where(Player.last_name.ilike(f"%{last_name}%"))
        if first_name:
            query = query.where(Player.first_name.ilike(f"%{first_name}%"))
        if patronymic:
            query = query.where(Player.patronymic.ilike(f"%{patronymic}%"))
        if birth_date:
            query = query.where(Player.birth_date == birth_date)

        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount

    def count(self):
        return self.session.scalar(select(func.count()).select_from(Player))

    def delete_by_position_or_squad(self, position=None, squad=None):
        conditions = []
        query = delete(Player)
        if position:
            conditions.append(Player.position == position)
        if squad:
            conditions.append(Player.squad == squad)
        if conditions:
            query = query.where(or_(*conditions))
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount

    def delete_by_team_or_city(self, team=None, city=None):
        conditions = []
        query = delete(Player)
        if team:
            conditions.append(Player.team == team)
        if city:
            conditions.append(Player.city == city)
        if conditions:
            query = query.where(or_(*conditions))
        result = self.session.execute(query)
        self.session.commit()
        return result.rowcount

    def get_page(self, page, per_page):
        offset = (page - 1) * per_page
        return self.session.scalars(select(Player).offset(offset).limit(per_page)).all()

    def get_all(self):
        return self.session.scalars(select(Player)).all()

    def clear(self):
        self.session.execute(delete(Player))
        self.session.commit()








