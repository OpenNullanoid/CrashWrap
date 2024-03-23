# This Python file uses the following encoding: utf-8
from dataclasses import dataclass

print("Exec B4 Vars")


# This is a dataclass for handling the various types of Error Information.
# Each of these will contain a formalized name, the exit code corresponding to it and the meaning of it.
@dataclass
class ErrorInfo:
    name: str = ""
    code: int = 0
    mean: str = ""


# Here are the crash handler configuration options.
ProductName = "Program"  # Here you specify the formalized name of the program.
DeveloperName = (
    "Developer"  # Here you specify the name of the developer of the program.
)
BinaryPath = "/bin/echo 0"  # Here you specify the startup path for the executable.
LogsPath = "./logs/"  # Here you can specify where to keep logs for it.
Version = "0.0.0.0"  # Here you specify the Version of the program.

# Here you can put in information for the specific exit codes.
ErrorDetails = []
ErrorDetails.append(
    ErrorInfo(
        "Segmentation Fault",
        -11,
        "This means that the program failed to manage memory properly",
    )
)
ErrorDetails.append(
    ErrorInfo(
        "Illegal Hardware Instruction",
        -4,
        "This means that the program tried executing code which is not supported by the CPU",
    )
)
