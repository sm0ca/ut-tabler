"""CSC111 FINAL PROJECT: UT-TABLER

===============================

This is the main file that runs UT-Tabler from start to finish.

Copyright and Usage Information
===============================

This file is provided solely for the users of the UT-TABLER application.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Anbuselvan Ragunathan, Sanchaai Mathiyarasan, Yathusan Koneswararajah
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui_class import Program
from parse_functions import parse_course_options
import sys

if __name__ == "__main__":
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    course_options = parse_course_options()
    app = QApplication(sys.argv)
    widget = Program(course_options)
    widget.show()
    sys.exit(app.exec())
