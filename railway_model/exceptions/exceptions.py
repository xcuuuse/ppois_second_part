class TicketSellingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SeatError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class LocomotiveUsingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

