#====================================================================#
# File Information
#====================================================================#
"""
    AppLoading.py
    =============
    This file is used to control and coordinate the loading of the
    application's various things. It uses a list of things to do where
    each element is paired with a function that returns `True` if an
    error occured and `False` if that loading step was successful.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from .BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Example:
    #region   --------------------------- DOCSTRING
    ''' This class is a reference style class which represents the current state that a device can be in.
        A device can be GUI or hardware.
        You don't have to use this class when defining the state of a device, but it is more convenient than
        memorizing all the numbers associated by heart.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    fakeVar : type = "sus"
    ''' It's ugly docstring which for some annoying reason is below whatever it needs to explain... Which is hideous and hard to follow. No humans read data from bottom to top bruh.'''
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")