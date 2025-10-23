from typing import Any
from functools import total_ordering

@total_ordering
class Time:
    def __init__(self, hours: int, minutes: int) -> None:
        '''stores time in 24-hour format'''
        self.hours = hours
        self.minutes = minutes

    @staticmethod
    def earliest_time():
        return Time(0,0)
    @staticmethod
    def latest_time():
        return Time(23,59)

    @staticmethod
    def is_valid_time(hours: int, minutes: int) -> bool:
        return hours >= 0 and hours <= 23 and minutes >= 0 and minutes < 60

    @staticmethod
    def from_string(description: str) -> 'Time':
        hour_str, minute_str = description.split(":", maxsplit=1)
        hours = int(hour_str)
        minutes = int(minute_str)
        if not Time.is_valid_time(hours, minutes):
            raise ValueError(f"The string '{description}' is not a valid time")
        return Time(hours, minutes)

    def to_minutes(self) -> int:
        return 60*self.hours + self.minutes

    def difference_in_minutes(self, other: 'Time') -> int:
        return abs((self - other).to_minutes())

    def __add__(self, other: 'Time') -> 'Time':
        new_hours = self.hours + other.hours
        new_minutes = self.minutes + other.minutes
        new_hours += new_minutes // 60
        new_minutes %= 60
        return Time(new_hours, new_minutes)

    def __sub__(self, other: 'Time') -> 'Time':
        new_hours = self.hours - other.hours
        new_minutes = self.minutes - other.minutes
        new_hours += new_minutes // 60
        new_minutes %= 60
        if new_hours < 0:
            new_minutes -= 60
            new_hours += 1
        return Time(new_hours, new_minutes)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Time):
            return (self.hours == other.hours) and (self.minutes == other.minutes)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Time):
            return (self.hours < other.hours) or ((self.hours == other.hours) and (self.minutes < other.minutes))
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.hours, self.minutes))

    def __str__(self) -> str:
        return f"{self.hours:02}:{self.minutes:02}"



class DailyTimes:
    WEEKDAYS = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday'}
    def __init__(self, schedule: dict[str, list[str]]) -> None:
        self.blocks : dict[str, tuple[Time,Time]] = {}
        for day in self.WEEKDAYS:
            if day in schedule:
                start = Time.from_string(schedule[day][0])
                end = Time.from_string(schedule[day][1])
                self.blocks[day] = (start, end)

    def day_has_scheduled_block(self, day: str) -> bool:
        return day in self.blocks

    def times_on_day(self, day: str) -> tuple[Time, Time]:
        return self.blocks[day]


class Course:
    def __init__(self, code: str, info: dict[str, Any]) -> None:
        self.code = code
        self.name: str = info["name"]
        self.location: str = info["location"]
        self.times = DailyTimes(info["times"])

    def meets_on_this_day(self, day: str) -> bool:
        return self.times.day_has_scheduled_block(day)

    def meeting_times_on_day(self, day: str) -> tuple[Time, Time]:
        return self.times.times_on_day(day)
