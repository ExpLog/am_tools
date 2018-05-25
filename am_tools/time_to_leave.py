import datetime as dt
from typing import List, Optional

import mechanicalsoup
import re

outer_table_row_re = re.compile(r"ctl00_DefaultContent_EmployeeMapGrid_ctl00__[0-9]+")
time_table_row_re = re.compile(r"ctl00_DefaultContent_EmployeeMapGrid_ctl00_ctl36_DataGrid[1-4]")
clock_re = re.compile(r"[0-9]{2}:[0-9]{2}:[0-9]{2}")
date_re = re.compile(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")


def build_clock_in_out_datetimes(table_row_text: str) -> Optional[List[Optional[dt.datetime]]]:
    match = date_re.search(table_row_text)
    if match:
        date = match.group()
    else:
        return None

    clock_times = clock_re.findall(table_row_text)
    if not clock_times:
        return None

    month, day, year = [int(x) for x in date.split("/")]
    datetime_list = []
    for time in clock_times:
        hour, minute, second = [int(x) for x in time.split(":")]
        datetime = dt.datetime(year, month, day, hour, minute, second)
        datetime_list.append(datetime)

    if len(datetime_list) < 4:
        datetime_list.extend([None] * (4 - len(datetime_list)))

    return datetime_list


def get_work_clock_times(user: str, password: str) -> List[List[Optional[dt.datetime]]]:
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("http://asmill01/millenium/")

    browser.select_form("#aspnetForm")
    browser["ctl00$DefaultContent$Login1$UserName"] = user
    browser["ctl00$DefaultContent$Login1$Password"] = password

    browser.submit_selected()

    cookie_jar = browser.get_cookiejar()
    cookie_jar.set("EmployeeMapPageSize", "31", domain="asmill01.local")
    browser.open("http://asmill01/Millenium/TNADiary/Default.aspx")

    page = browser.get_current_page()

    table = page.find("table", id="ctl00_DefaultContent_EmployeeMapGrid_ctl00")
    times = [build_clock_in_out_datetimes(row.text) for row in table.find_all("tr", id=outer_table_row_re)]
    return [t for t in times if t]


def calculate_time_to_leave(entry: dt.datetime, lunch: dt.datetime, back: dt.datetime) -> dt.datetime:
    total = dt.timedelta(seconds=8 * 60 * 60)
    morning_work = lunch - entry
    total = total - morning_work
    return back + total


def build_time_to_leave_message(credentials: dict) -> str:
    time_list = get_work_clock_times(credentials["user"], credentials["password"])[-1]

    entry, lunch, back = time_list[0], time_list[1], time_list[2]
    estimate = False
    is_today = True

    today = dt.datetime.now()
    if today.date() != entry.date():
        is_today = False

    if not entry:
        return "There is no entry time"
    if not lunch:
        lunch = entry + dt.timedelta(hours=3)
        estimate = True
    if not back:
        back = lunch + dt.timedelta(hours=1)
        estimate = True

    leave = calculate_time_to_leave(entry, lunch, back)

    today_warning = ""
    if not is_today:
        today_warning = "The last date in the table is not for today.\n"

    if estimate:
        leave_message = f"Assuming an one hour lunch, you should leave at {leave}."
    else:
        leave_message = f"You should leave at {leave}."

    return today_warning + leave_message
