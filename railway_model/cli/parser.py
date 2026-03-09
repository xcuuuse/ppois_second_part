import argparse


class Parser:
    @staticmethod
    def build_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser("Railway model", "railway-cli")
        subparsers = parser.add_subparsers(dest="command", help="available commands")

        state_parser = subparsers.add_parser("state", help="Show train's current state")
        state_parser.add_argument("state_id", type=int, help="Id for compound to show state")

        move_parser = subparsers.add_parser("move", help="Move along the route")
        move_parser.add_argument("move_comp_id", type=int, nargs="?",
                                 default=1, help="Number of compound to move")

        subparsers.add_parser("timetable", help="Manage timetable")

        book_parser = subparsers.add_parser("book", help="Book a seat")
        book_parser.add_argument("comp_book_id", type=int, help="Compound id")
        book_parser.add_argument("coach", type=int, help="Coach number")
        book_parser.add_argument("seat", type=int, help="Seat number")
        book_parser.add_argument("pass_id", type=int, help="Passenger id")

        service_parser = subparsers.add_parser("service", help="Service the compound")
        service_parser.add_argument("number_to_service", type=int, help="Compound ID")

        create_parser = subparsers.add_parser("create",
                                              help="Creates compound with route from O to end station")
        create_parser.add_argument("loco_number", type=int, help="Locomotive number")
        create_parser.add_argument("coach_amount", type=int, help="Number of coaches")
        create_parser.add_argument("end_station", type=str, help="End station name (start is always O)")
        create_parser.add_argument("--time", type=int, default=480, help="Departure time in minutes")
        create_parser.add_argument("--seats", type=int, default=10, help="Seats per coach")
        create_parser.add_argument("--price", type=int, default=25, help="Seat price")

        subparsers.add_parser("tick", help="Advance simulation time")
        settime_parser = subparsers.add_parser("settime", help="Set simulation time manually")
        settime_parser.add_argument("time", type=int, help="Time in minutes")
        passenger_parser = subparsers.add_parser("passenger", help="Creates a passenger")
        passenger_parser.add_argument("name", type=str, help="Passenger name")
        passenger_parser.add_argument("finance", type=int, help="Passenger finance")
        subparsers.add_parser("now", help="Show current simulation time")
        subparsers.add_parser("exit", help="Exit")
        return parser

