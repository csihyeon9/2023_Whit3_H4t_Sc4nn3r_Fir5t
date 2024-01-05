# fuzzer.py
from logging_module import FuzzerLogger
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QCoreApplication
import time

class Fuzzer:
    def __init__(self, window_instance, url, logger_name="fuzzer_logger", log_file_path="fuzzer.log"):
        self.window_instance = window_instance
        self.url = url
        self.logger = FuzzerLogger(logger_name, log_file_path)
        self.cancelled = False
        self.current_payload_index = 0 
        self.current_vuln_count = 0

    def cancel_fuzzing(self):
        self.cancelled = True

    def extract_forms(self):
        self.logger.debug("Extracting forms from the target URL.")
    # 나머지 코드는 동일 
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find_all("form")


    def parse_forms(self, forms):  
        result = []
        for form in forms:
            try:
                form_data = {}
                form_data['action'] = form['action'] if form.has_attr('action') else None
                form_data['method'] = form['method'] if form.has_attr('method') else None
                form_data['inputs'] = [inputs for inputs in form.find_all('input')]
                result.append(form_data)
            except:  # 가져올게 없는 경우
                continue
        return result

    def fuzz(self, payloads, input_elem, method):
        total_payloads = len(payloads)

        # 추가: 중단된 페이로드의 인덱스부터 반복
        for i in range(self.current_payload_index, total_payloads):
            if self.cancelled:  # 추가: 스캔이 중지되었다면 루프 종료
                break

            script = payloads[i]
            self.current_vuln_count += 1  # 추가: 중단된 지점의 번호 증가
            self.window_instance.plainTextEdit.appendPlainText(f"[{self.current_vuln_count}] Testing script: {script}")

            if method.lower() == "get":
                response = requests.get(self.url, params={input_elem['name']: script}).text
            else:
                response = requests.post(self.url, data={input_elem['name']: script}).text

            if script in response:
                message = f"\n[+] Vulnerability found!\n"
                self.window_instance.show_vulnerability_message(message)

                cursor = self.window_instance.plainTextEdit.textCursor()
                cursor.setPosition(self.window_instance.previous_cursor_position)
                self.window_instance.plainTextEdit.setTextCursor(cursor)

            progress_value = int((i + 1) / total_payloads * 100)
            self.window_instance.progressBar.setValue(progress_value)

            # 추가: 일정 시간 동안 잠시 중지
            QCoreApplication.processEvents()
            time.sleep(0.1)

        # 추가: 모든 페이로드를 테스트했을 때 중단된 지점 업데이트
        self.current_payload_index = i + 1

    def perform_fuzzing(self, payloads):
        forms = self.extract_forms()
        parsed_forms = self.parse_forms(forms)

        self.window_instance.plainTextEdit.appendPlainText("\n===== Start scanning vulnerabilities =====\n")

        for form in parsed_forms:
            if self.cancelled:  # 추가: 스캔이 중지되었다면 루프 종료
                break

            try:
                method = form['method'].lower() if form['method'] else None
                inputs = form['inputs']
                for input_elem in inputs:
                    self.fuzz(payloads, input_elem, method)
                    # 추가: 중단된 지점 업데이트
                    QCoreApplication.processEvents()
            except:
                continue

        self.window_instance.plainTextEdit.appendPlainText("\n" + "="*42 + "\n\n")