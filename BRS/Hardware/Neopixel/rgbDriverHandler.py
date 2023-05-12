#====================================================================#
# File Information
#====================================================================#
"""
    rgbDriverHandler.py
    ================
    Summary:
    --------
    This file handles the neopixel driver that runs on Raspberry
    Pis. It handles a JSON file used to communicate with a python
    script that is executing in a different thread unlinked from
    your main application.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("rgbDriverHandler.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
import sys
import subprocess
import time
from enum import Enum

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ...Utilities.Information import Information
from ...Utilities.FileHandler import JSONdata, CompareKeys, AppendPath
from ...Utilities.Enums import Execution, FileIntegrity
from ...Debug.consoleLog import Debug
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#
_defaultToDriverJsonStructure = {
    "Version" : 1.0,
    "LedCount": 3,
    "State" : "OFF",
    "Mode": "CUSTOM",
    "Colors": {
        "B" : [0,0,0],
        "R" : [0,0,0],
        "S" : [0,0,0]
    }
}
"""
    _defaultToDriverJsonStructure:
    ==============================
    Summary:
    --------
    Private global variable that holds
    a copy of what the JSON file used
    to communicate to the Neopixel driver
    is expected to look like by default.

    This is used to identify older or
    newer versions of the file or to
    spot any potential corruptions or
    mishandling of that file.

    Default:
    --------
    {
        "Version" : 1.0,
        "LedCount": 3,
        "State" : "OFF",
        "Mode": "STATIC",
        "Colors": {
            "B" : [0,0,0],
            "R" : [0,0,0],
            "S" : [0,0,0]
        }
    }
"""

_defaultToApplicationJsonStructure = {
    "Version" : 1.0,
    "State" : "OFF"
}
"""
    _defaultToApplicationJsonStructure:
    ===================================
    Summary:
    --------
    Private global variable that holds
    a copy of what the JSON file that
    communicates with your application
    is expected to look like by default.

    This is used to identify older or
    newer versions of the file or to
    spot any potential corruptions or
    mishandling of that file.

    Default:
    --------
    {
        "Version" : 1.0,
        "State" : "OFF"
    }
