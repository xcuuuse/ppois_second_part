import threading
import time
from railway.route import Route
from compound.compound import Compound
from management.timetable import Timetable, TimetableCell
from exceptions.exceptions import TimetableError


class RouteManager:
    def __init__(self, route: Route, compound: Compound,
                 timetable: Timetable):
        self.__route = route
        self.__compound = compound
        self.__timetable = timetable
        self.__time = 0
        self.__running = False
        self.__timer_thread = None

    def __update_time(self):
        while True:
            time.sleep(1)
            self.__time += 1

    def start_timer(self):
        self.__running = True
        self.__timer_thread = threading.Thread(target=self.__update_time)
        self.__timer_thread.start()

    def stop_timer(self):
        self.__running = False
        if self.__timer_thread and self.__timer_thread.is_alive():
            self.__timer_thread.join()

    def control_route_action(self):
        self.start_timer()
        self.__compound.check_state()
        cell = TimetableCell(self.__compound, self.__route, self.__time)
        if cell not in self.__timetable.cells:
            raise TimetableError("No cell")
        for cell in self.__timetable.cells:
            if cell.compound == self.__compound:
                while self.__time < cell.time:
                    time.sleep(0.1)
                self.__compound.move_along_route(self.__route)
        self.stop_timer()




