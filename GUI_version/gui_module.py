from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor
from PyQt5 import uic
import sys

# UI 파일 연결
form_class = uic.loadUiType("gui_module2.ui")[0]

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui_module2.ui", self)
        self.progressBar.setValue(0)
        self.pushButton.clicked.connect(self.read_payload)
        self.pushButton_3.clicked.connect(self.scan_startorstop)
        self.vuln_count = 0 
        self.plainTextEdit.setStyleSheet("background-color: white;")
        self.previous_cursor_position = 0
        self.pushButton_2.clicked.connect(self.save_text)
        self.payloads = None  # Initialize
        self.scan_running = False
    
    def scan_startorstop(self):
        if not self.scan_running:
            self.pushButton_3.setText("Stop")
            self.scan_start()
        else:
            self.pushButton_3.setText("Start")
            self.scan_stop()
        
    def save_text(self):
        # Open a file dialog to choose the save location
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text files (*.txt)")

        if file_path:
            # Get the plain text content from plainTextEdit
            text_content = self.plainTextEdit.toPlainText()

            # Save the text content to the selected file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_content)

            # Inform the user that the file has been saved
            self.statusBar().showMessage(f"Text saved to {file_path}")

    def read_payloads_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
        
    def read_payload(self):
        self.progressBar.setValue(0)

         # Payload 읽기
        payloads_file, _ = QFileDialog.getOpenFileName(self, "Select a wordlist for fuzzing", "", "Text files (*.txt)")
        if not payloads_file:
            self.plainTextEdit.setPlainText("Fuzzing aborted: No wordlist selected.")
            return

        self.label_4.setText(f"Loaded File: {payloads_file}")
        self.payloads = self.read_payloads_from_file(payloads_file)

    def scan_start(self):
        self.progressBar.setValue(0)
        self.scan_running = True
        url = self.lineEdit.text()

        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading)
        self.loading_timer.start(100)

        # default payload
        if self.payloads is None:
            default_payload_file = "xss_vectors.txt"
            self.payloads = self.read_payloads_from_file(default_payload_file)

        # Send the parameters to the fuzzer module
        from fuzzer_module import Fuzzer
        self.fuzzer_instance = Fuzzer(self, url)
        self.fuzzer_instance.perform_fuzzing(self.payloads)

    def scan_stop(self):
        if self.scan_running and hasattr(self, 'fuzzer_instance') and self.fuzzer_instance is not None:
            self.scan_running = False
            self.fuzzer_instance.cancel_fuzzing()

    def show_vulnerability_message(self, message):
        # QTextCharFormat - 텍스트 스타일 지정
        format = QTextCharFormat()
        format.setForeground(QColor("red"))

        # QTextCursor - 현재 텍스트 커서 설정
        cursor = self.plainTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)

        # 현재 커서 위치 저장
        self.previous_cursor_position = cursor.position()

        cursor.insertText(message, format)
        cursor.insertBlock()  

        # 새로운 색상 적용된 텍스트 표시
        self.plainTextEdit.setTextCursor(cursor)

    def getSelectedRadioButton(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() and item.widget().isChecked():
                return item.widget().text()

    def update_loading(self):
        current_value = self.progressBar.value()
        if current_value >= 100:
            self.loading_timer.stop()
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()