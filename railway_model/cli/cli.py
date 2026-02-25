import argparse
import sys
import json
from passenger.passenger import Passenger
from exceptions import exceptions
from pathlib import Path
from railway.route import Route, Station, Railway
from management.serializer import Serializer
from management.locomotive_manager import LocomotiveManager
from compound.compound import Compound, Locomotive, Coach
from management.timetable import Timetable, TimetableCell
from management.ticket_manager import TicketManager
from typing import List


class Timer:
    TIME_FILE = "time.json"

    @staticmethod
    def load_time():
        try:
            with open(Timer.TIME_FILE, "r") as f:
                return json.load(f)["time"]
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    @staticmethod
    def save_time(time):
        with open(Timer.TIME_FILE, "w") as f:
            json.dump({"time": time}, f)

    @staticmethod
    def increment_time():
        current_time = Timer.load_time()
        new_time = current_time + 100
        Timer.save_time(new_time)
        return new_time

    @staticmethod
    def reset_time():
        with open(Timer.TIME_FILE, "w") as f:
            json.dump({"time": 0}, f)


class Cli:
    @staticmethod
    def __create_default_compound():
        locomotive = Locomotive(1)
        coaches = [
            Coach(number=1, seats_amount=5, seat_price=25),
            Coach(number=2, seats_amount=4, seat_price=45)
        ]
        return Compound(locomotive, coaches)

    @staticmethod
    def __create_compound(locomotive_number: int, coach_amount: int, seats=10, price=25):
        locomotive = Locomotive(locomotive_number)
        coaches = [Coach(number=i+1, seats_amount=seats, seat_price=price)for i in range(coach_amount)]
        return Compound(locomotive, coaches)

    @staticmethod
    def __free_compound(compound: Compound):
        for i in compound.coaches:
            i.free_seat([i for i in range(len(i.seats.keys()))])

    @staticmethod
    def __create_default_route():
        return Route([
            Railway({Station("O"), Station("A")}, 100)
        ])

    @staticmethod
    def create_route(main_station: Station, add_station: Station, length=100):
        return Route([Railway({main_station, add_station}, length)])

    @staticmethod
    def __find_compound(timetable: Timetable, compound_id: int):
        for cell in timetable.cells:
            if cell.compound.compound_id == compound_id:
                return cell
        return None

    """def __create_passenger(self, name: str):
        passenger = Passenger(name, finance=100)
        self.__passengers[passenger.passenger_id] = passenger
        return passenger """

    @staticmethod
    def __book_seat(passenger: Passenger, compound: Compound, coach: Coach, seat_number: int, time: int):
        TicketManager.create_ticket(passenger, compound, coach, seat_number, time)

    @staticmethod
    def check_timetable(timetable: Timetable, current_time: int):
        for cell in timetable.cells:
            if cell.time == current_time + 100:
                print(f"The compound {cell.compound.compound_id} is gonna depart")
                return True
        return False


    @staticmethod
    def cli():
        main_station: Station = Station("O")

        parser = argparse.ArgumentParser("Railway model", "railway-cli")
        subparsers = parser.add_subparsers(dest="command", help="available commands")

        state_parser = subparsers.add_parser("state", help="Show train's current state")
        state_parser.add_argument("state_id", type=int, help="Id for compound to show state")
        move_parser = subparsers.add_parser("move", help="Move along the route")
        move_parser.add_argument("move_id", type=int, nargs="?",
                                 default=1, help="Number of compound to move")

        table_parser = subparsers.add_parser("table", help="Manage timetable")
        table_parser.add_argument("--add", nargs=2, type=int, metavar=("ID", "TIME"),
                                  help="Add compound to timetable (ID TIME)")
        table_parser.add_argument("--show", action="store_true", help="Show timetable")

        book_parser = subparsers.add_parser("book", help="Book a seat")
        book_parser.add_argument("coach", type=int, help="Coach number")
        book_parser.add_argument("seat", type=int, help="Seat number")
        book_parser.add_argument("pass_id", type=int, help="Passenger id")

        save_parser = subparsers.add_parser("save", help="Save state")
        save_parser.add_argument("--file", type=str, default=Serializer.STATE_FILE,
                                 help="File to save to")

        service_parser = subparsers.add_parser("service", help="Service the compound")
        service_parser.add_argument("number", type=int, help="Compound ID")

        create_compound_parser = subparsers.add_parser("create_compound", help="Creates the compound")
        create_compound_parser.add_argument("loco_number", type=int, help="Locomotive number")
        create_compound_parser.add_argument("coach_amount", type=int, help="Coach amount")
        subparsers.add_parser("exit", help="Exit")
        args = parser.parse_args()

        timetable = None
        state_path = Path(args.file if hasattr(args, "file") else Serializer.STATE_FILE)
        try:
            try:
                timetable = Serializer.load(str(state_path))
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
                case "state": #fix
                    print("\n Current state ")
                    for cell in timetable.cells:
                        if cell.compound.compound_id == args.state_id:
                            break
                        else:
                            raise exceptions.TimetableError("Compound not found")
                    print(f"Compound ID: {compound.compound_id}")
                    if compound.current_pos < len(route.stations):
                        print(f"Pos: {compound.current_pos} ({route.stations[compound.current_pos].name})")
                    else:
                        print("Pos: The route is completed")
                    print(f"State: {compound.state.name}")
                    print("\nCoaches:")
                    for coach in compound.coaches:
                        free = len(coach.free_seats)
                        print(f"Coach {coach.number} (price: {coach.seat_price}): {free}/{len(coach.seats)} free seats")

                case "move":
                    print(f"\nMoving compound {args.compound_id}")

                    cell = Cli.__find_compound(timetable, args.compound_id)
                    if not cell:
                        raise exceptions.TimetableError("No compound")
                    compound = cell.compound
                    route = cell.route
                    if compound.current_pos > len(route.stations) - 1:
                        raise exceptions.TimetableError("The compound has already finished the route")
                    elif compound.current_pos == len(route.stations) - 1:
                        print(f"The compound {args.compound_id} has completed the route")
                        compound.process_station_actions()
                    elif cell.time < Timer.increment_time():
                        raise exceptions.TimetableError("The compound has already departed")
                    else:
                        compound.move_along_route(route)

                case "book": #finish
                    try:
                        compound.coaches[args.coach - 1].occupy_seat(args.seat, args.pass_id)
                        print(f"The {args.seat} seat in coach {args.coach} is booked for passenger{args.pass_id}")
                    except IndexError:
                        print(f"Error: coach {args.coach} doesn't exist")
                    except Exception as e:
                        print(f"Booking error: {str(e)}")

                case "save":
                    Serializer.save(timetable, str(state_path))

                case "service":
                    cell = Cli.__find_compound(timetable, args.number)
                    if not cell:
                        raise exceptions.TimetableError("No compound")
                    compound = cell.compound
                    manager = LocomotiveManager()
                    manager.check_locomotive(compound.locomotive)

                case "create_compound": #finish
                    new_compound = Cli.__create_compound(
                        locomotive_number=args.loco_number,
                        coach_amount=args.coach_amount
                    )
                    route = Cli.__create_default_route()
                    timetable.cells.append(TimetableCell(new_compound, route, time=800))
                    print("Created new compound")

                case "table":
                    if args.add:
                        compound_id, time = args.add
                        cell = Cli.__find_compound(timetable, compound_id)
                        if not cell:
                            print(f"Compound {compound_id} not found")
                            return 1
                        cell.time = time
                        print(f"Updated {compound.compound_id} time")
                    elif args.show:
                        for cell in timetable.cells:
                            print(str(cell))
                    else:
                        parser.print_help()
                case "exit":
                    Timer.reset_time()
                    print("Exiting...")
                    return 0

                case _:
                    parser.print_help()
                    return 1

        except Exception as e:
            print(f"Error: {str(e)}")
            return 1

        finally:
            if args.command and args.command != "exit":
                current_time = Timer.increment_time()
                print(f"Time: {current_time}")
                Cli.check_timetable(timetable, current_time)
            if timetable is not None and args.command != "save":
                Serializer.save(timetable, str(state_path))


