#====================================================================#
# File Information
#====================================================================#
"""
    battery.py
    =============
    Holds widgets and functions for battery displayings.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ....BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("battery.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#
def GetBatteryIconFromPourcentage(pourcent:int, mode:str = None, DontDebug:bool = True) -> str:
    """
        GetBatteryIconFromPourcentage:
        ==============================
        Summary:
        --------
        This function returns a battery icon
        depending on a given integer pourcentage
        ranging from 0 to 100.

        Arguments:
        ----------
        - `pourcent:int` defines which battery level you're at. 0-100. There is 10 battery levels
        - `mode:str` variant of the battery. defaults to `None`.
            - `"bluetooth"`
            - `"charging"`
            - `"charging-wireless"`
            - `"unknown"`
    """
    Debug.Start("GetBatteryIconFromPourcentage", DontDebug=DontDebug)

    if(mode == "unknown"):
        Debug.Log("returning unknown battery icon.")
        Debug.End()
        return "battery-unknown"
    
    Debug.Log("Calculating battery value...")
    value = (pourcent/10)
    if(value != 0):
        if(value < 10):
            value = None
        else:
            value = str(value).split(".")[0] + "0"
    else:
        value = None
    
    if(mode == None):
        if(value == "100"):
            Debug.End()
            return "battery"
        
        if(value == None):
            Debug.End()
            return "battery-outline"
        
        Debug.End()
        return "battery-" + value

    if(mode == "bluetooth"):
        if(value == "100"):
            Debug.End()
            return "battery-bluetooth"
        
        if(value == None):
            Debug.End()
            return "battery-outline"
        
        Debug.End()
        return "battery-" + value + "bluetooth"
    
    if(mode == "charging"):
        if(value == "100"):
            Debug.End()
            return "battery-charging-100"
        
        if(value == None):
            Debug.End()
            return "battery-charging-outline"
        
        Debug.End()
        return "battery-charging-" + value
    
    if(mode == "charging-wireless"):
        if(value == "100"):
            Debug.End()
            return "battery-charging-wireless"
        
        if(value == None):
            Debug.End()
            return "battery-charging-wireless-outline"
        
        Debug.End()
        return "battery-charging-wireless-" + value

    Debug.Error("NO BATTERY MATCHES GIVEN VALUES")
    Debug.End()
    return None
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
LoadingLog.End("battery.py")