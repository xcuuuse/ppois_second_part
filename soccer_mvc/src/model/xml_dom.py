import xml.dom.minidom as minidom
from .player import Player


class XMLDom:
    @staticmethod
    def save_to_xml(players: list[Player], filename: str):
        doc = minidom.getDOMImplementation().createDocument(None, "players", None)
        root = doc.documentElement

        for player in players:
            player_el = doc.createElement("player")

            fields = {
                "last_name": player.last_name,
                "first_name": player.first_name,
                "patronymic": player.patronymic or "",
                "birth_date": player.birth_date.isoformat(),
                "team": player.team,
                "city": player.city,
                "squad": player.squad,
                "position": player.position
            }

            for key, value in fields.items():
                element = doc.createElement(key)
                element.appendChild(doc.createTextNode(value))
                player_el.appendChild(element)

            root.appendChild(player_el)

        with open(filename, "w", encoding="utf-8") as file:
            doc.writexml(file, indent="  ", addindent="  ", newl="\n")
