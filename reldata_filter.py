import datetime as dt
import re

file = "/home/lfontoura/Downloads/rel.data-20180702/data"
output = "/home/lfontoura/Downloads/rel.data-20180702/filtered_data"
sep = "^_<+>_^"

start_dt = dt.datetime(2018, 6, 21, 16, 34, 21)
end_dt = dt.datetime(2018, 6, 21, 17, 10, 0)

date_pattern = re.compile(".* Jul (\d+) (\d+:\d+:\d+) .*")
output_lines = 0

with open(file, "r") as in_file, open(output, "w") as out_file:
    for line, notif in enumerate(in_file, 1):
        if line % 10000 == 0:
            print(f"Processing line {line}. Outputted {output_lines} lines.")

        properties = notif.split(sep)
        event_time = properties[1]
        date_string = event_time.split("=")[1]

        match = date_pattern.match(date_string)
        if match:
            day = match.group(1)
            time = match.group(2)
            hour, minutes, seconds = time.split(":")
            date = dt.datetime(2018, 7, int(day), int(hour), int(minutes), int(seconds))
            if start_dt <= date <= end_dt:
                output_lines += 1
                print(notif, file=out_file)
