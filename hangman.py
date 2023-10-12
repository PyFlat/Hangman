import random
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPen, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.words = Words()

        self.setWindowTitle("Hangman")
        self.setFixedSize(700, 450)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.upper_widget = QWidget()
        self.layout2 = QHBoxLayout()
        self.upper_widget.setLayout(self.layout2)

        self.drawWidget = HangmanWidget()
        self.layout2.addWidget(self.drawWidget)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label.setText("")
        font = QFont()
        font.setPixelSize(25)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 5)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.layout2.addWidget(self.label)

        self.layout.addWidget(self.upper_widget)

        self.keyboardWidget = KeyBoard()
        self.layout.addWidget(self.keyboardWidget)

        self.start_game()

    def update_main_label(self, text):
        self.label.setText(text)

    def analyse_word(self):
        dict = {}
        for i, char in enumerate(self.word):
            if char not in dict:
                dict[char] = []
            dict[char].append(i)
        return dict

    def start_game(self):
        self.word = self.words.get_new_random_word()
        self.analysed = self.analyse_word()
        self.word = "_" * len(self.word)
        self.update_main_label(self.word)

        self.keyboardWidget.new_key_typed.connect(self.new_char)
    def new_char(self, key):
        if key in self.analysed:
            for index in self.analysed[key]:
                self.word = self.word[:index] + key + self.word[index + 1:]
            self.update_main_label(self.word)
        else:
            self.drawWidget.setHangmanParts(self.drawWidget.hangman_parts + 1)
        if self.drawWidget.hangman_parts >= self.drawWidget.max_parts:
            self.drawWidget.setHangmanParts(0)
            self.keyboardWidget.new_key_typed.disconnect()
            self.start_game()

class HangmanWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.hangman_parts = 0
        self.max_parts = 9


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.black, 2)
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

class KeyBoard(QWidget):
    new_key_typed = Signal(str)
    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout(self)

        keyboard_layout = [
            "QWERTZUIOP",
            "ASDFGHJKL",
            "YXCVBNM",
        ]

        for row in keyboard_layout:
            row_layout = QHBoxLayout()
            for letter in row:
                button = QPushButton(letter)
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)
            self.layout.addLayout(row_layout)

    def on_button_click(self):
        sender = self.sender()
        if sender and isinstance(sender, QPushButton):
            letter = sender.text()
            self.new_key_typed.emit(letter.lower())

class Words():
    def __init__(self, wordlist_path = None):
        if wordlist_path is None: wordlist_path = "wortliste2.txt"
        self.lines = open(wordlist_path, "r", newline="\n").readlines()
        self.wordlist = [line.strip().lower() for line in self.lines]
    def get_new_random_word(self):
        return random.choice(self.wordlist)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
