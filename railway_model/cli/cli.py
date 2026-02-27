import argparse
from cli.timer import Timer
from passenger.passenger import Passenger
from exceptions import exceptions
from pathlib import Path
from railway.route import Route, Station, Railway
from management.serializer import Serializer
from compound.compound import Compound, Locomotive, Coach
from management.timetable import Timetable, TimetableCell
from management.ticket_manager import TicketManager


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
    def __create_route(main_station: Station, add_station: Station, length=100):
        return Route([Railway({main_station, add_station}, length)])

    @staticmethod
    def __find_cell_by_comp_id(timetable: Timetable, compound_id: int):
        for cell in timetable.cells:
            if cell.compound.compound_id == compound_id:
                return cell
        return None

    @staticmethod
    def __book_seat(passenger: Passenger, compound: Compound, coach: Coach, seat_number: int, time: int):
        TicketManager.create_ticket(passenger, compound, coach, seat_number, time)

    @staticmethod
    def check_timetable(timetable: Timetable, current_time: int):
        for cell in timetable.cells:
            if cell.time == current_time + 100:
                print(f"\nThe compound {cell.compound.compound_id} is departing from {cell.route.stations[0].name}")

    @staticmethod
    def cli():
        parser = argparse.ArgumentParser("Railway model", "railway-cli")
        subparsers = parser.add_subparsers(dest="command", help="available commands")

        state_parser = subparsers.add_parser("state", help="Show train's current state")
        state_parser.add_argument("state_id", type=int, help="Id for compound to show state")
        move_parser = subparsers.add_parser("move", help="Move along the route")
        move_parser.add_argument("move_comp_id", type=int, nargs="?",
                                 default=1, help="Number of compound to move")

        table_parser = subparsers.add_parser("table", help="Manage timetable")
        table_parser.add_argument("--add", nargs=2, type=int, metavar=("ID", "TIME"),
                                  help="Add compound to timetable (ID TIME)")
        table_parser.add_argument("--show", action="store_true", help="Show timetable")

        book_parser = subparsers.add_parser("book", help="Book a seat")
        book_parser.add_argument("comp_book_id", type=int, help="Coach number")
        book_parser.add_argument("coach", type=int, help="Coach number")
        book_parser.add_argument("seat", type=int, help="Seat number")
        book_parser.add_argument("pass_id", type=int, help="Passenger id")

        save_parser = subparsers.add_parser("save", help="Save state")
        save_parser.add_argument("--file", type=str, default=Serializer.STATE_FILE,
                                 help="File to save to")

        service_parser = subparsers.add_parser("service", help="Service the compound")
        service_parser.add_argument("number_to_service", type=int, help="Compound ID")

        create_compound_parser = subparsers.add_parser("create_compound",
                                                       help="Creates compound with route from O to end station")
        create_compound_parser.add_argument("loco_number", type=int, help="Locomotive number")
        create_compound_parser.add_argument("coach_amount", type=int, help="Number of coaches")
        create_compound_parser.add_argument("end_station",
                                            type=str, help="End station name (start is always O)")
        create_compound_parser.add_argument("--seats", type=int, default=10, help="Seats per coach")
        create_compound_parser.add_argument("--price", type=int, default=25, help="Seat price")
        create_compound_parser.add_argument("--time", type=int, default=800, help="Departure time")

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
                raise exceptions.TimetableError("There is no compound with such id")

            match args.command:
                case "state":
                    cell = Cli.__find_cell_by_comp_id(timetable, args.state_id)
                    if not cell:
                        raise exceptions.TimetableError("Compound not found")

                    compound = cell.compound
                    route = cell.route
                    print("\nCurrent state ")
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
                    print(f"\nMoving compound {args.move_comp_id}")
                    cell = Cli.__find_cell_by_comp_id(timetable, args.move_comp_id)
                    if not cell:
                        raise exceptions.TimetableError("No compound to move")
                    compound = cell.compound
                    route = cell.route
                    compound.locomotive.start_engine()
                    if compound.current_pos > len(route.stations) - 1:
                        raise exceptions.TimetableError("The compound has already finished the route")
                    elif compound.current_pos == len(route.stations) - 1:
                        print(f"The compound {args.move_comp_id} has completed the route")
                        compound.process_station_actions()
                    elif cell.time < Timer.load_time():
                        raise exceptions.TimetableError("The compound has already departed")
                    else:
                        compound.move_along_route(route)

                case "book":
                    cell = Cli.__find_cell_by_comp_id(timetable, args.comp_book_id)
                    if not cell:
                        raise exceptions.TimetableError("Compound not found")
                    compound = cell.compound
                    route = cell.route
                    if args.coach < 1 or args.coach > len(compound.coaches):
                        raise exceptions.SeatError(f"Coach {args.coach} does not exist.")
                    coach = compound.coaches[args.coach - 1]
                    if args.seat not in coach.seats:
                        raise exceptions.SeatError(f"Seat {args.seat} does not exist in coach {args.coach}.")
                    if args.seat not in coach.free_seats:
                        raise exceptions.SeatError(f"Seat {args.seat} in coach {args.coach} is already occupied")
                    if coach.seats[args.seat] == args.pass_id:
                        raise exceptions.SeatError(f"Passenger {args.pass_id} already occupies seat {args.seat}")
                    try:
                        coach.occupy_seat(args.seat, args.pass_id)
                        print(f"Seat {args.seat} in coach {args.coach} booked for passenger {args.pass_id}")
                        print(
                            f"Departure time: {cell.time}, Route: {route.stations[0].name} → {route.stations[-1].name}")
                    except Exception as e:
                        raise exceptions.TicketSellingError(f"Booking failed: {str(e)}")
                case "save":
                    Serializer.save(timetable, str(state_path))

                case "service":
                    cell = Cli.__find_cell_by_comp_id(timetable, args.number_to_service)
                    if not cell:
                        raise exceptions.TimetableError("No compound")
                    locomotive = cell.compound.locomotive
                    locomotive.get_service()

                case "create_compound":
                    new_compound = Cli.__create_compound(
                        locomotive_number=args.loco_number,
                        coach_amount=args.coach_amount,
                        seats=args.seats,
                        price=args.price
                    )
                    start_station = Station("O")
                    end_station = Station(args.end_station)
                    route = Route([Railway({start_station, end_station}, 100)])
                    timetable.cells.append(TimetableCell(new_compound, route, args.time))
                    print(f"Created new compound ID={new_compound.compound_id}")
                    print(f"Route: O → {args.end_station}")
                    print(f"Departure time: {args.time}")
                case "table":
                    if args.add:
                        compound_id, time = args.add
                        cell = Cli.__find_cell_by_comp_id(timetable, compound_id)
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
        return 0
