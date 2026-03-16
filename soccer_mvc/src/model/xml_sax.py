import xml.sax
from datetime import date
from .player import Player


class PlayerHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.players = []
        self.current_player = {}
        self.current_tag = ""

    def startElement(self, name: str, attrs):
        self.current_tag = name
        if name == "player":
            self.current_player = {}

    def characters(self, content):
        content = content.strip()
        if not content:
            return
        if self.current_tag in ("last_name", "first_name", "patronymic", "team", "city", "squad", "position"):
            self.current_player[self.current_tag] = content
        elif self.current_tag == "birth_date":
            self.current_player["birth_date"] = date.fromisoformat(content)

    def endElement(self, name):
        if name == "player":
            self.players.append(Player(
                last_name=self.current_player.get("last_name"),
                first_name=self.current_player.get("first_name"),
                patronymic=self.current_player.get("patronymic") or None,
                birth_date=self.current_player.get("birth_date"),
                team=self.current_player.get("team"),
                city=self.current_player.get("city"),
                squad=self.current_player.get("squad"),
                position=self.current_player.get("position")))
        self.current_tag = ""


class XMLSax:
    @staticmethod
    def load_from_xml(filename: str):
        handler = PlayerHandler()
        xml.sax.parse(filename, handler)
        return handler.players
