import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import PySimpleGUI as sg
from datetime import datetime, timedelta
from PyQt5.QtGui import *
import webbrowser
import uuid
import os
import subprocess
from pathlib import Path

conn = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="3278_GroupProject"
)
cursor = conn.cursor(buffered=True)

student_uid = "3037123459"  # for testing
# student_uid = ""

login_time = datetime.today()


day_of_the_week = ["MON", "TUE", "WED", "THU", "FRI"]


class Login(QDialog):
    def __init__(self):
        global student_uid
        super(Login, self).__init__()
        self.capture = None

        loadUi("Login.ui", self)
        student_uid = self.usernameInput_lineEdit_login.text()
        self.login_button_login.clicked.connect(self.login)
        self.login_button_login.setStyleSheet(
            "background-color:#0B5563; color: white")

    def login(self):
        global student_uid
        student_uid = self.usernameInput_lineEdit_login.text()

        # MISSING: check if username in database
        cursor.execute(
            'SELECT student_name FROM Student WHERE student_uid = "'
            + student_uid
            + '";'
        )
        result = cursor.fetchall()
        # print(result)
        data = "error"

        for x in result:
            data = x

        # If the student's information is not found in the database
        if data == "error":
            # the student's data is not in the database
            print("The user " + student_uid +
                  " is NOT FOUND in the database.")
            self.usernameInput_lineEdit_login.clear()
        else:
            # student_uid = self.username.text();
            # loginface = ControlWindow()
            # widget.addWidget(loginface)
            # widget.setCurrentIndex(widget.currentIndex() + 1)
            if not self.capture:
                self.capture = QtCapture(0)
                # self.end_button.clicked.connect(self.capture.stop)
                # self.capture.setFPS(1)
                self.capture.setParent(self)
                self.capture.setWindowFlags(QtCore.Qt.Tool)
            self.capture.start()
            self.capture.show()


class LoginFace(QDialog):
    def __init__(self):
        super(LoginFace, self).__init__()
        loadUi("LoginFace.ui", self)
        # MISSING: face detection code

# to capture face and do face recognition


class QtCapture(QtWidgets.QWidget):
    def __init__(self, *args):
        super(QtWidgets.QWidget, self).__init__()

        global student_uid
        # 1 Create database connection
        self.myconn = mysql.connector.connect(
            host="localhost", user="root", passwd="flutterball55", database="3278_GroupProject"
        )
        self.date = datetime.utcnow()
        self.now = datetime.now()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.cursor = self.myconn.cursor()

        # 2 Load recognize and read label from model
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("./FaceRecognition/train.yml")

        self.labels = {"person_name": 1}
        with open("./FaceRecognition/labels.pickle", "rb") as f:
            self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}

        # create text to speech
        engine = pyttsx3.init()
        rate = engine.getProperty("rate")
        engine.setProperty("rate", 175)

        # Define camera and detect face
        self.fps = 24
        self.cap = cv2.VideoCapture(*args)
        self.gui_confidence = 40
        self.face_cascade = cv2.CascadeClassifier(
            './FaceRecognition/haarcascade/haarcascade_frontalface_default.xml')

        self.video_frame = QtWidgets.QLabel()
        lay = QtWidgets.QVBoxLayout()
        # lay.setMargin(0)
        lay.addWidget(self.video_frame)
        self.setLayout(lay)

        # ------ Modification ------ #
        self.ith_frame = 1
        # ------ Modification ------ #

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5)

        # ------ Modification ------ #
        # Save images if isCapturing
        for (x, y, w, h) in self.faces:
            print(x, w, y, h)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            # predict the id and confidence for faces
            id_, conf = self.recognizer.predict(roi_gray)

            # If the face is recognized
            if conf >= self.gui_confidence:
                print(id_)
                print(self.labels)
                font = cv2.QT_FONT_NORMAL
                id = 0
                id += 1
                name = self.labels[id_]
                current_name = name.split("_")[0]
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1,
                            color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (255, 0, 0), (2))
                # Find the student information in the database.
                select = "SELECT student_uid FROM Student WHERE student_uid='"+current_name+"'"
                name = cursor.execute(select)
                result = cursor.fetchall()
                # print(result)
                data = "error"

                for x in result:
                    data = x

                # If the student's information is not found in the database
                if data == "error":
                    # the student's data is not in the database
                    print("The student", current_name,
                          "is NOT FOUND in the database.")

                # If the student's information is found in the database
                else:
                    """
                    Implement useful functions here.
                    Check the course and classroom for the student.
                        If the student has class room within one hour, the corresponding course materials
                            will be presented in the GUI.
                        if the student does not have class at the moment, the GUI presents a personal class
                            timetable for the student.

                    """
                    # update = "UPDATE Student SET login_date=%s WHERE name=%s"
                    # val = (date, current_name)
                    # cursor.execute(update, val)
                    # update = "UPDATE Student SET login_time=%s WHERE name=%s"
                    # val = (current_time, current_name)
                    # cursor.execute(update, val)
                    # myconn.commit()

                    hello = ("Hello ", current_name,
                             "You did attendance today")
                    print(hello)
                    self.stop()
                    self.deleteLater()
                    main = MainPage()
                    widget.addWidget(main)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    break

            # If the face is unrecognized
            else:
                color = (255, 0, 0)
                stroke = 2
                font = cv2.QT_FONT_NORMAL
                cv2.putText(frame, "UNKNOWN", (x, y), font,
                            1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (255, 0, 0), (2))
                hello = ("Your face is not recognized")
                print(hello)
        self.ith_frame += 1
        # ------ Modification ------ #

        # My webcam yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(
            frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()
    # ------ Modification ------ #

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()


