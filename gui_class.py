"""CSC111 FINAL PROJECT: UT-TABLER

===============================

This is the file which contains the graphic user interface code for the UT-TABLER application.
This file uses a class to create a window using pyQt5 which allows the user to select desired courses
and rank their preference for generating timetables. After generating, the timetables are displayed and they
can be looked through by pressing the next and prev buttons.

Copyright and Usage Information
===============================

This file is provided solely for the users of the UT-TABLER application.
All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Anbuselvan Ragunathan, Sanchaai Mathiyarasan, Yathusan Koneswararajah
"""

import time
from typing import Optional
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QSplashScreen
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView


from tree_computations import get_ttables_ranked
from table_visualization import make_timetable


class Program(QWidget):
    """Class for window of GUI"""

    def __init__(self, wordlist: list, parent: Optional[QWidget] = None) -> None:
        QWidget.__init__(self, parent)
        self.wordlist = wordlist
        self.pref_rank = [0, 0, 0]
        self.index = 0

        self.resize(1000, 667)
        self.setWindowTitle("UT-Tabler")
        self.setWindowIcon(QIcon('assets/icon.svg'))

        image = QPixmap('assets/logo.svg')
        splash = QSplashScreen(image, Qt.WindowStaysOnTopHint)
        splash.resize(int(1920 * .5), int(1080 * .5))
        splash.show()
        time.sleep(1)
        splash.close()

        self.title = QLabel(self)
        self.title.setText("Welcome to the UT-Tabler!")
        self.title.setFont(QFont('Helvetica', 30))
        self.title.move(int(1920 * .15), int(1080 * .001))

        self.desc = QLabel(self)
        self.desc.setText("Select the courses you want to enroll in and possible timetables will be generated")
        self.desc.setFont(QFont('Helvetica', 14))
        self.desc.move(int(1920 * .008), int(1080 * .05))

        self.selectedc = set()
        self.cb = QComboBox(self)
        self.cb.addItems(self.wordlist)
        self.cb.setEditable(True)
        self.cb.resize(int(1920 * .1), int(1080 * .05))
        self.cb.move(int(1920 * .008), int(1080 * .1))

        self.select_lbl = QLabel(self)
        self.select_lbl.setText("Selected Courses: ")
        self.select_lbl.setFont(QFont('Helvetica', 12))
        self.select_lbl.move(int(1920 * .008), int(1080 * .2))

        self.addbtn = QPushButton(self)
        self.addbtn.setText("Add Course")
        self.addbtn.move(int(1920 * .12), int(1080 * .1))
        self.addbtn.resize(int(1920 * .1), int(1080 * .05))
        self.addbtn.setStyleSheet("background-color: lightgray")
        self.addbtn.clicked.connect(self.course_select)

        self.clrbtn = QPushButton(self)
        self.clrbtn.setText("Clear Courses")
        self.clrbtn.move(int(1920 * .008), int(1080 * .23))
        self.clrbtn.resize(int(1920 * .1), int(1080 * .05))
        self.clrbtn.setStyleSheet("background-color: lightgray")
        self.clrbtn.clicked.connect(self.clear_selected)

        self.pref_lbl = QLabel(self)
        self.pref_lbl.setText("Rank Your Preferences:")
        self.pref_lbl.setFont(QFont('Helvetica', 10))
        self.pref_lbl.move(int(1920 * .008), int(1080 * .3))

        self.build_dis = QLabel(self)
        self.build_dis.setText("Minimize Distances Between Buildings")
        self.build_dis.setFont(QFont('Helvetica', 10))
        self.build_dis.move(int(1920 * .03), int(1080 * .32))

        self.rank1 = QComboBox(self)
        self.rank1.addItems(['1', '2', '3'])
        self.rank1.move(int(1920 * .008), int(1080 * .32))

        self.early = QLabel(self)
        self.early.setText("Minimize Classes That Start Early")
        self.early.setFont(QFont('Helvetica', 10))
        self.early.move(int(1920 * .03), int(1080 * .35))

        self.rank2 = QComboBox(self)
        self.rank2.addItems(['2', '1', '3'])
        self.rank2.move(int(1920 * .008), int(1080 * .35))

        self.late = QLabel(self)
        self.late.setText("Minimize Classes That Start Late")
        self.late.setFont(QFont('Helvetica', 10))
        self.late.move(int(1920 * .03), int(1080 * .38))

        self.rank3 = QComboBox(self)
        self.rank3.addItems(['3', '2', '1'])
        self.rank3.move(int(1920 * .008), int(1080 * .38))

        self.subbtn = QPushButton(self)
        self.subbtn.setText("Submit")
        self.subbtn.move(int(1920 * .008), int(1080 * .43))
        self.subbtn.resize(int(1920 * .1), int(1080 * .05))
        self.subbtn.setStyleSheet("background-color: lightgray")
        self.subbtn.clicked.connect(self.submit_courses)

        self.err_lbl = QLabel(self)
        self.err_lbl.setText('')
        self.err_lbl.setFont(QFont('Helvetica', 10))
        self.err_lbl.setStyleSheet("QLabel { color : red; }")
        self.err_lbl.move(int(1920 * .008), int(1080 * .48))

    def course_select(self) -> None:
        """Function which adds a course to the list after selecting on the combobox, self.cb"""
        self.selectedc.add(self.cb.currentText())
        self.select_lbl.setText("Selected Courses: " + ', '.join(self.selectedc))
        self.select_lbl.adjustSize()

    def clear_selected(self) -> None:
        """Function which clears the selected courses label, select_lbl"""
        self.selectedc.clear()
        self.select_lbl.setText("Selected Courses: ")
        self.select_lbl.adjustSize()

    def submit_courses(self) -> None:
        """Function that sends the chosen courses and preferences to the backend"""
        if len(self.selectedc) < 1:
            self.err_lbl.setText('Please choose at least 1 course')
            self.err_lbl.adjustSize()

            return None

        elif (self.rank3.currentText() == self.rank2.currentText()
              or self.rank1.currentText() == self.rank3.currentText()
              or self.rank1.currentText() == self.rank2.currentText()):
            self.err_lbl.setText('Please rank preferences with no repeating ranks')
            self.err_lbl.adjustSize()

            return None

        self.ttables = get_ttables_ranked(self.selectedc, self.pref_rank)
        if not self.ttables:
            self.err_lbl.setText('These courses conflict with each other, please try again')
            self.err_lbl.adjustSize()

            return None

        self.pref_rank[int(self.rank1.currentText()) - 1] = 0
        self.pref_rank[int(self.rank2.currentText()) - 1] = 1
        self.pref_rank[int(self.rank3.currentText()) - 1] = 2

        self.desc.deleteLater()
        self.cb.deleteLater()
        self.select_lbl.deleteLater()
        self.addbtn.deleteLater()
        self.clrbtn.deleteLater()
        self.pref_lbl.deleteLater()
        self.build_dis.deleteLater()
        self.rank1.deleteLater()
        self.rank2.deleteLater()
        self.rank3.deleteLater()
        self.early.deleteLater()
        self.late.deleteLater()
        self.subbtn.deleteLater()
        self.err_lbl.deleteLater()

        self.show_timetable()

        return None

    def show_timetable(self) -> None:
        """Generates and displays a timetable"""
        self.title.setText(f"Timetable {str(self.index + 1)}/{len(self.ttables)}")
        self.title.move(int(1920 * .2), int(1080 * .001))

        self.view = QWebEngineView()

        self.next = QPushButton(self)
        self.next.setText("Next")
        self.next.move(int(1920 * .45), int(1080 * .001))
        self.next.resize(int(1920 * .05), int(1080 * .05))
        if self.index < len(self.ttables) - 1:
            self.next.setStyleSheet("background-color: green")
        else:
            self.next.setStyleSheet("background-color: lightgray")
        self.next.clicked.connect(self.press_next)
        self.next.show()

        self.prev = QPushButton(self)
        self.prev.setText("Prev")
        self.prev.move(int(1920 * .008), int(1080 * .001))
        self.prev.resize(int(1920 * .05), int(1080 * .05))
        if self.index > 0:
            self.prev.setStyleSheet("background-color: green")
        else:
            self.prev.setStyleSheet("background-color: lightgray")
        self.prev.clicked.connect(self.press_prev)
        self.prev.show()

        make_timetable(self.ttables[self.index])
        with open('timetable.htm', 'r') as f:
            html = f.read()
            self.view.setHtml(html)

        self.view.resize(700, 500)
        self.view.show()

    def press_next(self) -> None:
        """Method of the next button when viewing timetables which shows the next timetable to user
        Preconditions:
        - 0 <= self.index <= len(self.ttables)
        """
        if self.index < len(self.ttables) - 1:
            self.view.close()
            self.index += 1
            self.show_timetable()

    def press_prev(self) -> None:
        """Method of the prev button when viewing timetables which shows the previous timetable to user
        Preconditions:
        - 0 <= self.index <= len(self.ttables)
        """
        if self.index > 0:
            self.view.close()
            self.index -= 1
            self.show_timetable()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
