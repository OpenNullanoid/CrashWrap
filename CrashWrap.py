# This Python file uses the following encoding: utf-8
import os
import sys
import subprocess
import copy

from datetime import datetime

# Responsible for providing variables for runtime of this program
from HandlerVars import *

# Qt Libraries
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QDesktopServices, QFontDatabase
from PySide6.QtCore import QUrl

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic CrashWrapUI.ui -o CrashWrapUI.py, or
#     pyside2-uic CrashWrapUI.ui -o CrashWrapUI.py
from CrashWrapUI import Ui_CrashHandler


class CrashHandlerUi(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_CrashHandler()
        self.ui.setupUi(self)

        self.ui.LogViewer.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

        self.ui.ExitButton.clicked.connect(sys.exit)  # Connects the exit button to exit fucnction

        self.ui.RestartButton.clicked.connect(self.restart_program)
        self.ui.LogsButton.clicked.connect(self.open_logs_folder)

    def show_window(self, main_error, sub_error, logs):
        self.setWindowTitle(f"{ProductName} has encountered a runtime error")
        self.ui.MainErrorLabel.setText(main_error)  # Display main error information
        self.ui.SubErrorLabel.setText(sub_error)  # Display explanation of the error
        self.ui.LogViewer.setPlainText(logs)  # Display logs to the user
        self.show()

    def open_logs_folder(self):
        QDesktopServices.openUrl(QUrl(LogsPath))

    def restart_program(self):
        self.hide()
        CrashHandlerMain.exec_program(self)


class CrashHandlerMain:
    ## This function creates a log file in the stated logging directory and then hands over the path of it.
    @staticmethod
    def create_log_file():
        try:
            # Create a directory to store log files if it doesn't exist
            log_dir = LogsPath
            os.makedirs(log_dir, exist_ok=True)

            # Generate a timestamped log file name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file_path = os.path.join(log_dir, f"log_{timestamp}.txt")

            return log_file_path
        except Exception as e:
            # Handle any exceptions that occur during file creation
            print(f"Error creating log file: {e}")
            return None

    ## This function loads currently working log file and returns it as a editable string.
    @staticmethod
    def load_log_file(log_file_path):
        try:
            # Loads the log file in read-only mode and returns it.
            with open(log_file_path, "r") as log_file:
                logs = log_file.read()
                return logs
        except Exception as e:
            return f"Unable to read the log file at: {log_file_path}"  # If failed, then just hand this string over.

    ## This function launches the program by its path and while running, it should try to write it's standard output and errors to the generated log.
    ## Once execution finishes, return the newly-written logs and error code.
    @staticmethod
    def launch_and_monitor(program_path):
        try:
            # Get the path for the log file
            log_file_path = CrashHandlerMain.create_log_file()
            if log_file_path is None:
                return -1, ""

            # Open the log file for writing
            with open(log_file_path, "w") as log_file:
                # Launch the external program
                process = subprocess.Popen(
                    program_path,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )

                # Wait for the program to finish
                process.communicate()

                return process.returncode, log_file_path
        except Exception as e:
            # Handle any exceptions that occur during execution
            return -1, ""

    ## This function analyzes the return code and then hands over the information about it from the HandlerVars.
    @staticmethod
    def handle_error_codes(return_code: int):
        for error_info in ErrorDetails:
            if error_info.code == return_code:
                return copy.deepcopy(error_info)

    ## This is responsible for executing and then retriving the standard output and error code and passes information over to the Qt window.
    @staticmethod
    def exec_program(widget):
        return_code, log_file_path = CrashHandlerMain.launch_and_monitor(BinaryPath)
        error = CrashHandlerMain.handle_error_codes(return_code)
        logs = CrashHandlerMain.load_log_file(log_file_path)

        if return_code != 0:
            if error is not None:
                widget.show_window(
                    f"{ProductName} has crashed with an {error.name} error",
                    f"{error.mean} (Error {error.code}). \nYou can report the logs to {DeveloperName} for further assistance. Read their documentation as to how to get started.",
                    logs,
                )
            else:
                widget.show_window(
                    f"{ProductName} has crashed with an unexpected error",
                    f"Exit code: {return_code}. \nYou can report the logs to {DeveloperName} for further assistance. Read their documentation as to how to get started.",
                    logs,
                )
        else:
            sys.exit(0)


## Execution loop. Should not have too many functions here and instead should call from the CrashHandlerMain instead
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CrashHandlerUi()

    CrashHandlerMain.exec_program(widget)
    sys.exit(app.exec())
