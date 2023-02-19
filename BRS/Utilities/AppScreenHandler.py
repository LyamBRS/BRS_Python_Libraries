#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppScreenHandler.py")

from kivy.uix.screenmanager import Screen,ScreenManager
import os
import gettext
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class AppManager():
    """
        Static reference class used for screen building scripts to access
        the manager globally without 100000 references through input parameters.
    """
    manager = ScreenManager()
#====================================================================#
LoadingLog.End("AppScreenHandler.py")