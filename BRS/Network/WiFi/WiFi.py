#====================================================================#
# File Information
#====================================================================#
"""
    WiFi.py
    =============
    This file contains dumbed down interfacing functions that
    allows python applications to connect and detect WiFis around
    them... Hopefully.
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
LoadingLog.Import("Python")
import subprocess
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
def Netsh_GetNetworkInterfaces() -> list:
    """
        Netsh_GetNetworkInterfaces:
        ===========================
        Summary:
        --------
        Allows you to get a cleaned list of netsh terminal output.
        This function allows you to see all the interfaces that
        networks can use such as Hamachi, Ethernet and so on.

        This is especially useful if you want to check if your
        WINDOWS device has WiFi capabilities.

        `Attention`:
        ------------
        Netsh commands only works on WINDOWS DEVICES. They
        do not work on Linux nor MacOS devices.

        Returns:
        ----------
        - `Execution.Incompatibility`: The function cannot be used due to your device's operating system.
        - `(list)`: Good execution

        Examples of returned lists:
        -----------------------------
        - `[{"Admin State": "Disabled", "State": "Disconnected", "Type": "Dedicated", "Interface Name": "Hamachi"}]`
        - `[{"Admin State": "Enabled", "State": "Connected", "Type": "Dedicated", "Interface Name": "Ethernet"}]`
    """
    Debug.Start("Netsh_GetNetworkInterfaces")

    if(Information.initialized):
        if(Information.platform != "Windows"):
            Debug.Error(f"Attempting to call a netsh function on a non windows based OS: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility
        else:
            Debug.Log("Windows platform detected.")
    else:
        Debug.Warn("Warning, BRS's Information class is not initialized. This function cannot execute safety measures.")

    try:
        network = subprocess.check_output(["netsh", "interface", "show", "interface"])
        Debug.Log("Subprocess success")
    except:
        Debug.Error("Fatal error while running subprocess")
        Debug.End()
        return Execution.Crashed
    decodedNetwork = network.decode("ascii")
    lines = decodedNetwork.splitlines()

    #Remove Useless lines
    cleanedLines = []
    listOutcome = []
    for line in lines:
        if(len(line) > 0 and not line.startswith("-") and not "Admin State" in line):
            dataList:list = line.split(" ")
            cleanedList = [x for x in dataList if x] # remove empty characters / spaces from the list
            listOutcome.append(
                {
                    "Admin State": cleanedList[0],
                    "State": cleanedList[1],
                    "Type": cleanedList[2],
                    "Interface Name": cleanedList[3],
                }
            )

    Debug.Log("Function successfully ran")
    Debug.End()
    return listOutcome

def Netsh_GetWiFiNetworks() -> list:
    """
        Netsh_GetWiFiNetworks:
        ======================
        Summary:
        --------
        Allows you to get a cleaned list of netsh wlan networks output.
        This function allows you to see all the networks that are
        available wirelessly.

        This is especially useful if you want to check which WiFi
        your WINDOWS device can access

        `Attention`:
        ------------
        Netsh commands only works on WINDOWS DEVICES. They
        do not work on Linux nor MacOS devices.

        Returns:
        ----------
        - `Execution.Incompatibility`: The function cannot be used due to your device's operating system.
        - `Execution.Failed`: Failed to run the command. wlan is not accessible.

        Examples of returned lists:
        -----------------------------
        - `[{"Admin State": "Disabled", "State": "Disconnected", "Type": "Dedicated", "Interface Name": "Hamachi"}]`
        - `[{"Admin State": "Enabled", "State": "Connected", "Type": "Dedicated", "Interface Name": "Ethernet"}]`
    """
    Debug.Start("Netsh_GetWiFiNetworks")

    if(Information.initialized):
        if(Information.OS != "Windows"):
            Debug.Error(f"Attempting to call a netsh function on a non windows based OS: {Information.OS}")
            Debug.End()
            return Execution.Incompatibility
    else:
        Debug.Warn("Warning, BRS's Information class is not initialized. This function cannot execute safety measures.")
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("web.py")