from .database import Session
from .player import Player
from .player_repo import PlayerRepository
from datetime import date

repo = PlayerRepository()

# очищаем перед тестом
repo.clear()

# добавляем тестовых игроков
players = [
    Player(last_name="Иванов", first_name="Иван", patronymic="Иванович",
           birth_date=date(1990, 5, 20), team="Спартак", city="Москва",
           squad="основной", position="нападающий"),
    Player(last_name="Петров", first_name="Петр", patronymic=None,
           birth_date=date(1995, 3, 15), team="ЦСКА", city="Москва",
           squad="резерв", position="защитник"),
    Player(last_name="Сидоров", first_name="Алексей", patronymic="Петрович",
           birth_date=date(1988, 7, 1), team="Зенит", city="Санкт-Петербург",
           squad="основной", position="вратарь"),
]
repo.add_many(players)
print("Добавлено:", len(repo.get_all()))

# поиск по фамилии
result = repo.search_by_name_date(last_name="иван")
print("Поиск по 'иван':", [p.last_name for p in result])

# поиск по дате
result = repo.search_by_name_date(birth_date=date(1990, 5, 20))
print("Поиск по дате:", [p.last_name for p in result])

# поиск по позиции или составу
result = repo.search_by_position_or_squad(position="вратарь")
print("Поиск вратарей:", [p.last_name for p in result])

result = repo.search_by_position_or_squad(squad="основной")
print("Поиск основного состава:", [p.last_name for p in result])

# поиск по команде или городу
result = repo.search_by_team_or_city(city="Москва")
print("Поиск по Москве:", [p.last_name for p in result])

# пагинация
result = repo.get_page(page=1, per_page=2)
print("Страница 1 (по 2):", [p.last_name for p in result])

result = repo.get_page(page=2, per_page=2)
print("Страница 2 (по 2):", [p.last_name for p in result])

# удаление
deleted = repo.delete_by_position_or_squad(squad="резерв")
print("Удалено из резерва:", deleted)
print("Осталось:", len(repo.get_all()))