# NOTE: get login_time
def StartFaceRecognition():
    # 1 Create database connection
    myconn = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="3278_GroupProject"
    )
    date = datetime.utcnow()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cursor = myconn.cursor()

    # 2 Load recognize and read label from model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("FaceRecognition/train.yml")

    labels = {"person_name": 1}
    with open("FaceRecognition/labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    # create text to speech
    engine = pyttsx3.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 175)

    # Define camera and detect face
    face_cascade = cv2.CascadeClassifier(
        "FaceRecognition/haarcascade/haarcascade_frontalface_default.xml"
    )
    cap = cv2.VideoCapture(0)

    # 3 Define pysimplegui setting
    layout = [
        [
            sg.Text(
                "Setting",
                size=(18, 1),
                font=("Any", 18),
                text_color="#1c86ee",
                justification="left",
            )
        ],
        [
            sg.Text("Confidence"),
            sg.Slider(
                range=(0, 100),
                orientation="h",
                resolution=1,
                default_value=60,
                size=(15, 15),
                key="confidence",
            ),
        ],
        [sg.OK(), sg.Cancel()],
    ]
    win = sg.Window(
        "Attendance System",
        default_element_size=(21, 1),
        text_justification="right",
        auto_size_text=False,
    ).Layout(layout)
    event, values = win.Read()
    if event is None or event == "Cancel":
        exit()
    args = values
    gui_confidence = args["confidence"]
    win_started = False

    # 4 Open the camera and start face recognition
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            print(x, w, y, h)
            roi_gray = gray[y: y + h, x: x + w]
            roi_color = frame[y: y + h, x: x + w]
            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)

            # If the face is recognized
            if conf >= gui_confidence:
                # print(id_)
                # print(labels[id_])
                font = cv2.QT_FONT_NORMAL
                id = 0
                id += 1
                name = labels[id_]
                current_name = name
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1,
                            color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                # Find the student information in the database.
                select = (
                    "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'"
                    % (name)
                )
                name = cursor.execute(select)
                result = cursor.fetchall()
                # print(result)
                data = "error"

                for x in result:
                    data = x

                # If the student's information is not found in the database
                if data == "error":
                    # the student's data is not in the database
                    print("The student", current_name,
                          "is NOT FOUND in the database.")

                # If the student's information is found in the database
                else:
                    """
                    Implement useful functions here.
                    Check the course and classroom for the student.
                        If the student has class room within one hour, the corresponding course materials
                            will be presented in the GUI.
                        if the student does not have class at the moment, the GUI presents a personal class 
                            timetable for the student.

                    """
                    update = "UPDATE Student SET login_date=%s WHERE name=%s"
                    val = (date, current_name)
                    cursor.execute(update, val)
                    update = "UPDATE Student SET login_time=%s WHERE name=%s"
                    val = (current_time, current_name)
                    cursor.execute(update, val)
                    myconn.commit()

                    hello = ("Hello ", current_name,
                             "You did attendance today")
                    print(hello)
                    engine.say(hello)

            # If the face is unrecognized
            else:
                color = (255, 0, 0)
                stroke = 2
                font = cv2.QT_FONT_NORMAL
                cv2.putText(
                    frame, "UNKNOWN", (x,
                                       y), font, 1, color, stroke, cv2.LINE_AA
                )
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                hello = "Your face is not recognized"
                print(hello)
                engine.say(hello)
                # engine.runAndWait()

        # GUI
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        if not win_started:
            win_started = True
            layout = [
                [sg.Text("Attendance System Interface", size=(30, 1))],
                [sg.Image(data=imgbytes, key="_IMAGE_")],
                [
                    sg.Text("Confidence"),
                    sg.Slider(
                        range=(0, 100),
                        orientation="h",
                        resolution=1,
                        default_value=60,
                        size=(15, 15),
                        key="confidence",
                    ),
                ],
                [sg.Exit()],
            ]
            win = (
                sg.Window(
                    "Attendance System",
                    default_element_size=(14, 1),
                    text_justification="right",
                    auto_size_text=False,
                )
                .Layout(layout)
                .Finalize()
            )
            image_elem = win.FindElement("_IMAGE_")
        else:
            image_elem.Update(data=imgbytes)

        event, values = win.Read(timeout=20)
        if event is None or event == "Exit":
            break
        gui_confidence = values["confidence"]

    win.Close()
    cap.release()


