import json
from exceptions.exceptions import TimetableError


class Timer:
    TIME_FILE = "data/time.json"

    @staticmethod
    def load_time():
        try:
            with open(Timer.TIME_FILE, "r") as file:
                return json.load(file)["time"]
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    @staticmethod
    def save_time(time: int):
        with open(Timer.TIME_FILE, "w") as file:
            json.dump({"time": time}, file)

    @staticmethod
    def advance(minutes: int = 30):
        time = min(Timer.load_time() + minutes, 1439)
        Timer.save_time(time)
        return time

    @staticmethod
    def set_time(time_hhmm: str):
        hour, minute = map(int, time_hhmm.split(":"))
        time = hour * 60 + minute
        Timer.save_time(time)
        return time

    @staticmethod
    def format_time(minutes: int) -> str:
        if minutes < 0:
            raise TimetableError("Minutes value has to be more than xero")
        hour = minutes // 60
        minute = minutes - hour * 60
        return f"{hour:02d}:{minute:02d}"

    @staticmethod
    def reset_time():
        Timer.save_time(0)

