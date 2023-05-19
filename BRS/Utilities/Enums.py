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
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("Enums.py")
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Enums
#====================================================================#
LoadingLog.Class("Dates")
class Dates(Enum):
    """
        Dates:
        ------
        Enumeration of possible dates to save. These dates types can
        be used to store types of dates into logs. The following
        dates type are stored in this enumeration:
        - `Creation`
        - `Current`
        - `Exit`
        - `Open`
        - `Updated`
    """
    Creation:str = "Creation"
    """Date corresponding to the creation of something."""
    Current:str = "Current"
    """Date corresponding to the current date."""
    Exit:str = "Exit"
    """Date corresponding to something's exiting."""
    Open:str = "Open"
    """Date corresponding to the opening of something or the loading of something."""
    Updated:str = "Updated"
    """Date corresponding to the updating of something."""

    def GetName(DateEnum:str) -> str:
        """
            GetName:
            --------
            Standard BRS enum function that takes a value from this
            enum as input parameter and returns the string representation
            of that value. Usually used for GUI displays.
        """
        if(DateEnum == Dates.Creation):
            return "Creation"
        if(DateEnum == Dates.Current):
            return "Current"
        if(DateEnum == Dates.Exit):
            return "Exit"
        if(DateEnum == Dates.Open):
            return "Open"
        if(DateEnum == Dates.Updated):
            return "Updated"
        return "No Match"
#====================================================================#
LoadingLog.Class("FileIntegrity")
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
        # try:
        #     match Integrity:
        #         case FileIntegrity.Ahead:
        #             return "Ahead"
        #         case FileIntegrity.Good:
        #             return "Good"
        #         case FileIntegrity.Blank:
        #             return "Blank"
        #         case FileIntegrity.Corrupted:
        #             return "Corrupted"
        #         case FileIntegrity.Outdated:
        #             return "Outdated"
        #         case FileIntegrity.Error:
        #             return "Error"
        #         case _:
        #             return "No Match"
        # except:
        if(Integrity == FileIntegrity.Ahead):
            return "Ahead"
        if(Integrity == FileIntegrity.Good):
            return "Good"
        if(Integrity == FileIntegrity.Blank):
            return "Blank"
        if(Integrity == FileIntegrity.Corrupted):
            return "Corrupted"
        if(Integrity == FileIntegrity.Outdated):
            return "Outdated"
        if(Integrity == FileIntegrity.Error):
            return "Error"
        return "No Match"
#====================================================================#
LoadingLog.Class("GitHubFail")
class GitHubFail(Enum):
    """
        GitHubFail:
        -----------
        This enumeration class is used to identify the type of error
        being returned from the GitHub API.
    """
    Good:int = 0
    """ GitHub function was successful. """
    LocalRepository:int = 1
    """ Failed to get local repository """
    User:int = 2
    """ The specified user did not exist, or an error occured while accessing it. """
    UserRepositories:int = 3
    """ Failed to get the specified user's repositories """
    MatchingRepository:int = 4
    """ No user repositories matched the local repository. """
    MatchingRepositoryTag:int = 5
    """ Failed to get tags from matching repository. """

    def GetName(Integrity:int) -> str:
        """
            GetName:
            --------
            Standard BRS enum function that takes a value from this
            enum as input parameter and returns the string representation
            of that value. Usually used for GUI displays.
        """
        # try:
        #     match Integrity:
        #         case FileIntegrity.Ahead:
        #             return "Ahead"
        #         case FileIntegrity.Good:
        #             return "Good"
        #         case FileIntegrity.Blank:
        #             return "Blank"
        #         case FileIntegrity.Corrupted:
        #             return "Corrupted"
        #         case FileIntegrity.Outdated:
        #             return "Outdated"
        #         case FileIntegrity.Error:
        #             return "Error"
        #         case _:
        #             return "No Match"
        # except:
        if(Integrity == FileIntegrity.Ahead):
            return "Ahead"
        if(Integrity == FileIntegrity.Good):
            return "Good"
        if(Integrity == FileIntegrity.Blank):
            return "Blank"
        if(Integrity == FileIntegrity.Corrupted):
            return "Corrupted"
        if(Integrity == FileIntegrity.Outdated):
            return "Outdated"
        if(Integrity == FileIntegrity.Error):
            return "Error"
        return "No Match"
#====================================================================#
LoadingLog.Class("Execution")
class Execution(Enum):
    """
        Execution:
        ==========
        Summary:
        --------
        This enum is used to define what happened when trying to
        execute a function.
        
        Members:
        --------
        - Good
        - Exception
        - Bad
    """

    Passed:int = 0
    """ The execution was successful. """

    Crashed:int = 1
    """ An exception occured. The execution failed through a try catch."""

    Failed:int = 2
    """ The execution simply failed. """

    NoConnection:int = 3
    """ The execution failed due to no connection available. Wether it's bluetooth or WiFi"""

    Incompatibility:int = 4
    """ The execution failed because there is an incompatibility issue that couldn't be resolved."""

    ByPassed:int = 5
    """ The execution was bypassed with NO ERRORS."""

    Unecessary:int = 6
    """ The execution was bypassed because there was no point in executing it."""
#====================================================================#
class VarTypes:
    """
        VarTypes:
        =========
        Summary:
        --------
        Holds definition of c variable
        types as struct compatible strings.
    """
    class Unsigned:
        Char:str = "B"
        Short:str = "H"
        Int:str = "I"
        Long:str = "L"
        LongLong:str = "Q"
    
    class Signed:
        Char:str = "b"

    Bool:str = "?"
    Char:str = "c"
    Short:str = "h"
    Int:str = "i"
    Long:str = "l"
    Longlong:str = "q"
    Float:str = "f"
    Double:str = "d"

LoadingLog.End("Enums.py")