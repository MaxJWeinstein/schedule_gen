#!/Users/Max/Documents/drexel/schedule_gen/venv/bin/python
from pathlib import Path
from sys import argv, exit

from schedule_maker import ScheduleMaker

VALID_SEASONS = ["fall", "winter", "spring", "summer"]
SCHOOL_DIRECTORY = Path("/Users/Max/Documents/drexel")

def usage():
    print("schedule_gen.py SEASON YEAR")
    print(f"SEASON must be one of {VALID_SEASONS}")
    print("YEAR must be the last 2 digits of the year")
    exit(1)

def main(args: list[str]):
    # parse command-line arguments
    if len(args) != 3: usage()
    season = args[1].lower()
    if season not in VALID_SEASONS: usage()
    year = args[2]
    if len(year) != 2 or not year.isdigit(): usage()

    term_directory = SCHOOL_DIRECTORY / f"{season}_{year}"
    source_file = term_directory / "schedule.json"

    schedule_maker = ScheduleMaker(source_file, html_path=term_directory/"schedule.html", css_path=term_directory/"style.css", base_css_path=SCHOOL_DIRECTORY/"schedule_gen"/"base_style.css")
    schedule_maker.generate_html_page()
    return schedule_maker

if __name__ == "__main__":
    main(argv)