class MainPage(QDialog):
    def __init__(self):
        super(MainPage, self).__init__()
        # get current time
        time_now = datetime.today().replace(day=2, hour=10, minute=00)

        # list of class for timetable
        class_list = []

        # get student name
        cursor.execute(
            'SELECT student_name FROM Student WHERE student_uid = "'
            + student_uid
            + '";'
        )
        student_name = cursor.fetchall()[0][0]

        # determine do they have class in 1 hr
        have_class = False
        cursor.execute(
            "SELECT course_code FROM StudentTakesCourse WHERE student_uid = "
            + student_uid
            + ";"
        )
        course_list = cursor.fetchall()

        # get today midnight for remainling time calculation
        today = datetime.today()
        today = today.replace(day=2, hour=0, minute=0)

        for course in course_list:
            # for lectures
            # get all lecture info
            cursor.execute(
                'SELECT C.course_code, C.course_name, LT.start_time, LT.day_of_the_week, LT.end_time FROM Course C, Lecture_timeslots LT WHERE C.course_code = LT.course_code AND C.course_code = "'
                + course[0]
                + '";'
            )
            lecture_info = cursor.fetchall()

            for timeslot in lecture_info:
                class_info = {
                    "mode": "lecture",
                    "code": timeslot[0],
                    "name": timeslot[1],
                    "start_time": timeslot[2],
                    "day": timeslot[3],
                    "end_time": timeslot[4],
                    "group": 0,
                }

                class_list.append(class_info)

                # only loop classes on the same week day
                if day_of_the_week[time_now.weekday()] != timeslot[3]:
                    continue

                # calculate time before class
                start_time = today + class_info["start_time"]
                end_time = today + class_info["end_time"]
                time_diff_start = (start_time - time_now).seconds / 3600
                time_diff_end = (end_time - time_now).seconds / 3600
                class_duration = (end_time - start_time).seconds / 3600

                if (time_diff_start <= 1) or (class_duration - time_diff_end > 0):
                    have_class = True
                    curr_class = class_info

            # for tutorials
            # get tutorial gp num
            cursor.execute(
                'SELECT group_number FROM StudentTakesCourse WHERE student_uid = "'
                + student_uid
                + '" AND course_code = "'
                + course[0]
                + '";'
            )

            tutorial_gp_num = cursor.fetchall()[0][0]

            if tutorial_gp_num == 0:
                continue

            # get tutorial info
            cursor.execute(
                "SELECT TT.course_code, C.course_name, TT.start_time, TT.day_of_the_week, TT.end_time FROM Course C, Tutorial_timeslots TT WHERE TT.course_code = C.course_code AND TT.group_number = "
                + str(tutorial_gp_num)
                + ' AND C.course_code = "'
                + course[0]
                + '";'
            )

            tutorial_info = cursor.fetchall()[0]

            class_info = {
                "mode": "tutorial",
                "code": tutorial_info[0],
                "name": tutorial_info[1],
                "start_time": tutorial_info[2],
                "day": tutorial_info[3],
                "end_time": tutorial_info[4],
                "group": tutorial_gp_num,
            }

            class_list.append(class_info)

            if day_of_the_week[time_now.weekday()] != tutorial_info[3]:
                continue

            # calculate time before class
            start_time = today + class_info["start_time"]
            end_time = today + class_info["end_time"]
            time_diff_start = (start_time - time_now).seconds / 3600
            time_diff_end = (end_time - time_now).seconds / 3600
            class_duration = (end_time - start_time).seconds / 3600

            if (time_diff_start <= 1) or (class_duration - time_diff_end > 0):
                have_class = True
                curr_class = class_info

        # load CourseInfo page if have class
        if have_class:
            # load ui
            loadUi("CourseInfo.ui", self)

            self.class_info = curr_class

            # assign button event handler
            self.login_history_button_courseinfo.clicked.connect(
                self.gotoLoginHistory)
            self.login_history_button_courseinfo.setStyleSheet(
                "background-color:#0B5563; color: white"
            )

            self.logout_button_courseinfo.clicked.connect(self.logout)
            self.logout_button_courseinfo.setStyleSheet(
                "background-color:#0B5563; color: white"
            )

            self.email_button_courseinfo.clicked.connect(self.emailMe)
            self.email_button_courseinfo.setStyleSheet(
                "background-color:#0B5563; color: white"
            )

            self.main_page_button_courseinfo.setStyleSheet(
                "background-color:#0B5563; color: white"
            )
            # change welcome message
            self.welcome_message_label_courseinfo.setText(
                "Welcome " + student_name)

            # get class info

            # get class info

            # change course code & name
            if curr_class["group"] == 0:
                self.course_code_label_courseinfo.setText(
                    curr_class["code"] + "    Lecture"
                )
            else:
                self.course_code_label_courseinfo.setText(
                    curr_class["code"] + "    Tutorial Gp" +
                    str(curr_class["group"])
                )

            self.course_name_label_courseinfo.setText(curr_class["name"])

            # change latest message (NOTE: message data need to have time)
            cursor.execute(
                'SELECT teacher_message FROM Course_teacher_message WHERE course_code = "'
                + curr_class["code"]
                + '" ORDER BY message_id DESC;'
            )

            lastest_message = cursor.fetchall()[0][0]

            self.latest_announcement_label_courseinfo.setText(lastest_message)
            self.class_info["message"] = lastest_message

            # change course info

            self.course_info_list_courseinfo.setFont(
                QFont("Noto Sans CJK HK", 12))
            # self.course_info_list_courseinfo.setOpenExternalLinks(True)
            self.course_info_list_courseinfo.addItem(
                "Time: "
                + str(curr_class["start_time"])[:-3]
                + " - "
                + str(curr_class["end_time"])[:-3]
            )

            # get venue
            if curr_class["mode"] == "lecture":
                cursor.execute(
                    'SELECT venue FROM Lecture WHERE course_code = "'
                    + curr_class["code"]
                    + '";'
                )
            else:
                cursor.execute(
                    'SELECT venue FROM Tutorial WHERE course_code = "'
                    + curr_class["code"]
                    + '";'
                )

            venue = cursor.fetchall()[0][0]

            self.course_info_list_courseinfo.addItem("Classroom: " + venue)
            self.class_info["venue"] = venue

            # get zoom link
            if curr_class["mode"] == "lecture":
                cursor.execute(
                    'SELECT zoom_links FROM Lecture_zoom_links WHERE course_code = "'
                    + curr_class["code"]
                    + '";'
                )
            else:
                cursor.execute(
                    'SELECT zoom_links FROM Tutorial_zoom_links WHERE course_code = "'
                    + curr_class["code"]
                    + '" AND group_number = '
                    + str(curr_class["group"])
                    + ";"
                )

            link = cursor.fetchall()[0][0]

            self.course_info_list_courseinfo.addItem("Zoom Link: " + link)
            self.course_info_list_courseinfo.itemClicked.connect(
                self.zoom_link)
            self.class_info["zoom_link"] = link.replace("\r", "")

            # get insturctor info
            if curr_class["mode"] == "lecture":
                cursor.execute(
                    'SELECT L.instructor_name, L.instructor_email FROM Lecturer L, LecturerTeachesLecture LTL WHERE L.instructor_id = LTL.instructor_id AND LTL.course_code = "'
                    + curr_class["code"]
                    + '";'
                )
            else:
                cursor.execute(
                    'SELECT T.instructor_name, T.instructor_email FROM Tutor T, TutorTeachesTutorial TTT WHERE T.instructor_id = TTT.instructor_id AND TTT.course_code = "'
                    + curr_class["code"]
                    + '" AND TTT.group_number = '
                    + str(curr_class["group"])
                    + ";"
                )

            instructor_info = cursor.fetchall()[0]

            self.course_info_list_courseinfo.addItem(
                "Instructor: " + instructor_info[0]
            )
            self.class_info["instructor_name"] = str(instructor_info[0])
            self.course_info_list_courseinfo.addItem(
                "Instructor Email: " + instructor_info[1]
            )
            self.class_info["instructor_email"] = str(instructor_info[1])

            # get course material links
            cursor.execute(
                'SELECT lecture_and_tutorial_notes FROM Course_lecture_and_tutorial_notes WHERE course_code = "'
                + curr_class["code"]
                # + "COMP3278-1A" #for testing
                + '";'
            )

            if cursor.rowcount > 0:
                note_link_temp = cursor.fetchall()
                note_link_list = []
                for note in note_link_temp:
                    temp = list(str(note[0]))
                    index = [0, 0]
                    count = 0
                    for i in range(len(temp)):
                        if temp[i] == "'":
                            index[count] = i
                            count += 1

                    note_link_list.append(
                        str("".join(temp[index[0] + 1: index[1]])
                            ).replace("\\r", "")
                    )

                self.note_link = note_link_list

                # set list font size
                self.material_list_courseinfo.setFont(
                    QFont("Noto Sans CJK HK", 12))

                # add material to list
                for i in range(len(self.note_link)):
                    self.material_list_courseinfo.addItem(
                        "Note" + str(i + 1) + ": " + self.note_link[i]
                    )

                self.material_list_courseinfo.itemClicked.connect(
                    self.material_link)

        # load Timetable page if do NOT have class
        else:
            # load ui
            loadUi("Timetable.ui", self)

            # assign button event handler
            self.login_history_button_timetable.clicked.connect(
                self.gotoLoginHistory)
            self.login_history_button_timetable.setStyleSheet(
                "background-color:#0B5563; color: white"
            )

            self.logout_button_timetable.clicked.connect(self.logout)
            self.logout_button_timetable.setStyleSheet(
                "background-color:#0B5563; color: white"
            )

            self.main_page_button_timetable.setStyleSheet(
                "background-color:#0B5563; color: white"
            )

            # change welcome message
            self.welcome_message_label_timetable.setText(
                "Welcome " + student_name)

            # set height of each row
            self.timetable_table.verticalHeader().setDefaultSectionSize(40)

            # get number of col and row
            col_num = self.timetable_table.columnCount()
            row_num = self.timetable_table.rowCount()

            # add class to timetable
            for class_ in class_list:
                # col = day of the week
                for c in range(col_num):
                    col = self.timetable_table.horizontalHeaderItem(c).text()

                    if class_["day"] != col:
                        continue

                    in_timetable = False

                    # row = time
                    for r in range(row_num):
                        row = self.timetable_table.verticalHeaderItem(r).text()

                        if str(class_["start_time"])[:-3] == row:
                            # show class code & mode in timtable
                            self.timetable_table.setItem(
                                r,
                                c,
                                QTableWidgetItem(
                                    class_["code"] + "\n" + class_["mode"]
                                ),
                            )

                            # change bg color of cell
                            self.timetable_table.item(r, c).setBackground(
                                QColor(82, 153, 211)
                            )
                            self.timetable_table.item(r, c).setForeground(
                                QBrush(QColor(255, 255, 255))
                            )
                            in_timetable = True

                        elif in_timetable:
                            end_time = list(str(class_["end_time"])[:-3])
                            end_time[3] = str(int(end_time[3]) + 1)
                            end_time = "".join(end_time)

                            if end_time == row:
                                break

                            self.timetable_table.setItem(
                                r, c, QTableWidgetItem(""),
                            )
                            self.timetable_table.item(r, c).setBackground(
                                QColor(82, 153, 211)
                            )

                    if in_timetable:
                        break

    def gotoAnnouncement(self):
        announcement = Announcement()
        widget.addWidget(announcement)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLoginHistory(self):
        loginhistory = LoginHistory()
        widget.addWidget(loginhistory)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logout(self):
        exiting(login_time)
        sys.exit(app.exec_())

    def zoom_link(self, clickedItem):
        if clickedItem.text()[0:10] == "Zoom Link:":
            webbrowser.open(clickedItem.text()[11:])

    def material_link(self, clickedItem):
        index = int(clickedItem.text()[4]) - 1
        path = Path(os.getcwd())
        webbrowser.open_new(os.getcwd().replace(
            "ui_files", "") + self.note_link[index])

    def emailMe(self):
        # set popup window
        msg = QMessageBox()
        msg.setWindowTitle("Email Me")
        msg.setText(
            self.class_info["code"]
            + "'s information and material have been emailed to you!"
        )

        # get student email
        cursor.execute(
            'SELECT email_address FROM Student WHERE student_uid = "'
            + student_uid
            + '";'
        )
        email_address = cursor.fetchall()[0][0]

        # construct email
        subject = (
            self.class_info["code"]
            + "'s "
            + self.class_info["mode"]
            + " information and materials"
        )
        subject = subject.replace(" ", "%20")  # replace white space

        materials = ""
        for i in range(len(self.note_link)):
            materials = (
                materials + "Note" + str(i + 1) +
                ": " + self.note_link[i] + "\n    "
            )

        email_content = f"""{self.class_info["code"]} {self.class_info["name"]} {self.class_info["mode"]}
    Message from Instructor: {self.class_info["message"]}

Course Information:
    Time: {self.class_info["start_time"]} - {self.class_info["end_time"]}
    Classroom: {self.class_info["venue"]}
    Zoom Link: {self.class_info["zoom_link"]}
    Instructor: {self.class_info["instructor_name"]}
    Instructor Email: {self.class_info["instructor_email"]}

Course Material (please download the materials in the ICMS system):
    {materials}
        """

        email_content = email_content.replace(" ", "%20")
        email_content = email_content.replace("\n", "%0A")
        email_content = email_content.replace("&", "%26")

        # show popup window
        x = msg.exec_()

        # send email through webbrowser
        webbrowser.open(
            "mailto:?to="
            + email_address
            + "&subject="
            + subject
            + "&body="
            + email_content,
            new=1,
        )


