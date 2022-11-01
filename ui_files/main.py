import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
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

conn = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="3278_GroupProject"
)
cursor = conn.cursor()

student_uid = "3037123459"
# temp for testing connection with mysql
time_now = datetime.today()

day_of_the_week = ["MON", "TUE", "WED", "THU", "FRI"]


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui", self)
        username = self.usernameInput_lineEdit_login.text()
        self.login_button_login.clicked.connect(self.login)

    def login(self):
        # MISSING: check if username in database
        # if (username in data base):
        # loginface = LoginFace()
        # widget.addWidget(loginface)
        # widget.setCurrentIndex(widget.currentIndex() + 1)
        # else:
        #    self.lineEdit.clear

        # TEMP: set to go to mainpage for simplicity
        mainpage = MainPage()
        widget.addWidget(mainpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginFace(QDialog):
    def __init__(self):
        super(LoginFace, self).__init__()
        loadUi("LoginFace.ui", self)
        # MISSING: face detection code


# NOTE: store login time into LoginHistory table
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
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            print(x, w, y, h)
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = frame[y : y + h, x : x + w]
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
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
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
                    print("The student", current_name, "is NOT FOUND in the database.")

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

                    hello = ("Hello ", current_name, "You did attendance today")
                    print(hello)
                    engine.say(hello)

            # If the face is unrecognized
            else:
                color = (255, 0, 0)
                stroke = 2
                font = cv2.QT_FONT_NORMAL
                cv2.putText(
                    frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA
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
        today = today.replace(hour=0, minute=0)

        for course in course_list:
            # for lectures
            # get all lecture info
            cursor.execute(
                'SELECT C.course_code, C.course_name, LT.start_time, LT.day_of_the_week FROM Course C, Lecture_timeslots LT WHERE C.course_code = LT.course_code AND C.course_code = "'
                + course[0]
                + '";'
            )
            lecture_info = cursor.fetchall()

            for timeslot in lecture_info:
                # only loop classes on the same week day
                if day_of_the_week[time_now.weekday()] != timeslot[3]:
                    continue

                # calculate time before class
                course_time = today + timeslot[2]
                time_diff = (course_time - time_now).seconds / 3600

                if time_diff <= 1:
                    have_class = True
                    curr_class = {
                        "mode": "lecture",
                        "code": timeslot[0],
                        "name": timeslot[1],
                        "time": timeslot[2],
                        "group": 0,
                    }
                    break

            if have_class:
                break

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
                "SELECT TT.course_code, C.course_name, TT.start_time, TT.day_of_the_week FROM Course C, Tutorial_timeslots TT WHERE TT.course_code = C.course_code AND TT.group_number = "
                + str(tutorial_gp_num)
                + ' AND C.course_code = "'
                + course[0]
                + '";'
            )

            tutorial_info = cursor.fetchall()[0]

            if day_of_the_week[time_now.weekday()] != tutorial_info[3]:
                continue

            # calculate time before class
            course_time = today + tutorial_info[2]
            time_diff = (course_time - time_now).seconds / 3600

            if time_diff <= 1:
                have_class = True
                curr_class = {
                    "mode": "tutorial",
                    "code": tutorial_info[0],
                    "name": tutorial_info[1],
                    "time": tutorial_info[2],
                    "group": tutorial_gp_num,
                }
                break

        # load CourseInfo page if have class
        # if have_class:
        curr_class = {
            "mode": "lecture",
            "code": "CCST9002-1A",
            "name": "Quantitative Literacy in Science, Technology and Society",
            "time": timedelta(hours=13, minutes=30),
            "group": 0,
        }  # testing
        if True:  # testing
            # load ui
            loadUi("CourseInfo.ui", self)

            # assign button event handler
            self.login_history_button_courseinfo.clicked.connect(self.gotoLoginHistory)
            # self.all_announcement_button_courseinfo.clicked.connect(
            #     self.gotoAnnouncement
            # )
            self.logout_button_courseinfo.clicked.connect(self.exiting)
            # self.email_button_courseinfo.clicked.connect(self.emailMe)

            # change welcome message
            self.welcome_message_label_courseinfo.setText("Welcome " + student_name)

            # change course code & name
            if curr_class["group"] == 0:
                self.course_code_label_courseinfo.setText(
                    curr_class["code"] + "    Lecture"
                )
            else:
                self.course_code_label_courseinfo.setText(
                    curr_class["code"] + "    Tutorial Gp" + str(curr_class["group"])
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

            # change course info

            self.course_info_list_courseinfo.setFont(QFont("Noto Sans CJK HK", 12))
            # self.course_info_list_courseinfo.setOpenExternalLinks(True)
            self.course_info_list_courseinfo.addItem(
                "Time: " + str(curr_class["time"])[:-3]
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
                    + ' AND ";'
                )

            link = cursor.fetchall()[0][0]

            self.course_info_list_courseinfo.addItem("Zoom Link: " + link)
            self.course_info_list_courseinfo.itemClicked.connect(self.zoom_link)
            # self.course_info_list_courseinfo.clicked.connect(self.link)

            # get insturctor info
            # get zoom link
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
                    + curr_class["group"]
                    + '";'
                )

            instruxtor_info = cursor.fetchall()[0]

            self.course_info_list_courseinfo.addItem(
                "Instructor: " + instruxtor_info[0]
            )
            self.course_info_list_courseinfo.addItem(
                "Instructor Email: " + instruxtor_info[1]
            )

        # load Timetable page if do NOT have class
        else:
            # load ui
            loadUi("Timetable.ui", self)

            # assign button event handler
            self.login_history_button_timetable.clicked.connect(self.gotoLoginHistory)
            self.logout_button_timetable.clicked.connect(self.exiting)

            # change welcome message
            self.welcome_message_label_timetable.setText("Welcome " + student_name)

    def gotoAnnouncement(self):
        announcement = Announcement()
        widget.addWidget(announcement)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLoginHistory(self):
        loginhistory = LoginHistory()
        widget.addWidget(loginhistory)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def exiting(self):
        print("Exiting")
        sys.exit(app.exec_())

    def zoom_link(self, clickedItem):
        if clickedItem.text()[0:10] == "Zoom Link:":
            webbrowser.open(clickedItem.text()[11:])

    # MISSING: email course info to student email
    # def emailMe(self):


class LoginHistory(QDialog):
    def __init__(self):
        super(LoginHistory, self).__init__()
        loadUi("LoginHistory.ui", self)
        self.main_page_button_loginhistory.clicked.connect(self.gotoMainPage)
        self.logout_button_loginhistory.clicked.connect(self.exiting)

    def gotoMainPage(self):
        mainpage = MainPage()
        widget.addWidget(mainpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def exiting(self):
        print("Exiting")
        sys.exit(app.exec_())


class Announcement(QDialog):
    def __init__(self):
        super(Announcement, self).__init__()
        loadUi("Announcement.ui", self)
        self.main_page_button_announcement.clicked.connect(self.gotoMainPage)
        self.login_history_button_announcement.clicked.connect(self.gotoLoginHistory)
        self.logout_button_announcement.clicked.connect(self.exiting)

    def gotoMainPage(self):
        mainpage = MainPage()
        widget.addWidget(mainpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoLoginHistory(self):
        loginhistory = LoginHistory()
        widget.addWidget(loginhistory)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def exiting(self):
        print("Exiting")
        sys.exit(app.exec_())

    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))


class LoginFace(QDialog):
    def __init__(self):
        super(LoginFace, self).__init__()
        StartFaceRecognition()

    def exiting(self):
        print("Exiting")
        sys.exit(app.exec_())


# main
# StartFaceRecognition()
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
# login = Login()
login = MainPage()
widget.addWidget(login)
widget.setFixedHeight(768)
widget.setFixedWidth(1024)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")

