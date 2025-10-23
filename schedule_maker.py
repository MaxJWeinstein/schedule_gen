import json
from math import ceil
from pathlib import Path
import shutil

import htpy

from schedule import Course, DailyTimes, Time


class ScheduleMaker:
    def __init__(self, source_file: Path, html_path: Path, css_path: Path, base_css_path: Path, minutes_per_row:int=30) -> None:
        self.source = source_file
        self.html_path = html_path
        self.css_path = css_path
        self.base_css_path = base_css_path

        with open(source_file) as f:
            info = json.load(f)
            self.courses = [Course(code, course_info) for code,course_info in info.items()]

        self.minutes_per_row = minutes_per_row
        self.times = self.determine_time_intervals(Time(minutes_per_row//60, minutes_per_row%60))

        self.meetings: dict[str, MeetingTime] = {}
        i = 1
        for course in self.courses:
            for day, (start, end) in course.times.blocks.items():
                self.meetings[f"event{i}"] = MeetingTime(day, start, end, course)
                i += 1

        self.calendar_body = htpy.body[
            htpy.div(".container")[
                htpy.div(".days")[
                    htpy.div(".filler"),htpy.div(".filler"),
                    *[htpy.div(".day")[day] for day in DailyTimes.WEEKDAYS.values()]
                ],
                htpy.div(".calendar")[
                    *[htpy.div(".time", style=f"grid-row:{i+1}")[str(time)] for i, time in enumerate(self.times)],
                    htpy.div(".filler-col"),
                    *[htpy.div(".col", style=f"grid-column:{i+3}") for i in range(len(DailyTimes.WEEKDAYS))],
                    *[htpy.div(".row", style=f"grid-row:{i+1}") for i in range(len(self.times))],
                    *[htpy.div(class_=["event", name])[meeting.html_body()] for name, meeting in self.meetings.items()]
                ]
            ]
        ]

        self.html_file_contents = htpy.html[
            htpy.head[
                htpy.meta(charset="utf-8"),
                htpy.meta(http_equiv="X-UA-Compatible", content="IE=edge"),
                htpy.title["Weekly Schedule"],
                htpy.meta(name="viewport", content="width=device-width, initial-scale=1"),
                htpy.link(rel="stylesheet", href=css_path.as_uri())
            ],
            self.calendar_body
        ]

    def determine_time_intervals(self, sep:Time=Time(0,30)) -> list[Time]:
        earliest = Time.latest_time()
        latest = Time.earliest_time()
        for course in self.courses:
            for start, end in course.times.blocks.values():
                if start < earliest:
                    earliest = start
                if end > latest:
                    latest = end

        times: list[Time] = []
        current_time = earliest - sep
        while current_time <= latest:
            times.append(current_time)
            current_time += sep
        times.append(current_time)
        return times

    def generate_html_page(self):
        shutil.copy2(self.base_css_path, self.css_path)
        with open(self.css_path, "a") as f:
            f.write(f"* {{\n\t--num-rows: {len(self.times)};\n}}\n")
            for event_number, meeting_info in self.meetings.items():
                style=f".{event_number} {meeting_info.style_body(self.times[0], self.minutes_per_row)}\n"
                f.write(style)


        with open(self.html_path, "w") as f:
            f.write(str(self.html_file_contents))

class MeetingTime:
    def __init__(self, day: str, start: Time, end: Time, course: Course) -> None:
        self.course = course
        self.start = start
        self.end = end
        day_number = list(DailyTimes.WEEKDAYS).index(day)
        self.grid_column = day_number + 3

    def grid_row(self, start_of_day: Time, minutes_per_row:int=30) -> int:
        time_into_day = self.start.difference_in_minutes(start_of_day)
        raw_row = ceil(time_into_day/minutes_per_row)
        return raw_row + 2

    def num_rows(self, minutes_per_row:int=30):
        duration = self.start.difference_in_minutes(self.end)
        return ceil(duration/minutes_per_row)

    def style_body(self, start_of_day: Time, minutes_per_row:int=30) -> str:
        return f"{{\n\tgrid-column: {self.grid_column};\n\tgrid-row: {self.grid_row(start_of_day,minutes_per_row)}/span {self.num_rows(minutes_per_row)};\n}}"

    def html_body(self) -> htpy.Fragment:
        return htpy.fragment[
            htpy.div(".event-time")[f"{self.start} - {self.end}"],
            htpy.div(".event-title")[self.course.code],
            htpy.div(".event-location")[self.course.location]
        ]
