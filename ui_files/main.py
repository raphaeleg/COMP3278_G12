import sys 
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("Login.ui", self)
        username = self.usernameInput_lineEdit_login.text()
        self.login_button_login.clicked.connect(self.login)
    
    def login(self):
        # MISSING: check if username in database
        #if (username in data base):
        # loginface = LoginFace()
        # widget.addWidget(loginface)
        # widget.setCurrentIndex(widget.currentIndex() + 1)
        #else:
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


class MainPage(QDialog):
    def __init__(self):
        super(MainPage, self).__init__()
        # MISSING: conditon for loading main page
        #if (1 hr before class):
        loadUi("CourseInfo.ui", self)
        #self.email_button_courseinfo.clicked.connect(self.emailMe)
        #else:
        #   loadUi("Timetable.ui", self)
        
        self.login_history_button_courseinfo.clicked.connect(self.gotoLoginHistory)
        self.all_announcement_button_courseinfo.clicked.connect(self.gotoAnnouncement)
        self.logout_button_courseinfo.clicked.connect(self.exiting)

    
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
        
    # MISSING: email course info to student email
    #def emailMe(self):
        


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


# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login = Login()
widget.addWidget(login)
widget.setFixedHeight(768)
widget.setFixedWidth(1024)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
