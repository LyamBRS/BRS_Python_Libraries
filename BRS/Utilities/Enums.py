#====================================================================#
# File Information
#====================================================================#
"""
    Enums.py
    ========
    This python file contains generic enumations which should be used
    as much as possible by BRS applications. They are created to remove
    the need to parse a string as returned values or input parameters,
    which takes a lot of processing power for no reasons other than
    readability.

    These are not real enumerations like you would find in a C/C#/C++
    application. They are simply classes filled with members which are
    equal to a value. The returned value in terms no longer matter because
    the application will only be comparing numbers instead of entire strings.
"""
#====================================================================#
# Imports
#====================================================================#
from enum import Enum
# from ..Debug.LoadingLog import LoadingLog
# LoadingLog.Start("Enums.py")
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Enums
#====================================================================#
class FileIntegrity(Enum):
    """
        Enumeration of possible results of an integrity check on any
        given file. This is the resulted value from functions that
        check if a file complies with a wanted format and is usable.
    """
    Good:int = 0
    """ The file passed the integrity check """
    Blank:int = 1
    """ The file was empty """
    Corrupted:int = 2
    """ The file contains corrupted or unexpected data """
    Ahead:int = 3
    """ The file's version is ahead of what was expected """
    Outdated:int = 4
    """ The file's version is behind what was expected """
    Error:int = 5
    """ A fatal error occured while checking the file's integrity """

    def GetName(Integrity:int) -> str:
        """
            GetName:
            --------
            Standard BRS enum function that takes a value from this
            enum as input parameter and returns the string representation
            of that value. Usually used for GUI displays.
        """
        match Integrity:
            case FileIntegrity.Ahead:
                return "Ahead"
            case FileIntegrity.Good:
                return "Good"
            case FileIntegrity.Blank:
                return "Blank"
            case FileIntegrity.Corrupted:
                return "Corrupted"
            case FileIntegrity.Outdated:
                return "Outdated"
            case FileIntegrity.Error:
                return "Error"
            case _:
                return "No Match"
#====================================================================#

# LoadingLog.End("Enums.py")