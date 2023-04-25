"""CSC111 FINAL PROJECT: UT-TABLER

===============================

This python module contains the class necessary to build the schedule tree.

Copyright and Usage Information
===============================

This file is provided solely for the users of the UT-TABLER application.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Anbuselvan Ragunathan, Sanchaai Mathiyarasan, Yathusan Koneswararajah
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class SectInfo:
    """A dataclass that contains all the necessary information for a section.
    Instance Attributes:
    - sect: A string representation of the section code
    - course: A string representation of the course code
    - instructors: A string containing all the instructors for the section
    - room_times: A dictionary that maps days of the week to a list of lists, with each sublist (which represnts a
                lecture) containing two tuples, the first containing a string of the lecture room number (or two strings
                for first and second semester room numbers, if the is year-long) and the second containing 2 floats to
                represent the start and end times of the lecture.
    """
    sect: str
    course: str
    instructors: str
    room_times: dict[str, list[list[tuple[str], tuple[float]]]]


class Schedule:
    """Schedule Tree
    Instance Attributes:
    - info: An instance of a SectInfo class that represents the information of the course (name, section, times, etc.)
    - sub_courses: A list of all the possible courses that come after the current course that we are at in the tree

    Representation Invariants:
    self.sect != ''
    self.course != ''
    self.instructors != ''
    self.room_times != {}
    """
    info: Optional[SectInfo]
    sub_courses: list[Schedule]

    def __init__(self, sect_info: Optional[SectInfo]) -> None:
        """
        This is the initializer for the Schedule class
        """
        self.info = sect_info
        self.sub_courses = []

    def add_sections(self, course_dict: dict[str, list[SectInfo]], course_names: list[str], prev_times: dict) -> None:
        """
        A recursive method that adds all the sections of a course in course_dict as sub_courses while ensuring each
        section does not conflict with any of the times from its ancestor sections. Before adding the newly created
        tree for each section to this trees sub_courses list, a recursive call is made on the newly created tree,
        passing in course_dict, the remaining courses to be added, and the dictionary of lecture times for this new
        tree's ancestor section, to populate its own sub_courses list. Does not do anything if there are no more courses
        left to be added in course_names.

        Preconditions:
        - course_dict != {}
        - course_names != []
        - prev_times != {}
        - all(lec.course == section for section in course_dict for lec in course_dict[section])
        """
        if course_names:
            sections = course_dict[course_names[0]]  # list[SectInfo]
            for section_info in sections:  # Each SectInfo object (should be turned into subtrees)
                sinfo_dict = section_info.room_times  # The rooms and times for the section
                times_dict = {day: [session[1] for session in sinfo_dict[day]]
                              for day in sinfo_dict}  # Just the times
                if not check_conflict(prev_times, times_dict):  # Check if conflict with any prev ones
                    new_prev = {day: prev_times[day] + times_dict[day] for day in sinfo_dict}
                    new_tree = Schedule(section_info)
                    new_tree.add_sections(course_dict, course_names[1:], new_prev)
                    self.sub_courses.append(new_tree)

    def accumulate_ttables(self) -> list[list[SectInfo]]:
        """
        A recursive method that collects a list of all possible "paths" through the tree by accumulating the SectInfo
        object for each section along each path. If the section has no sub_courses, it returns a list within a list
        which contains the section's SectInfo object. If the section's self.info attribute is None (meaning it is
        the root of the tree) then we only return the accumulation of the list of paths for its sub_courses, otherwise
        we return the list of paths for its subcourses, and prepend this section's SectInfo object to each before
        returning.
        """
        if not self.sub_courses:
            return [[self.info]]

        paths = []

        if self.info is None:
            for sec in self.sub_courses:
                paths.extend(sec.accumulate_ttables())
        else:
            for sec in self.sub_courses:
                paths.extend([[self.info] + path for path in sec.accumulate_ttables()])

        return paths


def check_conflict(day_time_1: dict[str, list[tuple[float, float]]],
                   day_time_2: dict[str, list[tuple[float, float]]]) -> bool:
    """
    A helper function for the Schedule class. Return whether there would be any overlapping time intervals if a
    dictionary of tuples (which represent time intervals for a course) were to be merged with another dictionary of
    tuples (which represnts time intervals for the course's ancestors). Return True if there are overlaps.
    Return False if there are no overlaps.

    Preconditions:
    - day_time_1 != {}
    - day_time_2 != {}
    """
    for day in day_time_1:
        for time1 in day_time_1[day]:
            for time2 in day_time_2[day]:
                if max(time1[0], time2[0]) < min(time1[1], time2[1]):
                    # Overlap spotted
                    return True
    # Overlap not spotted
    return False


if __name__ == '__main__':
    import doctest
    import python_ta
    doctest.testmod(verbose=True)
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['unused-import', 'too-many-branches', 'too-many-nested-blocks'],
    })
