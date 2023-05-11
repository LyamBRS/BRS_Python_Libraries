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
    listOfSeenNetworks = []
    listOfSeenBSSID = []
    oldSSID:str = ""
    newSSID:bool = False
    newBSSID:bool = False

    for line in decodedNetwork.split("\n"):
        line = line.strip()
        if line.startswith("SSID"):

            ssid = line.split(":")[1].strip()

            if ssid in listOfSeenNetworks:
                newSSID = False
                # Debug.Log("[SKIPPED]")
            else:
                listOfSeenNetworks.append(ssid)
                newSSID = True
                current_network = {}
                Debug.Log(">>>> [CLEARED CONTENT]")
                current_network["ssid"] = ssid
                var = current_network["ssid"]
                # Debug.Log(f">>> SSID = {var}")

        elif line.startswith("Authentication") and newSSID:
            current_network["authentication"] = line.split(":")[1].strip()
            var = current_network["authentication"]
            # Debug.Log(f">>> authentication = {var}")

        elif line.startswith("Encryption") and newSSID:
            current_network["encryption"] = line.split(":")[1].strip()
            var = current_network["authentication"]
            # Debug.Log(f">>> encryption = {var}")

        elif line.startswith("Signal") and newSSID:
            signal = line.split(":")[1].strip()
            current_network["signal"] = signal
            # Debug.Log(f">>> signal = {signal}")

            try:
                if(current_network["ssid"] != None):
                    newSSID = False
                    Debug.Log(f"[APPENDING : {current_network}]")
                    listToReturn.append(current_network)
                    # Debug.Log(f"NEW LIST >>> {listToReturn}")
            except:
                Debug.Error("Something went wrong durring WiFi parsing.")

        elif line.startswith("BSSID") and newSSID:
            bssid = line.split(":")[1].strip()

            dataList:list = line.split(" ")
            cleanedList = [x for x in dataList if (x and len(x)>5)]
            # Debug.Log(f">>> BSSID: {cleanedList}")
            try:
                current_network["bssid"] = cleanedList[0]
            except:
                current_network["bssid"] = "ERROR"

        elif line.startswith("Channel") and newSSID:
            current_network["channel"] = line.split(":")[1].strip()

    # Debug.Log("Found networks: ")
    # Debug.Log(str(listToReturn))
    Debug.End()
    return listToReturn

