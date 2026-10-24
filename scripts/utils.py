
import collections
import datetime
import os
import re

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

Date = collections.namedtuple("Date", [
    "edition",
    "month_name",
    "month",
    "year",
    "date",
])


# TODO: Replace with date.strptime from python 3.14 when I can use that.
def get_month_name(month_int):
    if month_int == 1:
        return "January"
    if month_int == 2:
        return "February"
    if month_int == 3:
        return "March"
    if month_int == 4:
        return "April"
    if month_int == 5:
        return "May"
    if month_int == 6:
        return "June"
    if month_int == 7:
        return "July"
    if month_int == 8:
        return "August"
    if month_int == 9:
        return "September"
    if month_int == 10:
        return "October"
    if month_int == 11:
        return "November"
    if month_int == 12:
        return "December"


def parse_date(edition):
    year, month = edition.split('-')
    year = int(year)
    month = int(month)
    month_name = get_month_name(month)
    # Just mark it as the first of the month. Currently just used for sorting.
    date = f'{year}-{month:02}-01'
    return Date(edition, month_name, month, year, date)


def next_month():
    today = datetime.date.today()
    year = today.year
    month = today.month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

    return f"{year}-{month:02}"


def ensure_edition_dir(edition):
    edition_dir = os.path.join(ROOT_DIR, f'content/editions/{edition}')
    os.makedirs(edition_dir, exist_ok=True)
    return edition_dir


def filename_from_title(title):
    filename = re.sub(r'[^\w\d -]', '', title)
    return re.sub(r'\s+', '_', filename) + '.md'

def add_index(date, edition_dir):
    with open(os.path.join(edition_dir, '_index.md'), 'w') as wfp:
        front_matter = (
            '---',
            f'title: "{date.month_name}, {date.year}"',
            f'year: {date.year}',
            f'monthIndex: {date.month}',
            f'date: {date.date}',
            f'pdf: /editions/Frenchtown-Sun-{date.month_name}-{date.year}.pdf',
            '---',
        )
        wfp.writelines('\n'.join(front_matter))