class LoginHistory(QDialog):
    def __init__(self):
        super(LoginHistory, self).__init__()
        loadUi("LoginHistory.ui", self)
        self.main_page_button_loginhistory.clicked.connect(self.gotoMainPage)
        self.main_page_button_loginhistory.setStyleSheet(
            "background-color:#0B5563; color: white"
        )
        self.logout_button_loginhistory.clicked.connect(self.logout)
        self.logout_button_loginhistory.setStyleSheet(
            "background-color:#0B5563; color: white"
        )

        self.login_history_button_loginhistory.setStyleSheet(
            "background-color:#0B5563; color: white"
        )

        # set col width
        self.login_hostory_table_loginhistory.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # hide row label
        self.login_hostory_table_loginhistory.verticalHeader().setVisible(False)

        # get login history from database
        cursor.execute(
            'SELECT login_time, logout_time FROM LoginHistory WHERE student_uid = "'
            + student_uid
            + '" ORDER BY login_time DESC;'
        )

        login_history_list = cursor.fetchall()

        for history in login_history_list:
            # add new row
            row = self.login_hostory_table_loginhistory.rowCount()
            self.login_hostory_table_loginhistory.insertRow(row)

            # add login time
            self.login_hostory_table_loginhistory.setItem(
                row, 0, QTableWidgetItem(str(history[0]))
            )

            # add logout time
            self.login_hostory_table_loginhistory.setItem(
                row, 1, QTableWidgetItem(str(history[1]))
            )

            # add duration
            self.login_hostory_table_loginhistory.setItem(
                row, 2, QTableWidgetItem(str(history[1] - history[0]))
            )

    def gotoMainPage(self):
        mainpage = MainPage()
        widget.addWidget(mainpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logout(self):
        exiting(login_time)
        sys.exit(app.exec_())


class LoginFace(QDialog):
    def __init__(self):
        super(LoginFace, self).__init__()
        StartFaceRecognition()


# fpr storeing login info when exit/logout
def exiting(login_time):
    logout_time = datetime.today()

    login_id = str(uuid.uuid4())

    # insert to database
    cursor.execute(
        'INSERT INTO LoginHistory VALUES ("'
        + str(login_id)
        + '", "'
        + student_uid
        + '", "'
        + str(login_time)
        + '", "'
        + str(logout_time)
        + '");'
    )

    conn.commit()

    print("Exiting")


# main
# StartFaceRecognition()
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login = Login()
# login = MainPage()
widget.addWidget(login)
widget.setFixedHeight(768)
widget.setFixedWidth(1024)
widget.show()

try:
    sys.exit(app.exec_())
except:
    exiting(login_time)
