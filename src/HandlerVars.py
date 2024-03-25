# This Python file uses the following encoding: utf-8
from dataclasses import dataclass

# This is a dataclass for handling the various types of Error Information.
# Each of these will contain a formalized name, the exit code corresponding to it and the meaning of it.
@dataclass
class ErrorInfo:
    name: str = ""
    code: int = 0
    mean: str = ""


# Here are the crash handler error configuration options.
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