"""
#====================================================================#
# Classes
#====================================================================#
class RGB:
    #region   --------------------------- DOCSTRING
    '''
        RGB:
        ====
        Summary:
        --------
        This class handles the RGB led of your Raspberry Pi project.
        This is mainly focused towards interfacing with BRS Kontrol.
        but can easily be manipulated to be used with your own
        custom projects.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    driverState:bool = False
    """
        driverState:
        ============
        Summary:
        --------
        boolean member that indicates the current 
        state of the BRS RGB driver.

        Values:
        -------
        - `False`: Default value. The driver is not running.
        - `True` : The driver is running.
    """

    ToDriverJsonObject:JSONdata = None
    """
        ToDriverJsonObject:
        ===========
        Summary:
        --------
        This member is a json object that
        stores path and file name of the
        JSON file used for your application
        to communicate with the driver by
        itself. See the JSONdata class
        for more information on it.

        `Attention`:
        ------------
        Do not handle this manually. This
        class does it for you and you might
        break shit up if you mess with this
        member.
    """

    ToApplicationJsonObject:JSONdata = None
    """
        ToApplicationJsonObject:
        ===========
        Summary:
        --------
        This member is a json object that
        stores path and file name of the
        JSON file used by the driver to
        to communicate with your application.
        See the JSONdata class
        for more information on it.

        `Attention`:
        ------------
        Do not handle this manually. This
        class does it for you and you might
        break shit up if you mess with this
        member.
    """
    
    initialized:bool = False
    """
        initialized:
        ============
        Summary:
        --------
        This member is a boolean
        member that can be used
        throughout your application
        to verify if the RGB class
        has been initialized.

        Defaults to: `False`

        Warning:
        --------
        Initialized does not mean
        that the neopixel driver
        is started and running. It
        simply means that everything
        is good and the driver is OK
        to run.

        Please use `driverState` to see
        if the driver is running or not.
    """
    
    #endregion
    #region   --------------------------- METHODS
    def StartDriver() -> Execution:
        """
            StartDriver:
            ============
            Summary:
            --------
            This method attempts to start the RGB 
            driver. The driver is started by
            running a python script in sudo mode
            through subprocess.

            Returns:
            --------
            - `Execution.Passed` = Driver has started
            - `Execution.ByPassed` = Information class was not initialized.
            - `Execution.Incompatibility` = You are not running on a device that supports IOT
            - `Execution.Unecessary` = Driver is already running
            - `Execution.Crashed` = Something crashed when starting the driver

            `Attention`:
            ------------
            Your device must be linux based and must
            be a Raspberry Pi. Make sure your
            Neopixel strip is connected to GPIO18
            and you have disabled audio in your
            config.txt.
        """
        Debug.Start("StartDriver")

        if (RGB.driverState == True):
            Debug.Warn("Driver is already running.")
            Debug.End()
            return Execution.Unecessary

        Debug.Log("Verifying Information class")
        if(not Information.initialized):
            Debug.Error("BRS Information class was not initialized")
            Debug.End()
            return Execution.ByPassed
        
        # if(Information.platform != "Linux"):
            # Debug.Error(f"Your platform does not support IOT: {Information.platform}")
            # Debug.End()
            # return Execution.Incompatibility

        Debug.Log("Setting up JSON")
        result = RGB._InitializeJSON()
        if(result != Execution.Passed):
            Debug.Error(f"The JSON function failed to execute with return code: {result}")
            Debug.End()
            return Execution.Failed

        Debug.Log("Launching Neopixel driver")
        result = RGB._StartNeoPixelPythonDriver()
        if(result != Execution.Passed):
            Debug.Error("Something went wrong when trying to launch neopixel driver")
            Debug.End()
            return Execution.Failed
        Debug.Log("DRIVER IS INITIALIZED AND LAUNCHED")

        Debug.Log("Waiting for driver to indicate its ON.")
        result = RGB._WaitForDriverToIndicateItStarted()
        if(result != Execution.Passed):
            Debug.Error("Something went wrong durring the driver's launch.")
            Debug.End()
            return Execution.Crashed

        Debug.Log("NEOPIXEL DRIVER IS UP AND RUNNING.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _InitializeJSON() -> Execution:
        """
            _InitializeJSON:
            ================
            Summary:
            --------
            This private method is used by
            the RGB class to initialize its
            ToDriverJsonObject member with the json
            file stored in the _ThreadFolder.

            This sets the JSON to ON for the
            driver to not immediately shut off
            when its started.

            Returns:
            --------
            - `Execution.Passed` = JSON object initialized and set to ON
            - `Execution.Crashed` = Fatal error occured.
            - `Execution.Failed` = Something prevented this from successfully running.
        """
        Debug.Start("_InitializeJSON")

        #region ------------------------- Creating path
        Debug.Log("Setting path of _ThreadFolder")
        path = os.path.abspath(__file__)
        path = path.replace("rgbDriverHandler.py", "")
        path = AppendPath(path, "_ThreadFolder/")
        #endregion

        RGB.ToDriverJsonObject = JSONdata("ToDriver", path)
        RGB.ToApplicationJsonObject = JSONdata("ToApplication", path)

        #region ------------------------- Creating ToDriver JSONs
        Debug.Log("Attempting to create ToDriver.json ...")
        createdSuccessfully = RGB.ToDriverJsonObject.CreateFile(_defaultToDriverJsonStructure)
        if(not createdSuccessfully):
            Debug.Error("Failed to create ToDriver.json")
            Debug.End()
            return Execution.Failed
        
        Debug.Log("JSON file was created. Loading it...")
        RGB.ToDriverJsonObject = JSONdata("ToDriver", path)
        if(RGB.ToDriverJsonObject.jsonData == None):
            Debug.Error("File is sempty?")
            Debug.End()
            return Execution.Crashed
        Debug.Log("File created successfully")
        #endregion

        #region ------------------------- Creating ToApplication JSONs
        Debug.Log("Attempting to create ToApplication.json ...")
        createdSuccessfully = RGB.ToApplicationJsonObject.CreateFile(_defaultToApplicationJsonStructure)
        if(not createdSuccessfully):
            Debug.Error("Failed to create ToApplication.json")
            Debug.End()
            return Execution.Failed
        
        Debug.Log("JSON file was created. Loading it...")
        RGB.ToApplicationJsonObject = JSONdata("ToApplication", path)
        if(RGB.ToApplicationJsonObject.jsonData == None):
            Debug.Error("File is sempty?")
            Debug.End()
            return Execution.Crashed
        Debug.Log("File created successfully")
        #endregion

        #region ------------------------- Comparing file content with expected content
        Debug.Log("Comparing JSON content...")
        result = CompareKeys(_defaultToDriverJsonStructure, RGB.ToDriverJsonObject.jsonData)
        if(result != FileIntegrity.Good):
            Debug.Error("JSON file's data does not match expected data")
            Debug.Log("Attempting to create new file...")
            createdSuccessfully = RGB.ToDriverJsonObject.CreateFile(_defaultToDriverJsonStructure)
            if(not createdSuccessfully):
                Debug.Error("Failed to create ToDriver.json")
                Debug.End()
                return Execution.Failed
            
            Debug.Log("JSON file was fixed. Loading it...")
            RGB.ToDriverJsonObject = JSONdata("ToDriver", path)
            if(RGB.ToDriverJsonObject.jsonData == None):
                Debug.Error("Error occured. File is not empty.")
                Debug.End()
                return Execution.Crashed
            Debug.Log("File fixed successfully")
        #endregion
        
        #region ------------------------- Setting JSON state to ON
        Debug.Log("Setting JSON driver state to ON...")
        try:
            RGB.ToDriverJsonObject.jsonData["State"] = "ON"
            Debug.Log("Success")
        except:
            Debug.Error("FATAL: Crashed when attempting to set STATE to ON")
            Debug.End()
            return Execution.Crashed

        Debug.Log("Saving JSON file...")
        fileSaved = RGB.ToDriverJsonObject.SaveFile()
        if(not fileSaved):
            Debug.Error("JSON file could not be saved")
            Debug.End()
            return Execution.Failed
        Debug.Log("File saved successfully.")
        #endregion
        RGB.initialized = True
        Debug.Log("RGB JSON IS INITIALIZED AND READY TO GO.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _StartNeoPixelPythonDriver() -> Execution:
        """
            _StartNeoPixelPythonDriver:
            ===========================
            Summary:
            --------
            This private method of the RGB
            class allows itself to start the
            python script that handles
            Neopixels directly on your
            Raspberry Pi.

            Returns:
            --------
            - `Execution.Passed` = Subprocess ran without errors
            - `Execution.Crashed` = Subprocess crashed without errors
            - `Execution.Failed` = Subprocess returned an error code.

            `Attention`:
            ------------
            This starts a python file by
            using the subprocess functions.
            This is made for LINUX devices
            ONLY.

            You need to have initialized the Information
            class prior to calling this method.
            `DO NOT MANUALLY CALL THIS METHOD ALRIGHT?`
            It may cause invisible python processes
            to be running in the background if you
            just constantly call this bullshit.
        """
        Debug.Start("_StartNeoPixelPythonDriver")

        #region ------------------------- Creating path
        Debug.Log("Getting driver path")
        path = os.path.abspath(__file__)
        path = path.replace("rgbDriverHandler.py", "driver.py")
        #endregion

        #region ------------------------- Running Subprocess
        Debug.Log("Trying to run neopixel driver")
        if sys.platform == 'win32':
            subprocess.Popen(['start', '/B', 'python', path], shell=True)
        else:
            subprocess.Popen(['python', path, '&'])
        #endregion
        Debug.Log("Success. Driver is launched.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def GetStateOfDriver() -> Execution:
        """
            GetStateOfDriver:
            =================
            Summary:
            --------
            Public method that allows you
            to read the current state of the
            Neopixel driver from the JSON
            file that it handles.

            Warning:
            --------
            This opens ToApplication.json and tries to
            Get the information within it. This process
            can be slow.

            Returns:
            --------
            - `Execution.Failed`: The RGB class is not initialized
            - `Execution.Crashed`: It's possible that you tried to read the file while the driver is writing in it.
            - `"OFF"` = The Neopixel driver is OFF
            - `"CRASHED"` = The Neopixel driver crashed.
        """
        Debug.Start("GetStateOfDriver")

        if(RGB.initialized):

            result = RGB.ToApplicationJsonObject.ReadFile()
            if(result != True):
                Debug.Error("Failed to read the file.")
                Debug.End()
                return Execution.Crashed
            
            Debug.Log("File read successfully.")
            
            state = RGB.ToApplicationJsonObject.jsonData["State"]
            Debug.Log("Successfully returned the driver's current state")
            Debug.End()
            return state

        else:
            Debug.Error("Tried to get state from uninitialized class")
            Debug.End()
            return Execution.Failed

        Debug.End()
    # -----------------------------------
    def _WaitForDriverToIndicateItStarted() -> Execution:
        """
            _WaitForDriverToIndicateItStarted:
            ==================================
            Summary:
            --------
            Private method that waits for
            ToApplication.json to say that the
            driver started. There is a 1 second
            timeout.

            Returns:
            --------
            - `Execution.Passed` = Driver started and its state is now ON
            - `Execution.Crashed` = Driver says that it crashed.
            - `Execution.Failed` = Timeout was reached... Rip
        """
        Debug.Start("_WaitForDriverToIndicateItStarted")
        timeout:float = 1000
        currentAttempt = 0

        Debug.Log("Start of the waiting game...")
        for currentMillisecond in range(timeout):
            if (currentMillisecond % 100 == 0):
                time.sleep(0.1)
                currentAttempt = currentAttempt + 1
                # Debug.Warn("Trying to read ToApplication.json")

                state = RGB.GetStateOfDriver()
                if(state != "ON"):
                    Debug.Error("Driver is not ON...")
                    if(state == "CRASHED"):
                        Debug.Error(f"Driver crashed during boot. Failed after {currentAttempt} attempts.")
                        Debug.End()
                        return Execution.Crashed
                else:
                    Debug.Log(f"Driver was seen ON after {currentAttempt} attempts.")
                    Debug.End()
                    return Execution.Passed

        Debug.Error(f"Driver never turned on after {currentAttempt} attempts over a period of {timeout} milliseconds")
        Debug.End()
        return Execution.Failed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")