# logging_module.py

import logging

class FuzzerLogger:
    def __init__(self, logger_name, log_file_path):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # 파일 핸들러를 통한 로깅 설정
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # 콘솔 핸들러를 통한 로깅 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # 이 부분을 DEBUG로 변경

        # 포매터 설정
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 핸들러 추가
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)