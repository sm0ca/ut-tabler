"""CSC111 FINAL PROJECT: UT-TABLER

===============================

This python module contains the functions necessary to compute all possible
timetables given desired courses and user preferences for building proximity,
minimizing early classes, and minimizing late classes.

Copyright and Usage Information
===============================

This file is provided solely for the users of the UT-TABLER application.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Anbuselvan Ragunathan, Sanchaai Mathiyarasan, Yathusan Koneswararajah
"""

from math import cos
from parse_functions import parse_coordinates, parse_course_csv
from schedule_tree import Schedule, SectInfo


def get_ttables_ranked(wanted: set[str], ranks: list[int]) -> list[list[SectInfo]]:
    """
    This function takes in a list of desired courses and a list used to represent the user's prioritization of
    building proximity, minimizing early classes, and minimizing late classes. It then gets the corresponding
    course_dict associated with the wanted courses (which contains the info for each course), constructs a tree
    using course_dict, then gets possible paths and ranks them baased on user preference. It then returns the top
    15 timetables.
    """
    course_dict = parse_course_csv(wanted)
    tree = Schedule(None)
    course_names = list(course_dict.keys())
    tree.add_sections(course_dict, course_names,
                      {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': []})

    possible_ttables = [p for p in tree.accumulate_ttables() if len(p) == len(wanted)]
    possible_ttables.sort(key=lambda ttable: _compute_scores(ttable, ranks))
    return possible_ttables[:15]


def _compute_scores(path: list[SectInfo], ranks: list[int]) -> list[float, int]:
    """
    This function returns a list, in the order that corresponds to the users timetable preferences, that contains the
    average distance between consecutive lectures, the number of morning classes, and the number of evening classes.
    Due to the way that Python sorts lists, by ordering these three values based on user preference, when used as a key
    for sorting Python will first sort by the user's first choice, then use the second choice to break ties, and then
    finally the third choice to break further ties.

    Preconditions:
    - set(ranks) == {1, 2, 3}
    """

    master_room_times = _get_master_room_times(path)
    all_dists = set()
    # The first element represents avg dist between buildings, the second represents number of morning classes, and the
    # third represents the number of evening classes.
    lst_scores = [0] * 3
    for sem in master_room_times:
        for lst in sem.values():
            lst_scores[1] += sum(1 for time in lst if time[1][0] < 10.0)
            lst_scores[2] += sum(1 for time in lst if time[1][1] > 17.0)

            num_dists = len(lst) - 1
            for i in range(num_dists):
                start, end = lst[i][0][0].split()[0], lst[i + 1][0][0].split()[0]

                # NOTE, IF A BUILDING ISN'T AVAILABLE, WE ASSUME MAX DISTANCE BETWEEN BUILDINGS
                if 'NA' in (start, end) or not len(start) == len(end) == 2:
                    all_dists.add(1.1740529167842144)  # Computed maximum distance between buildings
                elif start == end:
                    all_dists.add(0.0)
                else:
                    # Uses the Equirectangular approximation formula to calculate distance, where:
                    # x = change in longitude * cos(mean latitude)
                    # y = change in latitude
                    # dist = earth's radius * sqrt(x^2 + y^2)

                    lat1, lon1, lat2, lon2 = parse_coordinates(start, end)
                    all_dists.add(6371 * (((lon2 - lon1) * cos((lat1 + lat2) / 2)) ** 2 + (lat2 - lat1) ** 2) ** 0.5)

    if not all_dists:
        lst_scores[0] = 0
    else:
        lst_scores[0] = sum(all_dists) / len(all_dists)

    return [lst_scores[ranks[0]], lst_scores[ranks[1]], lst_scores[ranks[2]]]


def _get_master_room_times(path: list[SectInfo]) -> list[dict[str, list[list[tuple[str | float]]]]]:
    """
    This function takes in a list of SectInfo objects (essentially a "path" through the Schedule tree), and returns two
    mappings (one for each semester) from days of the week to all lectures happening on each corresponding day
    (represented as a list of lists, each of which contains two tuples, one representing the room and the other
    representing the lecture times).
    """
    master = [{'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': []},
              {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': []}]
    legend = {'F': 0, 'S': 1}
    for sec in path:
        c_type = sec.course[-1]
        for day in sec.room_times:
            if c_type == 'Y':
                for i in range(2):
                    master[i][day].extend([[(j[0][i],), j[1]] for j in sec.room_times[day]])
            else:
                master[legend[c_type]][day].extend(sec.room_times[day])

    for i in range(2):
        for day in master[i]:
            master[i][day].sort(key=lambda rm_time: rm_time[1][0])
    return master


if __name__ == '__main__':
    import doctest
    import python_ta
    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['unused-import', 'too-many-branches', 'too-many-nested-blocks'],
    })
