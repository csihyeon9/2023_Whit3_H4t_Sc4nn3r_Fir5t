import sys
from PyQt5.QtWidgets import QApplication
from gui_module import WindowClass
from logging_module import FuzzerLogger
if __name__ == "__main__":
    logger = FuzzerLogger(logger_name="gui_logger", log_file_path="gui.log")

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()

    logger.info("Application started.")
    
    sys.exit(app.exec_())