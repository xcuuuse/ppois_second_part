from management.timer import Timer


class JsonClock:

    def now(self):
        return Timer.load_time()

    def advance(self, minutes: int):
        return Timer.advance(minutes)

    def set_to(self, target_minutes: int):
        return Timer.set_time(Timer.format_time(target_minutes))

    def reset(self):
        Timer.reset_time()
