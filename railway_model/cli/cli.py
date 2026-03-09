from cli.timer import Timer
from cli.parser import Parser
from passenger.passenger import Passenger
from exceptions import exceptions
from pathlib import Path
from railway.route import Route, Railway
from management.serializer import Serializer
from compound.compound import Compound, Locomotive, Coach
from management.timetable import Timetable, TimetableCell
from management.ticket_manager import TicketManager
from management.passenger_serializer import PassengerSerializer
from railway.station import Station
from management.validator import Validator
from management.timetable_manager import TimetableManager


class Cli:
    @staticmethod
    def __create_compound(locomotive_number: int, coach_amount: int, seats=10, price=25) -> Compound:
        Validator.validate(locals(), {
            "locomotive_number": (int, lambda x: x >= 0),
            "coach_amount": (int, lambda x: x > 0),
        })
        locomotive = Locomotive(locomotive_number)
        coaches = [Coach(i+1, seats, price)for i in range(coach_amount)]
        return Compound(locomotive, coaches)

    @staticmethod
    def __free_compound(compound: Compound):
        for i in compound.coaches:
            i.free_seat([i for i in range(len(i.seats.keys()))])

    @staticmethod
    def __find_cell_by_comp_id(timetable: Timetable, compound_id: int):
        for cell in timetable.cells:
            if cell.compound.compound_id == compound_id:
                return cell
        return None

    @staticmethod
    def __check_timetable(timetable: Timetable, current_time: int):
        for cell in timetable.cells:
            departure = cell.time
            if departure == current_time:
                print(f"[DEPARTING] Compound {cell.compound.compound_id} "
                      f"departs from {cell.route.stations[0].name} "
                      f"at {Timer.format_time(departure)}")
            elif current_time < departure <= current_time + 30:
                print(f"[SOON] Compound {cell.compound.compound_id} "
                      f"departs in {departure - current_time} min "
                      f"({Timer.format_time(departure)})")

    @staticmethod
    def __get_cell(timetable: Timetable, compound_id: int) -> TimetableCell:
        cell = Cli.__find_cell_by_comp_id(timetable, compound_id)
        if not cell:
            raise exceptions.TimetableError(f"Compound {compound_id} not found")
        return cell

    @staticmethod
    def __state(cell: TimetableCell):
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
            print(f"Coach {coach.number} (price: {coach.seat_price}): {coach.free_seats} free seats")

    @staticmethod
    def __move(cell: TimetableCell):
        compound = cell.compound
        route = cell.route
        compound.locomotive.start_engine()
        print(f"\nMoving compound {compound.compound_id}")
        compound.move_along_route(route)
        if compound.current_pos == len(route.stations) - 1:
            print(f"Compound {compound.compound_id} reached final station, freeing seats...")
            compound.process_station_actions()
            PassengerSerializer.remove_tickets_for_compound(compound.compound_id)

    @staticmethod
    def __book(cell: TimetableCell, timetable: Timetable, parser):
        compound = cell.compound
        route = cell.route
        if parser.coach < 1 or parser.coach > len(compound.coaches):
            raise exceptions.SeatError(f"Coach {parser.coach} does not exist.")
        coach = compound.coaches[parser.coach - 1]
        if parser.seat not in coach.seats:
            raise exceptions.SeatError(f"Seat {parser.seat} does not exist in coach {parser.coach}.")
        if parser.seat not in coach.free_seats:
            raise exceptions.SeatError(f"Seat {parser.seat} in coach {parser.coach} is already occupied")
        if coach.seats[parser.seat] == parser.pass_id:
            raise exceptions.SeatError(f"Passenger {parser.pass_id} already occupies seat {parser.seat}")
        passenger = PassengerSerializer.get_passenger(parser.pass_id, timetable)
        TicketManager.create_ticket(passenger, compound, coach, parser.seat, cell.time)
        PassengerSerializer.save_passenger(passenger)
        print(f"Seat {parser.seat} in coach {parser.coach} booked for passenger {parser.pass_id}")
        print(
            f"Departure time: {Timer.format_time(cell.time)}, Route: {route.stations[0].name}->{route.stations[-1].name}")

    @staticmethod
    def __service(cell: TimetableCell):
        locomotive = cell.compound.locomotive
        locomotive.get_service()

    @staticmethod
    def __create(timetable, args):
        for cell in timetable.cells:
            if cell.compound.locomotive.number == args.loco_number:
                raise exceptions.CreatingEntityError(f"The locomotive {args.loco_number} is already occupied")
        new_compound = Cli.__create_compound(
            locomotive_number=args.loco_number,
            coach_amount=args.coach_amount,
            seats=args.seats,
            price=args.price
        )
        start_station = Station("O")
        end_station = Station(args.end_station)
        route = Route([Railway({start_station, end_station}, 100)])
        TimetableManager.add_cell(timetable, TimetableCell(new_compound, route, args.time))
        print(f"Created new compound ID={new_compound.compound_id}")
        print(f"Route: O -> {args.end_station}")
        print(f"Departure time: {Timer.format_time(args.time)}")

    @staticmethod
    def __passenger(args):
        data = PassengerSerializer.load_passengers()
        Passenger.id_counter = data.get("id_counter", 1)
        passenger = Passenger(args.name, args.finance)
        PassengerSerializer.save_passenger(passenger)
        print(f"Created passenger ID={passenger.passenger_id}, name={passenger.name}")

    @staticmethod
    def __set_time(time: int):
        current_time = Timer.load_time()
        if time <= current_time:
            raise exceptions.TimetableError("You cant set time less than now")
        Timer.set_time(Timer.format_time(time))
        print(f"Time set to {Timer.format_time(time)} ({time} minutes after midnight)")

    @staticmethod
    def cli():
        parser = Parser.build_parser()
        arguments = parser.parse_args()
        timetable = None
        state_path = Path(arguments.file if hasattr(arguments, "file") else Serializer.STATE_FILE)
        try:
            try:
                timetable = Serializer.load_state(str(state_path))
            except FileNotFoundError:
                print("State file not found, creating empty timetable")
                timetable = Timetable()
            if not arguments.command:
                parser.print_help()
                return 0

            match arguments.command:
                case "create":
                    Cli.__create(timetable, arguments)
                case "state":
                    Cli.__state(Cli.__get_cell(timetable, arguments.state_id))
                case "book":
                    Cli.__book(Cli.__get_cell(timetable, arguments.comp_book_id), timetable, arguments)
                case "service":
                    Cli.__service(Cli.__get_cell(timetable, arguments.number_to_service))
                case "timetable":
                    timetable.show_all()
                case "passenger":
                    Cli.__passenger(arguments)
                case "tick":
                    new_time = Timer.advance(arguments.minutes)
                    print(f"Time advanced to: {Timer.format_time(new_time)}")
                    for cell in timetable.cells:
                        if cell.time <= new_time and cell.compound.current_pos < len(cell.route.stations) - 1:
                            Cli.__move(cell)
                    Cli.__check_timetable(timetable, new_time)
                case "settime":
                    Cli.__set_time(arguments.time)
                case "now":
                    current_time = Timer.load_time()
                    print(f"Time: {Timer.format_time(current_time)}")
                    Cli.__check_timetable(timetable, current_time)
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
            if timetable is not None and arguments.command not in ("exit", "passenger"):
                Serializer.save_state(timetable, str(state_path))
        return 0


