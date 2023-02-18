#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from kivy.uix.screenmanager import Screen,ScreenManager
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

        Also contains the current language used by the application.
    """
    manager = ScreenManager()
#====================================================================#