def Windows_ConnectToNetwork(ssid:str, password:str) -> bool:
    """
        Windows_ConnectToNetwork:
        =========================
        Summary:
        --------
        This function attempts to connect
        to a given network by using a specific
        SSID and a specific password.

        Returns:
        --------
        - `True`: The connection was successful.
        - `False` : The connection didn't work.
    """
    Debug.Start("Windows_ConnectToNetwork")

    if(Information.initialized):
        if(Information.platform != "Windows"):
            Debug.Error(f"Attempting to call a netsh function on a non windows based OS: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility
        Debug.Log("Platform checked successfully.")
    else:
        Debug.Warn("Warning, BRS's Information class is not initialized. This function cannot execute safety measures.")


    Debug.Log("Trying to execute windows terminal command...")

    try:
        import os
        name = ""
        # function to establish a new connection
        def createNewConnection(name, SSID, password):
            config = f"""<?xml version=\"1.0\"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>{name}</name>
            <SSIDConfig>
                <SSID>
                    <name>{SSID}</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>WPA2PSK</authentication>
                        <encryption>AES</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
                    <sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>false</protected>
                        <keyMaterial>{password}</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>"""

            command = f"netsh wlan add profile filename=\""+name+".xml\""+" interface=\"Wi-Fi\""
            with open(name+".xml", 'w') as file:
                file.write(config)
            os.system(command)

        # function to connect to a network
        def connect(name, SSID):
            command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\""
            os.system(command)

        # function to display avavilabe Wifi networks
        def displayAvailableNetworks() -> int:
            """0: worked, anythingElse = failed."""
            command = "netsh wlan show networks interface=\"Wi-Fi\""
            returnedValue = os.system(command)
            return returnedValue

        # display available netwroks
        returnedValue = displayAvailableNetworks()
        if(returnedValue != 0):
            Debug.Error("Failed to display available networks")
            Debug.End()
            return False

        # input wifi name and password
        name = "Batiscan"
        password = "BATISCAN"

        # establish new connection
        createNewConnection(name, name, password)

        # connect to the wifi network
        connect(name, name)
    except:
        Debug.Error("Something failed when trying to connect through netsh... good luck!")
        Debug.End()
        return False

    Debug.Log("SUCCESS")
    Debug.End()
    return True

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

def Linux_ConnectToNetwork(ssid:str, password:str) -> bool:
    """
        Linux_ConnectToNetwork:
        =======================
        Summary:
        --------
        This function attempts to connect
        to a given network by using a specific
        SSID and a specific password.

        Returns:
        --------
        - `True`: The connection was successful.
        - `False` : The connection didn't work.
    """
    Debug.Start("Linux_ConnectToNetwork")

    if(Information.initialized):
        if(Information.platform != "Windows"):
            Debug.Error(f"Attempting to call a netsh function on a non windows based OS: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility
        Debug.Log("Platform checked successfully.")
    else:
        Debug.Warn("Warning, BRS's Information class is not initialized. This function cannot execute safety measures.")


    Debug.Log("Trying to execute windows terminal command...")

    Debug.Log("SUCCESS")
    Debug.End()
    return True

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

    interfaces = []
    if(Information.initialized):
        Debug.Log("Information is initialized")

        if(Information.platform == "Windows"):
            Debug.Log("Getting windows networks")
            interfaces = Windows_GetWiFiNetworks()
        if(Information.platform == "Linux"):
            Debug.Log("Getting Linux networks")
            interfaces = Linux_GetWiFiNetworks()
    else:
        Debug.Error("The information class was not initialized")
        return Execution.Failed

    Debug.Log("Parsing interfaces into normalized buffer")
    normalizedInterfaces = []


    for interface in interfaces:
        Debug.Log(interface)

        try:
            # Debug.Log(">>> ssid")
            try:
                ssid = interface["ssid"]
            except:
                Debug.Error("Failed to parse ssid")
                ssid = "ERROR"

            # Debug.Log(">>> bssid")
            try:
                bssid = interface["bssid"]
            except:
                Debug.Error("Failed to parse bssid")
                bssid = "???"

            # Debug.Log(">>> strength")
            try:
                strength = interface["signal"]
            except:
                Debug.Error("Failed to parse signal")
                strength = 0

            # Debug.Log(">>> creating normalized buffer")
            normalizedInterface = {}
            # Debug.Log(">>> placing ssid")
            normalizedInterface["ssid"] = ssid
            # Debug.Log(">>> placing bssid")
            normalizedInterface["bssid"] = bssid
            # Debug.Log(">>> placing mode")
            normalizedInterface["mode"] = None

            if("%" in strength):
                try:
                    # Debug.Log("Attempting to transform windows wifi strength")
                    strength = strength.replace("%", "")
                    normalizedInterface["strength"] = int(strength)
                except:
                    Debug.Error("Failed to normalize strength")
                    normalizedInterface["strength"] = 0
                    normalizedInterface["mode"] = "alert"
    
            # Debug.Log(">>> appending")
            normalizedInterfaces.append(normalizedInterface)
        except:
            Debug.Error("FAILED TO NORMALIZE GIVEN NETWORK")

    # Debug.Log("Normalized networks: ")
    # Debug.Log(str(normalizedInterfaces))

    Debug.Log("Success")
    Debug.End()
    return normalizedInterfaces

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

def ConnectToAWiFiNetwork(ssidOfTheNetwork:str, passwordOfTheNetwork:str) -> bool:
    """
        ConnectToAWiFiNetwork:
        ======================
        Summary:
        --------
        This function attempts to connect to a given wireless
        Wi-Fi network through various processes.
        If you are using a Linux based machine, the function
        will execute differently than a Windows machine.

        Windows machines will use `netsh`
        Linux machines will use `TO_DO`

        Return:
        -------
        - `True`: The connection is successful. Or at least it didn`t crash.
        - `False`: Failed to connect using the given parameters.

        `Attention`:
        ------------
        This is scuffed as fuck. It might just not work for
        your uses or your device. This is tested on
        Ethernet enabled Windows devices, Wi-Fi enabled
        Windows laptops and Raspberry Pi 4B. Nothing else.

        **PLEASE MAKE SURE THE `Information` class is initialised.**
    """
    Debug.Start("ConnectToAWiFiNetwork")

    if(Information.initialized):
        if(Information.platform == "Windows"):
            Debug.Log("Using Windows function.")
            result = Windows_ConnectToNetwork(ssidOfTheNetwork, passwordOfTheNetwork)
            Debug.Log(f"Function executed -> {result}")
            Debug.End()
            return result
        else:
            Debug.Log("Using Linux function.")
            result = Linux_ConnectToNetwork(ssidOfTheNetwork, passwordOfTheNetwork)
            Debug.Log(f"Function executed -> {result}")
            Debug.End()
            return result
    else:
        Debug.Error("Information class is not initialized. This function cannot be used.")
        Debug.End()
        return False
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("web.py")