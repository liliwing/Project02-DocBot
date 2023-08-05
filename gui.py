import os.path as osp
import requests
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

SERVER_IP = "http://localhost:5000"

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("GUI")
        self.setMinimumSize(QSize(800, 400))

        # File Picker
        self.filename = QLineEdit()
        self.filename.setPlaceholderText("Select a file ...")
        self.filename.setReadOnly(True)
        self.select_btn = QPushButton("Browse")
        self.select_btn.clicked.connect(self._handle_select_btn_onClick)
        file_picker_layout = QHBoxLayout()
        file_picker_layout.addWidget(self.filename)
        file_picker_layout.addWidget(self.select_btn)

        # Question
        self.question = QLineEdit()
        self.ask_btn = QPushButton("Ask")
        self.ask_btn.clicked.connect(self._handle_ask_btn_onClick)
        question_layout = QHBoxLayout()
        question_layout.addWidget(self.question)
        question_layout.addWidget(self.ask_btn)

        # Answer
        self.answer = QPlainTextEdit()
        self.answer.setReadOnly(True)

        # Create Form
        main_layout = QFormLayout()
        main_layout.addRow(QLabel("File"), file_picker_layout)
        main_layout.addRow(QLabel("Question"), question_layout)
        main_layout.addRow(QLabel("Answer"), self.answer)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _handle_select_btn_onClick(self):
        filename, ret = QFileDialog.getOpenFileName(self, "Select a File")
        if filename:
            self.filename.setText(filename)
            # Upload file to server
            requests.post(f"{SERVER_IP}/upload", files={"file": open(filename, "rb")})

    def _handle_ask_btn_onClick(self):
        filename = self.filename.text()
        question = self.question.text()
        if filename and question:
            response = requests.post(f"{SERVER_IP}/ask", json={
                "filename": osp.basename(filename), "question": question
            })
            data = response.json()
            answer = data["answer"]
            self.answer.setPlainText(answer)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
