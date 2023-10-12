import random
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal, QSize, QMetaObject, QCoreApplication
from PySide6.QtGui import QPainter, QPen, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(open("style.qss").read())

        self.ui.pushButton.clicked.connect(self.start_game)

        self.words = Words()

        self.start_game()

    def update_main_label(self, text):
        self.ui.label.setText(text)

    def analyse_word(self):
        dict = {}
        for i, char in enumerate(self.word):
            if char not in dict:
                dict[char] = []
            dict[char].append(i)
        return dict

    def start_game(self):
        try:
            self.ui.widget_2.new_key_typed.disconnect()
        except RuntimeError:
            pass
        self.ui.stackedWidget.setCurrentIndex(1)
        self.word = self.word_saved = self.words.get_new_random_word()
        self.analysed = self.analyse_word()
        self.word = "_" * len(self.word)
        self.ui.widget_3.setHangmanParts(0)
        self.update_main_label(self.word)

        self.ui.widget_2.new_key_typed.connect(self.new_char)
        self.ui.widget_2.enableAll()

    def lose(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.label_2.setText(f"Das Wort war: {self.word_saved}")

    def win(self):

        message = QMessageBox(parent=self, text="Du hast gewonnen!!!! Suppi")
        message.exec()
        self.start_game()


    def reveal(self):
        self.update_main_label(self.word_saved)

    def new_char(self, key):
        self.ui.widget_2.disableByKey(key)
        if key in self.analysed:
            for index in self.analysed[key]:
                self.word = self.word[:index] + key + self.word[index + 1:]
            self.update_main_label(self.word)
            if self.word == self.word_saved:
                self.win()
        else:
            self.ui.widget_3.setHangmanParts(self.ui.widget_3.hangman_parts + 1)
        if self.ui.widget_3.hangman_parts >= self.ui.widget_3.max_parts:


            self.lose()



class HangmanWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.hangman_parts = 0
        self.max_parts = 9


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.white, 2)
        painter.setPen(pen)

        if self.hangman_parts >= 1:
            painter.drawArc(100, 150, 100, 100, 0, 180 * 16)

        if self.hangman_parts >= 2:
            painter.drawLine(150, 150, 150, 50)

        if self.hangman_parts >= 3:
            painter.drawLine(150, 50, 225, 50)

        if self.hangman_parts >= 4:
            painter.drawLine(150, 75, 175, 50)

        if self.hangman_parts >= 5:
            painter.drawLine(225, 50, 225, 75)

        if self.hangman_parts >= 6:
            painter.drawEllipse(212.5, 75, 25,25)

        if self.hangman_parts >= 7:
            painter.drawLine(225, 100, 225, 150)

        if self.hangman_parts >= 8:
            painter.drawLine(225, 100, 212.5, 125)
            painter.drawLine(225, 100, 237.5, 125)

        if self.hangman_parts >= 9:
            painter.drawLine(225, 150, 210, 175)
            painter.drawLine(225, 150, 240, 175)

    def setHangmanParts(self, parts):
        self.hangman_parts = parts
        self.update()

class CustomKeyBoard(QWidget):
    new_key_typed = Signal(str)
    def __init__(self, parent):

        super().__init__(parent=parent)

        self.layout = QVBoxLayout(self)

        keyboard_layout = [
            "QWERTZUIOP",
            "ASDFGHJKL",
            "YXCVBNM",
        ]
        self.buttons = {}

        for row in keyboard_layout:
            row_layout = QHBoxLayout()
            for letter in row:
                button = QPushButton(letter)
                button.setObjectName("keyboard-buttons")
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)
                self.buttons[letter] = button
            self.layout.addLayout(row_layout)

    def on_button_click(self):
        sender = self.sender()
        if sender and isinstance(sender, QPushButton):
            letter = sender.text()
            self.new_key_typed.emit(letter.lower())

    def keyPressEvent(self, event):
        key = event.text().upper()
        if key in self.buttons:
            self.buttons[key].click()

    def enableAll(self):
        for button in self.buttons:
            self.buttons[button].setEnabled(True)

    def disableByKey(self, key:str):
        self.buttons[key.upper()].setEnabled(False)


class Words():
    def __init__(self, wordlist_path = None):
        if wordlist_path is None: wordlist_path = "wortliste.txt"
        self.lines = open(wordlist_path, "r", newline="\n").readlines()
        self.wordlist = [line.strip().lower() for line in self.lines]
    def get_new_random_word(self):
        return random.choice(self.wordlist)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 450)
        MainWindow.setMinimumSize(QSize(700, 450))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.page_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = HangmanWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")

        self.horizontalLayout.addWidget(self.widget_3)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.widget)

        self.widget_2 = CustomKeyBoard(self.page_2)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout_2.addWidget(self.widget_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_3 = QVBoxLayout(self.page_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.page_3)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2, 0, Qt.AlignHCenter)

        self.pushButton = QPushButton(self.page_3)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_3.addWidget(self.pushButton, 0, Qt.AlignHCenter)

        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
