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
def Windows_GetNetworkInterfaces() -> list:
    """
        Windows_GetNetworkInterfaces:
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
    Debug.Start("Windows_GetNetworkInterfaces")

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

def Windows_GetWiFiNetworks() -> list:
    """
        Windows_GetWiFiNetworks:
        ======================
        Summary:
        --------
        Allows you to get a cleaned list of `netsh wlan` networks output.
        This function allows you to see all the WiFis that are
        available wirelessly in a list format.

        This is especially useful if you want to check which WiFi
        your WINDOWS device can access and view

        `Attention`:
        ------------
        Netsh commands only works on WINDOWS DEVICES. They
        do not work on Linux nor MacOS devices.

        Returns:
        ----------
        - `Execution.Incompatibility`: The function cannot be used due to your device's operating system.
        - `Execution.Failed`: Failed to run the command. wlan is not accessible.
        - `Execution.Crashed` : terminal command failed to execute.

        Examples of returned lists:
        -----------------------------
        - `[{"Admin State": "Disabled", "State": "Disconnected", "Type": "Dedicated", "Interface Name": "Hamachi"}]`
        - `[{"Admin State": "Enabled", "State": "Connected", "Type": "Dedicated", "Interface Name": "Ethernet"}]`
    """
    Debug.Start("Windows_GetWiFiNetworks")

    if(Information.initialized):
        if(Information.platform != "Windows"):
            Debug.Error(f"Attempting to call a netsh function on a non windows based OS: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility
    else:
        Debug.Warn("Warning, BRS's Information class is not initialized. This function cannot execute safety measures.")

    try:
        network = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"])
        Debug.Log("Subprocess success")
    except:
        Debug.Error("Fatal error while running subprocess")
        Debug.End()
        return Execution.Crashed
    decodedNetwork = network.decode("ascii")
    lines = decodedNetwork.splitlines()

    listToReturn = []
    current_network = {}

    for line in decodedNetwork.split("\n"):
        line = line.strip()
        if line.startswith("SSID"):
            Debug.Warn("Key was not found. Could be fresh.")
            current_network.clear()
            current_network["ssid"] = line.split(":")[1].strip()
            var = current_network["ssid"]
            Debug.Log(f"SSID = {var}")

        elif line.startswith("Authentication"):
            current_network["authentication"] = line.split(":")[1].strip()
            var = current_network["authentication"]
            Debug.Log(f"authentication = {var}")

        elif line.startswith("Encryption"):
            current_network["encryption"] = line.split(":")[1].strip()
            var = current_network["authentication"]
            Debug.Log(f"encryption = {var}")

        elif line.startswith("Signal"):
            signal = line.split(":")[1].strip()
            current_network["signal"] = signal
            Debug.Log(f"signal = {signal}")

            try:
                if(current_network["ssid"] != None):
                    Debug.Log("Wifi is probably good...")
                    listToReturn.append(current_network)
            except:
                Debug.Error("Something went wrong durring WiFi parsing.")

        elif line.startswith("BSSID"):
            bssid = line.split(":")[1].strip()

            dataList:list = line.split(" ")
            cleanedList = [x for x in dataList if (x and len(x)>5)]
            Debug.Log(f"BSSID: {cleanedList}")

        elif line.startswith("Channel"):
            current_network["channel"] = line.split(":")[1].strip()

    Debug.Log("Found networks: ")
    Debug.Log(str(listToReturn))
    Debug.End()
    return listToReturn

def Linux_GetNetworkInterfaces() -> list:
    """
        Linux_GetNetworkInterfaces:
        ===========================
        Summary:
        --------
        This function returns a list
        of the possible network interfaces
        that your device can interact with.
        It also returns if they are connected,
        enabled, disconnected or disabled.

        `Attention`:
        ------------
        This commands only works on CERTAIN LINUX. They
        do not work on Windows but may work on
        MacOS.
    """
    Debug.Start("Linux_GetNetworkInterfaces")
    Debug.End()

def Linux_GetWiFiNetworks() -> list:
    """
        Linux_GetWiFiNetworks:
        ======================
        Summary:
        --------
        Allows you to get a cleaned list of `netsh wlan` networks output.
        This function allows you to see all the WiFis that are
        available wirelessly in a list format.

        This is especially useful if you want to check which WiFi
        your WINDOWS device can access and view

        `Attention`:
        ------------
        Netsh commands only works on WINDOWS DEVICES. They
        do not work on Linux nor MacOS devices.

        Returns:
        ----------
        - `Execution.Incompatibility`: The function cannot be used due to your device's operating system.
        - `Execution.Failed`: Failed to run the command. wlan is not accessible.
        - `Execution.Crashed` : terminal command failed to execute.

        Examples of returned lists:
        -----------------------------
        - `[{"Admin State": "Disabled", "State": "Disconnected", "Type": "Dedicated", "Interface Name": "Hamachi"}]`
        - `[{"Admin State": "Enabled", "State": "Connected", "Type": "Dedicated", "Interface Name": "Ethernet"}]`
    """
#====================================================================#
def GetNetworkInterfaces() -> list:
    """
        GetNetworkInterfaces:
        =====================
        Summary:
        --------
        This function will return a list
        of the available network interfaces
        of the device running your application.

        Attention:
        --------
        The Information class needs to be initialized
        before you can call this function. Otherwise,
        it has no clue what your device is and therefor
        cannot execute the appropriated subprocess

        Returns:
        --------
        - `[{"name": "Ethernet", "state": "Disconnected"}, {"name": "Wifi", "state": "Connected"}]`
    """
    Debug.Start("GetNetworkInterfaces")

    interfaces = []
    if(Information.initialized):
        Debug.Log("Information is initialized")

        if(Information.platform == "Windows"):
            Debug.Log("Getting windows interfaces")
            interfaces = Windows_GetNetworkInterfaces()
        if(Information.platform == "Linux"):
            Debug.Log("Getting Linux interfaces")
            interfaces = Linux_GetNetworkInterfaces()
    else:
        Debug.Error("The information class was not initialized")
        return Execution.Failed

    Debug.Log("Parsing interfaces into normalized buffer")
    normalizedInterfaces = []

    for interface in interfaces:
        Debug.Log(interface)
        normalizedInterface = {}
        normalizedInterface["name"] = interface["Interface Name"]
        normalizedInterface["state"] = interface["State"]
        normalizedInterfaces.append(normalizedInterface)

    Debug.Log("Success")
    Debug.End()
    return normalizedInterfaces

def GetWiFiNetworks() -> list:
    """
        GetWiFiNetworks:
        ================
        Summary:
        --------
        This function normalizes the gathering
        of available WiFi networks.

        Attention:
        ----------
        You need to have initialized the Information
        class prior to calling this function.
    """
    Debug.Start("GetWiFiNetworks")

    if(Information.initialized):
        pass
    else:
        Debug.Error("THE INFORMATION CLASS IS NOT INITIALIZED")

    Debug.End()

def CanDeviceUseWiFi() -> bool:
    """
        CanDeviceUseWiFi:
        =================
        Summary:
        --------
        This function checks if the device has access
        to WiFi interfaces. It will return True if its the case
        and False if it can't.
    """
    Debug.Start("CanDeviceUseWiFi")

    if(Information.platform == "Windows"):
        result = Windows_GetWiFiNetworks()
        if(type(result) != list):
            Debug.Error("WiFi function failed.")
            Debug.End()
            return False
        else:
            Debug.Log("WiFi can be used")
            Debug.End()
            return True

    if(Information.platform == "Linux"):
        result = Linux_GetWiFiNetworks()
        if(type(result) != list):
            Debug.Error("WiFi function failed.")
            Debug.End()
            return False
        else:
            Debug.Log("WiFi can be used")
            Debug.End()
            return True

    Debug.Error("FAILED TO EXECUTE")
    Debug.End()
    return False
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("web.py")