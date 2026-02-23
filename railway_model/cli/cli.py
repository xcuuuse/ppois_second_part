import argparse
import sys
from exceptions import exceptions
from pathlib import Path
from railway.route import Route, Station, Railway
from management.serializer import Serializer
from management.locomotive_manager import LocomotiveManager
from compound.compound import Compound, Locomotive, Coach
from management.timetable import Timetable, TimetableCell


class Cli:
    @staticmethod
    def __create_compound(locomotive_number: int, coach_amount: int, seats=10, price=25):
        locomotive = Locomotive(locomotive_number)
        coaches = [Coach(number=i+1, seats_amount=seats, seat_price=price)for i in range(coach_amount)]
        return Compound(locomotive, coaches)

    @staticmethod
    def __create_default_compound():
        locomotive = Locomotive(1)
        coaches = [
            Coach(number=1, seats_amount=5, seat_price=25),
            Coach(number=2, seats_amount=4, seat_price=45)
        ]
        compound = Compound(locomotive, coaches)

        return compound

    @staticmethod
    def __free_compound(compound: Compound):
        for i in compound.coaches:
            i.free_seat([i for i in range(len(i.seats.keys()))])

    @staticmethod
    def __create_default_route():
        return Route([
            Railway({Station("A"), Station("B")}, 100),
            Railway({Station("B"), Station("C")}, 100),
            Railway({Station("C"), Station("D")}, 100),
            Railway({Station("D"), Station("E")}, 100),
            Railway({Station("E"), Station("F")}, 100),
            Railway({Station("F"), Station("G")}, 100)
        ])

    @staticmethod
    def cli():
        parser = argparse.ArgumentParser("Railway model", "railway-cli")
        subparsers = parser.add_subparsers(dest="command", help="available commands")

        subparsers.add_parser("state", help="Show train's current state")
        move_parser = subparsers.add_parser("move", help="Move along the route")
        move_parser.add_argument("steps", type=int, nargs="?",
                                 default=1, help="Number of stations to move (default: 1)")

        table_parser = subparsers.add_parser("table", help="Manage timetable")
        table_parser.add_argument("--add", nargs=2, type=int, metavar=("ID", "TIME"),
                                  help="Add compound to timetable (ID TIME)")
        table_parser.add_argument("--show",help="Show timetable")

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

        timetable = None
        state_path = Path(args.file if hasattr(args, "file") else Serializer.STATE_FILE)

        try:
            try:
                timetable = Serializer.load(str(state_path))
                print(f"Loaded from {state_path}")
            except FileNotFoundError:
                print(f"The state is not found")
                compound = Cli.__create_default_compound()
                route = Cli.__create_default_route()
                timetable = Timetable()
                timetable.cells.append(TimetableCell(compound, route, 800))
                print(f"Created new table with (id = {compound.compound_id}")

            if not args.command:
                parser.print_help()
                return 0
            compound = None
            for cell in timetable.cells:
                if cell.compound.compound_id == getattr(args, 'compound_id', 1):
                    compound = cell.compound
                    route = cell.route
                    break

            if not compound:
                print(f"Compound with ID {getattr(args, 'compound_id', 1)} not found")
                return 1

            route = Cli.__create_default_route()
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
                        print(f"The {args.seat} seat in coach {args.coach} is booked for passenger{args.pass_id}")
                    except IndexError:
                        print(f"Ошибка: вагон {args.coach} не существует")
                    except Exception as e:
                        print(f"Ошибка бронирования: {str(e)}")

                case "save":
                    saved_path = Serializer.save(timetable, str(state_path))
                    print(f"Состояние сохранено вручную в {saved_path}")

                case "service":
                    print('g')

                case "table":
                    pass
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
            if timetable is not None and args.command != "save":
                saved_path = Serializer.save(timetable, str(state_path))
                print(f"Состояние автоматически сохранено в {saved_path}")