#====================================================================#
# File Information
#====================================================================#
"""
    web.py
    =============
    This file contains function used to access different web
    functionalities.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
from ...Debug.consoleLog import Debug
LoadingLog.Start("web.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import requests
#endregion
#region --------------------------------------------------------- BRS
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
#endregion
#====================================================================#
# Functions
#====================================================================#
def IsWebsiteOnline(url:str = 'http://www.google.com/', timeout:int = 5):
    """
        IsWebsiteOnline:
        ----------------
        Function that automatically checks if a website can be accessed.
        url defaults to google.com and timeout defaults to 5.

        Returns:
            - `bool`: `True`: Website could not be accessed. `False`: Website could be accessed.
    """
    Debug.Start("IsWebsiteOnline")
    try:
        request = requests.head(url, timeout=timeout)
        # HTTP errors are not raised by default, this statement does that
        request.raise_for_status()
        Debug.Log("Website request was successful")
        Debug.End()
        return False
    except requests.HTTPError as exception:
        Debug.Error("Checking internet connection failed, status code {0}.".format(exception.response.status_code))
    except requests.ConnectionError:
        Debug.Error("No internet connection available.")
        Debug.End()
    return True
#====================================================================#
# Classes
#====================================================================#

# class Example:
#     #region   --------------------------- DOCSTRING
#     ''' This class is a reference style class which represents the current state that a device can be in.
#         A device can be GUI or hardware.
#         You don't have to use this class when defining the state of a device, but it is more convenient than
#         memorizing all the numbers associated by heart.
#     '''
#     #endregion
#     #region   --------------------------- MEMBERS
#     fakeVar : type = "sus"
#     ''' It's ugly docstring which for some annoying reason is below whatever it needs to explain... Which is hideous and hard to follow. No humans read data from bottom to top bruh.'''
#     #endregion
#     #region   --------------------------- METHODS
#     #endregion
#     #region   --------------------------- CONSTRUCTOR
#     #endregion
#     pass
#====================================================================#
LoadingLog.End("web.py")