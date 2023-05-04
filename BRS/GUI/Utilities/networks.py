#====================================================================#
# File Information
#====================================================================#
"""
    networks.py
    =============
    This file contains functions and classes used to handle networks
    display such as wifi icons or ethernet ports.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
from ...Debug.consoleLog import Debug
LoadingLog.Start("networks.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ...Utilities.Information import Information
from ...Utilities.Enums import Execution
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
#endregion
#====================================================================#
# Functions
#====================================================================#
def GetWifiIcon(strength:int, mode:str) -> str:
    """
        GetWifiIcon:
        ============
        Summary:
        --------
        This function is used to get a material design icon
        from KivyMDs integrated library that represents the
        state of a WiFi network.

        Parameters:
        -----------
        - `strength:int` = wifi strength (0 to 100)
        - `mode:str` = "alert", "lock", "lock-open", "off",  None=normal
    """
    Debug.Start("GetWifiIcon")

    iconOutput = ""

    strength = int(strength/20)
    if(strength > 4):
        return Execution.Failed

    if (mode == "off"):
        Debug.End()
        return "wifi-strength-off-outline"

    if not mode in ["alert", "lock", "lock-open", "off"]:
        Debug.Log("Using regular icon")
    else:
        iconOutput = "wifi-strength-"
        if(strength > 0):
            iconOutput = iconOutput + str(strength) + "-"

        iconOutput = iconOutput + mode

    return iconOutput
    Debug.End()


#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("networks.py")