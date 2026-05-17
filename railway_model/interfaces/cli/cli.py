from pathlib import Path
from management.timer import Timer
from services.compound_service import CompoundService
from services.booking_service import BookingService
from services.locomotive_manager import LocomotiveManager
from services.passenger_service import PassengerService
from services.simulation_service import SimulationService
from interfaces.cli.parser import Parser
from persistence.json_timetable_repository import JsonTimetableRepository
from persistence.json_passenger_repository import JsonPassengerRepository
from persistence.json_clock import JsonClock
from services.timetable_manager import TimetableManager

class Cli:
    @staticmethod
    def _print_departures(departures):
        for d in departures:
            if d.status == "departing":
                print(f"[DEPARTING] Compound {d.compound_id} "
                      f"departs from {d.from_station} "
                      f"at {Timer.format_time(d.departure_time)}")
            else:
                print(f"[SOON] Compound {d.compound_id} "
                      f"departs in {d.minutes_until} min "
                      f"({Timer.format_time(d.departure_time)})")

    @staticmethod
    def _print_movement_events(events):
        for event in events:
            if event.kind == "completed":
                print(f"Compound {event.compound_id} reached final station "
                      f"({event.station_name}), freeing seats")

    @staticmethod
    def _print_state(state):
        print("\nCurrent state ")
        print(f"Compound ID: {state.compound_id}")
        if state.current_station is not None:
            print(f"Pos: {state.current_pos} ({state.current_station})")
        else:
            print("Pos: The route is completed")
        print(f"State: {state.state_name}")
        print("\nCoaches:")
        for coach in state.coaches:
            print(f"Coach {coach.number} (price: {coach.seat_price}): "
                  f"{coach.free_seats} free seats")

    @staticmethod
    def _handle_compound(timetable, args):
        result = CompoundService.create_compound(
            timetable=timetable,
            locomotive_number=args.loco_number,
            coach_amount=args.coach_amount,
            end_station_name=args.end_station,
            departure_time=args.time,
            seats=args.seats,
            price=args.price
        )
        print(f"Created new compound ID={result.compound_id}")
        print(f"Route: {result.route_from} -> {result.route_to}")
        print(f"Departure time: {Timer.format_time(result.departure_time)}")

    @staticmethod
    def _handle_state(timetable, args):
        Cli._print_state(CompoundService.get_state(timetable, args.state_id))

    @staticmethod
    def _handle_book(timetable, args, passengers):
        result = BookingService.book_seat(
            timetable=timetable,
            compound_id=args.comp_book_id,
            coach_number=args.coach,
            seat_number=args.seat,
            passenger_id=args.pass_id,
            passengers=passengers
        )
        print(f"Seat {result.seat_number} in coach {result.coach_number} "
              f"booked for passenger {result.passenger_id}")
        print(f"Departure time: {Timer.format_time(result.departure_time)}, "
              f"Route: {result.route_from}->{result.route_to}")

    @staticmethod
    def _handle_service(timetable, args):
        cell = BookingService._find_cell(timetable, args.number_to_service)
        LocomotiveManager.check_locomotive(cell.compound.locomotive)

    @staticmethod
    def _handle_passenger(args, passengers):
        result = PassengerService.create_passenger(args.name, args.finance, passengers)
        print(f"Created passenger ID={result.passenger_id}, name={result.name}")

    @staticmethod
    def _handle_tick(timetable, args, clock, passengers):
        result = SimulationService.tick(timetable, args.minutes, clock, passengers)
        print(f"Time advanced to: {Timer.format_time(result.new_time)}")
        Cli._print_movement_events(result.movement_events)
        Cli._print_departures(result.departures)

    @staticmethod
    def _handle_settime(args, clock):
        new_time = SimulationService.set_time(args.time, clock)
        print(f"Time set to {Timer.format_time(new_time)} "
              f"({new_time} minutes after midnight)")

    @staticmethod
    def _handle_now(timetable, clock):
        current, departures = SimulationService.now(timetable, clock)
        print(f"Time: {Timer.format_time(current)}")
        Cli._print_departures(departures)

    @staticmethod
    def cli():
        parser = Parser.build_parser()
        arguments = parser.parse_args()
        if hasattr(arguments, "file") and arguments.file:
            timetable_repo = JsonTimetableRepository(str(Path(arguments.file)))
        else:
            timetable_repo = JsonTimetableRepository()
        passenger_repo = JsonPassengerRepository()
        clock = JsonClock()
        timetable = None
        try:
            timetable = timetable_repo.load()
            if not arguments.command:
                parser.print_help()
                return 0
            match arguments.command:
                case "compound": Cli._handle_compound(timetable, arguments)
                case "state": Cli._handle_state(timetable, arguments)
                case "book": Cli._handle_book(timetable, arguments, passenger_repo)
                case "service": Cli._handle_service(timetable, arguments)
                case "timetable": TimetableManager.show_timetable(timetable)
                case "passenger": Cli._handle_passenger(arguments, passenger_repo)
                case "tick": Cli._handle_tick(timetable, arguments, clock, passenger_repo)
                case "settime": Cli._handle_settime(arguments, clock)
                case "now": Cli._handle_now(timetable, clock)
                case "exit":
                    clock.reset()
                    print("Exiting")
                    return 0
                case _:
                    parser.print_help()
                    return 1
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
        finally:


            if timetable is not None and arguments.command not in ("exit", "passenger"):
                timetable_repo.save(timetable)
        return 0