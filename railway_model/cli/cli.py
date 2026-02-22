import argparse
import sys
from exceptions import exceptions
from pathlib import Path
from railway.route import Route, Station, Railway
from management.serializer import Serializer
from management.locomotive_manager import LocomotiveManager
from compound.compound import Compound, Locomotive, Coach


def create_compound(locomotive_number: int, coach_amount: int, seats=10, price=25):
    locomotive = Locomotive(locomotive_number)
    coaches = [Coach(number=i+1, seats_amount=seats, seat_price=price)for i in range(coach_amount)]
    return Compound(locomotive, coaches)


def create_default_compound():
    locomotive = Locomotive(1)
    coaches = [
        Coach(number=1, seats_amount=5, seat_price=25),
        Coach(number=2, seats_amount=4, seat_price=45)
    ]
    compound = Compound(locomotive, coaches)

    return compound


def free_compound(compound: Compound):
    for i in compound.coaches:
        i.free_seat([i for i in range(len(i.seats.keys()))])


def create_default_route():
    return Route([
        Railway({Station("A"), Station("B")}, 100),
        Railway({Station("B"), Station("C")}, 100),
        Railway({Station("C"), Station("D")}, 100),
        Railway({Station("D"), Station("E")}, 100),
        Railway({Station("E"), Station("F")}, 100),
        Railway({Station("F"), Station("G")}, 100)
    ])


def cli():
    parser = argparse.ArgumentParser("Railway model", "railway-cli")
    subparsers = parser.add_subparsers(dest="command", help="available commands")

    subparsers.add_parser("state", help="Show train's current state")
    move_parser = subparsers.add_parser("move", help="Move along the route")
    move_parser.add_argument("steps", type=int, nargs="?",
                             default=1, help="Number of stations to move (default: 1)")

    book_parser = subparsers.add_parser("book", help="Book a seat")
    book_parser.add_argument("coach", type=int, help="Coach number")
    book_parser.add_argument("seat", type=int, help="Seat number")
    book_parser.add_argument("pass_id", type=int, help="Passenger id")

    save_parser = subparsers.add_parser("save", help="Save state")
    save_parser.add_argument("--file", type=str, default=Serializer.STATE_FILE,
                             help="File to save to")

    service_parser = subparsers.add_parser("service", help="Service the compound")
    service_parser.add_argument("number", type=int, help="Compound ID")
    subparsers.add_parser("exit", help="Exit")
    args = parser.parse_args()

    compound = None
    state_path = Path(args.file if hasattr(args, "file") else Serializer.STATE_FILE)

    try:
        try:
            compound = Serializer.load(str(state_path))
            print(f"Loaded from {state_path}")
        except FileNotFoundError:
            print(f"The state is not found")
            compound = create_default_compound()
            print(f"Created new compound(id = {compound.compound_id}")

        if not args.command:
            parser.print_help()
            return 0

        route = create_default_route()
        match args.command:
            case "state":
                print("\n Current state ")
                print(f"Compound ID: {compound.compound_id}")
                if compound.current_pos < len(route.stations):
                    print(f"Pos: {compound.current_pos} ({route.stations[compound.current_pos].name})")
                else:
                    print("Pos: The route is completed")
                print(f"State: {compound.state.name}")
                print("\nCoaches:")
                for coach in compound.coaches:
                    free = len(coach.free_seats)
                    print(f"  Coach {coach.number} (price: {coach.seat_price}): {free}/{len(coach.seats)} free seats")

            case "move":
                print(f"\nMoving to {args.steps} stations forward")
                for _ in range(args.steps):
                    if compound.current_pos < len(route.stations):
                        compound.move_along_route(route)
                    else:
                        print("The route is completed")
                        break
            case "book":
                try:
                    compound.coaches[args.coach - 1].occupy_seat(args.seat, args.pass_id)
                    print(f"Место {args.seat} в вагоне {args.coach} забронировано для пассажира {args.pass_id}")
                except IndexError:
                    print(f"Ошибка: вагон {args.coach} не существует")
                except Exception as e:
                    print(f"Ошибка бронирования: {str(e)}")

            case "save":
                saved_path = Serializer.save(compound, str(state_path))
                print(f"Состояние сохранено вручную в {saved_path}")

            case "service":
                print('g')

            case "exit":
                print("Завершаем работу...")
                return 0

            case _:
                parser.print_help()
                return 1

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return 1

    finally:
        if compound is not None and args.command != "save":
            saved_path = Serializer.save(compound, str(state_path))
            print(f"Состояние автоматически сохранено в {saved_path}")