import json
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