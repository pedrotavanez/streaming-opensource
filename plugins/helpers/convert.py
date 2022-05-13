#!/usr/bin/env python3
def convert(value, bw=False):
    if bw == True:
        magnitude_map = ["bits", "Kb", "Mb", "Gb", "Tb"]
        suffix = "/s"
    else:
        magnitude_map = ["bytes", "KB", "MB", "GB", "TB"]
        suffix = ""
    i = 0
    value = int(value)
    print(f"{value} {type(value)}")
    while value > 1000:
        value = value / 1000
        i = i + 1
    return f"{round(value, 3)} {magnitude_map[i]}{suffix}"