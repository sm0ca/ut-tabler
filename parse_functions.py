"""CSC111 FINAL PROJECT: UT-TABLER

===============================

This python module contains the functions necessary to parse building_info.csv
and course_info.csv.

Copyright and Usage Information
===============================

This file is provided solely for the users of the UT-TABLER application.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Anbuselvan Ragunathan, Sanchaai Mathiyarasan, Yathusan Koneswararajah
"""
from math import radians
from schedule_tree import SectInfo


def parse_coordinates(start: str, end: str) -> list[float]:
    """
    A function that parses "building_info.csv" to get the latitudes and longitudes (in radians) of the start and end
    locations that are provided as arguments.
    """
    coordinates = []
    with open("data/building_info.csv", "r") as file:
        for row in file:
            if row[:2] in (start, end):
                cols = row.strip().split('|')
                coordinates.append(radians(float(cols[1])))
                coordinates.append(radians(float(cols[2])))
            if len(coordinates) == 4:
                return coordinates
    return [0, 0, 0, 0]


def parse_course_csv(wanted: set[str]) -> dict[str, list[SectInfo]]:
    """
    A function that parses course_info.csv in order to obtain information about each course in the wanted list. A
    mapping from course code to a list of SectInfo objects, each of which contains information such as section code,
    course code, instructors, etc. for a section that corresponds to the course code key, is returned.
    """
    course_dict = {crs: [] for crs in wanted}
    with open("data/course_info.csv", "r") as file:
        for row in file:
            if row[:10] not in wanted:
                continue
            cols = row.strip().split("|")
            course_code = cols[0]
            section_code = cols[1]
            instructors = cols[2]

            days = cols[3].split("!")
            room_times = {'Mon': days[0], 'Tue': days[1], 'Wed': days[2], 'Thu': days[3], 'Fri': days[4]}
            for day in room_times:
                if room_times[day] == '###':
                    room_times[day] = []
                    continue
                room_times[day] = room_times[day].split('+')
                for i in range(len(room_times[day])):
                    room_times[day][i] = room_times[day][i].split('$')
                    room_times[day][i][0] = tuple(room_times[day][i][0].split(';'))

                    room_times[day][i][1] = room_times[day][i][1].split('~')
                    room_times[day][i][1][0] = [int(j) for j in room_times[day][i][1][0].split(':')]
                    room_times[day][i][1][0] = room_times[day][i][1][0][0] + room_times[day][i][1][0][1] / 60
                    room_times[day][i][1][1] = [int(j) for j in room_times[day][i][1][1].split(':')]
                    room_times[day][i][1][1] = room_times[day][i][1][1][0] + room_times[day][i][1][1][1] / 60

                    room_times[day][i][1] = tuple(room_times[day][i][1])

            course_dict[course_code].append(SectInfo(section_code, course_code, instructors, room_times))

    return course_dict


def parse_course_options() -> list[str]:
    """
    A function that returns a list of every unique course code in course_info.csv.
    """
    with open("data/course_info.csv", "r") as file:
        course_options = {row[:10] for row in file}
        course_options = list(course_options)
        course_options.sort()
    return course_options


if __name__ == '__main__':
    import doctest
    import python_ta
    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['math', 'schedule_tree'],
        'disable': ['unused-import', 'too-many-branches', 'too-many-nested-blocks'],
        'allowed-io': ['SectInfo']
    })
