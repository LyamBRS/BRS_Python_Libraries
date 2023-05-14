#====================================================================#
# File Information
#====================================================================#
"""
    driver.py
    =============
    This file is a python script that is executed parallel to your
    application which sole purpose is to handle RGB Neopixel LEDs
    that your IOT device may need to drive during the execution
    of its application.

    DO NOT EXECUTE THIS FILE MANUALLY.
    ----------------------------------
"""
#====================================================================#
# Loading Logs
#====================================================================#
import os
import sys
absolutePathOfTheDriver = os.path.abspath(__file__)
LibraryPath = absolutePathOfTheDriver.replace("BRS\\Hardware\\Neopixel\\driver.py", "")
LibraryPath = LibraryPath.replace("BRS/Hardware/Neopixel/driver.py", "")
sys.path.append(LibraryPath)

print("\n=========================================")
print("DRIVER: NEOPIXELS: COMPILING             ")
print("=========================================")

from BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import time
import math
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from BRS.Debug.consoleLog import Debug
from BRS.Utilities.Enums import FileIntegrity, Execution
from BRS.Utilities.FileHandler import AppendPath, CompareKeys, JSONdata
#endregion
#region ------------------------------------------------------- Board
LoadingLog.Import("CircuitPython")
import board
import neopixel

ORDER = neopixel.GRB
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Constant
#====================================================================#
ANIMATION_NEW_FRAME_DELAY = 0.01
ANIMATION_DURATION = 1

class GlobalVariables():
    """
        GlobalVariables:
        ================
        Summary:
        --------
        Holds variables used throughout the driver
        in functions that would otherwise not work.
    """
    currentAnimationTick:float = 0
    """
        currentAnimationTick:
        =====================
        Summary:
        --------
        The current millisecond that the LED animation is at.
        The milliseconds are displayed in decimals of seconds.
        1 millisecond is equal to 0.001 for example.

        Defaults to 0.
    """
#====================================================================#
# Global variables
#====================================================================#
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

_defaultToDriverJsonStructure = {
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
        "Mode": "Custom",
        "Custom": {
            "B" : [0,0,0],
            "R" : [0,0,0],
            "S" : [0,0,0]
        }
    }
"""

class RGBModes():
    """
        RGBModes:
        =========
        Summary:
        --------
        class which contains all
        the possible RGB modes that
        can be sent to the Neopixel
        driver.
    """
    off:str = "OFF"
    static:str = "STATIC"
    cycling:str = "CYCLING"
    pulse:str = "PULSE"
    loading:str = "LOADING"
#====================================================================#
# Global RGB functions
#====================================================================#
def GetCycledColor(colorToCycle, tick, maxTickCount, RadianOffset) -> float:
    """
        GetCycledColor:
        ===============
        Summary:
        --------
        This returns a cycled singular color from a
        wanted color.

        Arguments:
        ----------
        - `colorToCycle` = 0-255 color to cycle
        - `tick` = the current tick within the maxTickCount used to create a ratio from 1 to 0.
        - `maxTickCount` = The resolution of the animation. How many frames is there to animate?
        - `RadianOffset` = Offset to give to the color. (2.09 for cycled colors to offset green, red and blue)   
    """
    temporary = 0
    ratio = tick / maxTickCount
    ratio = ratio * 6.28

    temporary = math.sin(ratio + RadianOffset)
    temporary = math.pow(temporary, 4) * colorToCycle

    return temporary
# -------------------------------------------------------------------
def GetLerpedColors(currentColors:list, wantedColors:list):
    """
        GetLerpedColor:
        ===============
        Summary:
        --------
        Returns a lerped singular color.
    """
    globalDelta = 0.01

    wantedR = wantedColors[1]
    wantedG = wantedColors[2]
    wantedB = wantedColors[3]

    currentR = currentColors[1]
    currentG = currentColors[2]
    currentB = currentColors[3]

    def Lerp(current,wanted):
        return ((current - globalDelta) * current + globalDelta * wanted)

    newR = Lerp(currentR, wantedR)
    newG = Lerp(currentG, wantedG)
    newB = Lerp(currentB, wantedB)

    return [newR, newG, newB]

#====================================================================#
# Global functions
#====================================================================#
def printFatalDriverError(messageToPrint:str):
    """
        printFatalDriverError:
        ======================
        Summary:
        --------
        This function prints in the terminal a fatal error
        that occured within a driver. This is because the
        Debug class may or may not be initialized in the
        driver or the application. This ensure that it
        gets printed in a consistant format no matter what.

        Arguments:
        ----------
        - `messageToPrint`: string printed in the terminal.
    """
    print(f"[BRS - FATAL ERROR]:\t[NEOPIXEL]:\t{messageToPrint}")

def printDriverHeader(messageToPrint:str):
    """
        printDriverHeader:
        ==================
        Summary:
        --------
        prints a globally visible header for the main
        application to see in its terminal regardless
        of Debug information settings.

        Arguments:
        ----------
        - `messageToPrint` : The string to put in the header.
    """
    print("\n=========================================")
    print(f"DRIVER: NEOPIXELS: {messageToPrint}     ")
    print("=========================================")
# --------------------------------------------------------------------
def HandleDriver() -> Execution:
    """
        HandleDriver:
        =============
        Summary:
        --------
        This function's goal is to handle each ticks
        of the neopixel driver. It also handles
        the reading of the ToDriver.json file.
    """
    time.sleep(ANIMATION_NEW_FRAME_DELAY)
    GlobalVariables.currentAnimationTick = GlobalVariables.currentAnimationTick + ANIMATION_NEW_FRAME_DELAY

    if(GlobalVariables.currentAnimationTick > ANIMATION_DURATION):
        GlobalVariables.currentAnimationTick = 0
        result = DriverHandler.Update()
        if(result != Execution.Passed):
            printDriverHeader("STOPPING")
            # NeopixelHandler.Close()
            return result

        NeopixelHandler.UpdateFromJson()

    # Update the LEDs.
    NeopixelHandler.ShowNewPixels()
    return Execution.Passed
#====================================================================#
# Classes
#====================================================================#
class DriverHandler:
    #region   --------------------------- DOCSTRING
    """
        DriverHandler:
        ==============
        Summary:
        --------
        Handles the ToApplication.json file
        used by this process to communicate back
        with your application to tell it various
        information about its current state for
        example.
    """
    #endregion
    #region   --------------------------- MEMBERS
    OutputJsonObject:JSONdata = None
    """
        OutputJsonObject:
        =================
        Summary:
        --------
        This member is a json object that
        stores path and file name of the
        JSON file used for the driver
        to communicate with your application.
        See the `JSONdata` class
        for more information on it.

        `Attention`:
        ------------
        Do not handle this manually. This
        class does it for you and you might
        break shit up if you mess with this
        member.

        In fact, what are you doing importing
        anything from this file into your
        application???
        Use the RGB class instead bruh
    """

    InputJsonObject:JSONdata = None
    """
        InputJsonObject:
        ================
        Summary:
        --------
        This member is a json object that
        stores path and file name of the
        JSON file used for the application
        to communicate with this driver.
        See the `JSONdata` class
        for more information on it.

        `Attention`:
        ------------
        Do not handle this manually. This
        class does it for you and you might
        break shit up if you mess with this
        member.

        In fact, what are you doing importing
        anything from this file into your
        application???
        Use the RGB class instead bruh
    """
    
    initialized:bool = False
    """
        initialized:
        ============
        Summary:
        ---------
        If set to True, the JSONs were
        successfully initialized and could
        be loaded with the correct information.
    """
    #endregion
    #region   --------------------------- METHODS
    def Start() -> Execution:
        """
            Start:
            ============
            Summary:
            --------
            Attempts to start the neopixel driver.
            Checks the JSON files and other stuff.
        """
        Debug.Start("Start")

        Debug.Log("Trying to initialize the json")
        result = DriverHandler._InitializeOutputJson()
        if(result != Execution.Passed):
            Debug.Error("DRIVER: Failed to initialize the JSON.")
            Debug.End()
            return Execution.Crashed
        
        result = DriverHandler._InitializeInputJson()
        if(result != Execution.Passed):
            Debug.Error("DRIVER: Failed to verify and get data from ToDriver.json")
            Debug.Warn("Setting driver to crashed mode.")
            Debug.End()
            return Execution.Crashed
        
        Debug.Log("Driver's JSON were successfully initialized.")
        DriverHandler.initialized = True

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _InitializeOutputJson() -> Execution:
        """
            _InitializeOutputJson:
            ======================
            Summary:
            --------
            This private method is used by
            the class to initialize its
            OutputJsonObject member with the json
            file stored in the _ThreadFolder.

            This sets the JSON to ON for the
            application to not immediately
            think there was an error with
            the driver.

            Returns:
            --------
            - `Execution.Passed` = JSON object initialized and set to ON
            - `Execution.Crashed` = Fatal error occured.
            - `Execution.Failed` = Something prevented this from successfully running.
        """
        Debug.Start("_InitializeOutputJson")
        jsonFileName = "ToApplication"

        #region ------------------------- Creating path
        Debug.Log("Setting path of _ThreadFolder")
        path = os.path.abspath(__file__)
        path = path.replace("driver.py", "")
        path = AppendPath(path, "_ThreadFolder/")
        #endregion

        #region ------------------------- Checking if file exist.
        Debug.Log("Initializing JSONdata object...")
        DriverHandler.OutputJsonObject = JSONdata(jsonFileName, path)
        if(DriverHandler.OutputJsonObject.jsonData == None):
            Debug.Warn("The json file found is empty.")
            Debug.Log("Attempting to create new file...")
            createdSuccessfully = DriverHandler.OutputJsonObject.CreateFile(_defaultToApplicationJsonStructure)
            if(not createdSuccessfully):
                Debug.Error(f"Failed to create {jsonFileName}.json")
                Debug.End()
                return Execution.Failed
            
            Debug.Log("JSON file was created. Loading it...")
            DriverHandler.OutputJsonObject = JSONdata(jsonFileName, path)
            if(DriverHandler.OutputJsonObject.jsonData == None):
                Debug.Error("File is still empty even after being re-created.")
                Debug.End()
                return Execution.Crashed

        Debug.Log("File created successfully")
        #endregion

        #region ------------------------- Comparing file content with expected content
        Debug.Log("Comparing JSON content...")
        result = CompareKeys(_defaultToApplicationJsonStructure, DriverHandler.OutputJsonObject.jsonData)
        if(result != FileIntegrity.Good):
            Debug.Error("JSON file's data does not match expected data")
            Debug.Log("Attempting to create new file...")
            createdSuccessfully = DriverHandler.OutputJsonObject.CreateFile(_defaultToApplicationJsonStructure)
            if(not createdSuccessfully):
                Debug.Error(f"Failed to create {jsonFileName}.json")
                Debug.End()
                return Execution.Failed
            
            Debug.Log("JSON file was fixed. Loading it...")
            DriverHandler.OutputJsonObject = JSONdata(jsonFileName, path)
            if(DriverHandler.OutputJsonObject.jsonData == None):
                Debug.Error("Error occured. File is not empty.")
                Debug.End()
                return Execution.Crashed
            Debug.Log("File fixed successfully")
        #endregion
        
        #region ------------------------- Setting JSON state to ON
        Debug.Log("Setting JSON driver state to ON...")
        try:
            DriverHandler.OutputJsonObject.jsonData["State"] = "ON"
            Debug.Log("Success")
        except:
            Debug.Error("FATAL: Crashed when attempting to set STATE to ON")
            printFatalDriverError("335: Failed to set self state to ON")
            Debug.End()
            return Execution.Crashed

        Debug.Log("Saving JSON file...")
        fileSaved = DriverHandler.OutputJsonObject.SaveFile()
        if(not fileSaved):
            Debug.Error("JSON file could not be saved")
            Debug.End()
            return Execution.Failed
        Debug.Log("File saved successfully.")
        #endregion
        Debug.Log("DriverHandler's OutputJsonObject IS INITIALIZED AND READY TO GO.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _InitializeInputJson() -> Execution:
        """
            _InitializeInputJson:
            ================
            Summary:
            --------
            This private method is used by
            the class to initialize its
            InputJsonObject member with the json
            file stored in the _ThreadFolder.

            This sets the JSON to ON for the
            application to not immediately
            think there was an error with
            the driver.

            Returns:
            --------
            - `Execution.Passed` = JSON object initialized and set to ON
            - `Execution.Crashed` = Fatal error occured.
            - `Execution.Failed` = Something prevented this from successfully running.
        """
        Debug.Start("_InitializeInputJson")
        jsonFileName = "ToDriver"

        #region ------------------------- Creating path
        Debug.Log("Setting path of _ThreadFolder")
        path = os.path.abspath(__file__)
        path = path.replace("driver.py", "")
        path = AppendPath(path, "_ThreadFolder/")
        #endregion

        #region ------------------------- Checking if file exist.
        Debug.Log("Initializing JSONdata object...")
        DriverHandler.InputJsonObject = JSONdata(jsonFileName, path)
        if(DriverHandler.InputJsonObject.jsonData == None):
            Debug.Error("The Input json file found is empty.")
            printFatalDriverError("326: FAILED TO GET DATA FROM ToDriver.json")
            Debug.End()
            return Execution.Crashed
        Debug.Log("File's content gathered successfully.")
        #endregion

        #region ------------------------- Comparing file content with expected content
        Debug.Log("Comparing JSON content...")
        result = CompareKeys(_defaultToDriverJsonStructure, DriverHandler.InputJsonObject.jsonData)
        if(result != FileIntegrity.Good):
            Debug.Error("JSON file's data does not match expected data")
            printFatalDriverError("337: ToDriver.py has corrupted data in it.")
        #endregion
        
        #region ------------------------- Reading State of ToDriver
        Debug.Log("Reading JSON driver state...")
        try:
            if(DriverHandler.InputJsonObject.jsonData["State"] != "ON"):
                Debug.Log("Driver should close")
                printFatalDriverError("Driver started with json set to OFF...")
                Debug.End()
                return Execution.Failed
            Debug.Log("State is ON, the application wants to handle LEDs")
        except:
            Debug.Error("FATAL: Crashed when attempting to set STATE to ON")
            printFatalDriverError("392: Crashed when trying to read if ToDriver's state is ON")
            Debug.End()
            return Execution.Crashed
        #endregion
        DriverHandler.initialized = True
        Debug.Log("DriverHandler InputJsonObject IS INITIALIZED AND READY TO GO.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def Close(message:str = "OFF") -> Execution:
        """
            Close:
            ======
            Summary:
            --------
            Closes the driver properly.
            This means indicating through
            the JSON file that the driver
            is now OFF and saving the JSON
            file.

            Its then up to you to ensure
            that this scripts terminates
            properly.

            Arguments:
            ----------
            - `message`: a string to put as the driver's state. Defaults to "OFF".
            
            Possible values:
            ----------------
            - `"OFF"` : Default message value. Means the driver is now OFF.
            - `"CRASHED"` : Means the driver crashed during execution.
        """
        Debug.Start("Close")
    
        if(not DriverHandler.initialized):
            Debug.Error("Trying to properly close an uninitialized driver.")

        Debug.Log(f"Setting State to: {message}")
        DriverHandler.OutputJsonObject.jsonData["State"] = message

        Debug.Log("Saving OutputJsonObject")
        result = DriverHandler.OutputJsonObject.SaveFile()
        if(result != Execution.Passed):
            printFatalDriverError("457: Failed to save ToApplication.json")
            Debug.Error("oh no... err welp, looks like your application will have to figure out itself that the neopixel driver shutted down lmfao! Good luck!")
            Debug.End()
            return Execution.Failed
        
        Debug.Log("Successfully indicated to Application that the driver is no longer operational.")
        Debug.End()
        return Execution.Passed

        Debug.End()
    # -----------------------------------
    def Update() -> Execution:
        """
            Update:
            =======
            Summary:
            --------
            This function is to be called
            each time the animation is completed.

            Returns:
            --------
            - `Execution.Passed` = Updated successfully.
            - `Execution.Failed` = Driver should turn off.
            - `Execution.Crashed` = Fatal error occured while updating.
        """
        Debug.Start("Update")

        result = DriverHandler.InputJsonObject.ReadFile()
        if(result != Execution.Passed):
            Debug.Error("Failed to read file.")
            printFatalDriverError("568: Failed to read JSON")
            NeopixelHandler.currentMode = "OFF"
            DriverHandler.Close()
            Debug.End()
            return Execution.Crashed

        if(DriverHandler.InputJsonObject.jsonData["State"] != "ON"):
            Debug.Log("Driver should turn off now.")
            NeopixelHandler.currentMode = "OFF"
            DriverHandler.Close()
            Debug.End()
            return Execution.Failed

        Debug.End()
        return Execution.Passed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------------------------
class NeopixelHandler:
    #region   --------------------------- DOCSTRING
    """
        NeopixelHandler:
        ================
        Summary:
        --------
        Handles the neopixels depending on given
        parameters. Contains methods and members
        necessary to parse given information
        from your application into LED values.

        `Warning`:
        ----------
        Do not include this class in your main
        application. This is meant to be used
        solely by the BRS python neopixel handler
        for Raspberry Pis.
    """
    #endregion
    #region   --------------------------- MEMBERS
    amountOfLEDs = 0
    """
        amountOfLEDs:
        =============
        Summary:
        --------
        Holds how many LEDs this class needs
        to handle. Defaults to 0.
    """

    pinToUse = board.D18
    """
        pinToUse
        ========
        Summary:
        --------
        Which pin of the Raspberry Pi is
        responsible for the Neopixels.
        Defaults to `board.D18`
    """

    currentMode:str = "OFF"
    """
        currentMode:
        ============
        Summary:
        --------
        Holds the current RGB mode.
        See the class for a list
        of all possible modes.
    """

    pixelObject = None
    """
        pixelObject:
        ============
        Summary:
        --------
        This object holds the neopixel
        object from adafruit circuitPython
        which is directly used to handle
        hardware neopixels.

        Defaults to `None`.
    """

    wantedColors = []
    """
        wantedColors:
        =============
        Summary:
        --------
        A list of lists that holds the wanted
        colors of each LEDs in the strip.
        The lists within this list corresponds
        to individual neopixel's RGB values.

        Values are never to reach higher than
        255 and lower than 0.

        Example:
        --------
        - [[R,G,B], [0,0,0]]
    """
    
    currentColors = []
    """
        currentColors:
        ==============
        Summary:
        --------
        A list of lists that holds the current
        colors of each LEDs in the strip.
        The lists within this list corresponds
        to individual neopixel's RGB values.

        Values are never to reach higher than
        255 and lower than 0.

        Example:
        --------
        - [[R,G,B], [0,0,0]]
    """
    #endregion
    #region   --------------------------- METHODS
    def Initialize() -> Execution:
        """
            Initialize:
            ===========
            Summary:
            --------
            This method tries to
            initialize NeoPixels for a
            Raspberry Pi 4 using GPIO18.
        """
        Debug.Start("Initialize")

        Debug.Log("Getting led count from json.")
        ledCount = DriverHandler.InputJsonObject.jsonData["LedCount"]
        NeopixelHandler.amountOfLEDs = ledCount

        NeopixelHandler.pixelObject = neopixel.NeoPixel(
                                                        NeopixelHandler.pinToUse, 
                                                        NeopixelHandler.amountOfLEDs, 
                                                        brightness=1, 
                                                        auto_write=False, 
                                                        pixel_order=ORDER
                                                        )
        Debug.Log("NeopixelObject was initialized.")
        
        Debug.Log("Closing Neopixels")
        NeopixelHandler.pixelObject.fill((0,0,0))

        Debug.Log("Showing Neopixels")
        NeopixelHandler.pixelObject.show()

        Debug.Log("Initializing wanted and current colors")
        NeopixelHandler.wantedColors = []
        NeopixelHandler.currentColors = []

        for i in range(ledCount):
            NeopixelHandler.wantedColors.append([0,0,0])
            NeopixelHandler.currentColors.append([0,0,0])

        Debug.End()
        return Execution.Passed
    # -------------------------------------------
    def UpdateFromJson() -> Execution:
        """
            UpdateFromJson:
            ===============
            Summary:
            --------
            This function loads the JSON
            from the DriverHandler and
            stores it in this.
        """
        Debug.Start("UpdateFromJson")

        NeopixelHandler.currentLEDMode = DriverHandler.InputJsonObject.jsonData["Mode"]
        
        Debug.Log("Setting wanted colors")
        NeopixelHandler.wantedColors[0] = DriverHandler.InputJsonObject.jsonData["Colors"]["B"]
        NeopixelHandler.wantedColors[1] = DriverHandler.InputJsonObject.jsonData["Colors"]["R"]
        NeopixelHandler.wantedColors[2] = DriverHandler.InputJsonObject.jsonData["Colors"]["S"]

        Debug.End()
        return Execution.Passed
    # -------------------------------------------
    def ShowNewPixels(tick:int, maxTickCount:int) -> Execution:
        """
            ShowNewPixels:
            ==============
            Summary:
            --------
            Calculates and show new neopixels.
            This needs to be called at a fixed
            interval so that its updating
            RGB LEDs smoothly.
        """
        
        #region ---------------------------------- [OFF]
        if(NeopixelHandler.currentMode == RGBModes.off):
            for i in range(NeopixelHandler.amountOfLEDs):
                NeopixelHandler.wantedColors[i] = [0,0,0]
        #endregion

        #region ---------------------------------- [STATIC]
        if(NeopixelHandler.currentMode == RGBModes.static):
            for i in range(NeopixelHandler.amountOfLEDs):
                lerped = GetLerpedColors(NeopixelHandler.currentColors[i], NeopixelHandler.wantedColors[i])
                NeopixelHandler.currentColors[i] = lerped
        #endregion

        #region ---------------------------------- [PULSE]
        if(NeopixelHandler.currentMode == RGBModes.pulse):
            for i in range(NeopixelHandler.amountOfLEDs):

                lerped = GetLerpedColors(NeopixelHandler.currentColors[i], NeopixelHandler.wantedColors[i])

                cycledR = GetCycledColor(lerped[0], tick, maxTickCount, 0)
                cycledG = GetCycledColor(lerped[1], tick, maxTickCount, 0)
                cycledB = GetCycledColor(lerped[2], tick, maxTickCount, 0)

                NeopixelHandler.currentColors[i] = [cycledR, cycledG, cycledB]
        #endregion

        #region ---------------------------------- [CYCLING]
        if(NeopixelHandler.currentMode == RGBModes.cycling):
            for i in range(NeopixelHandler.amountOfLEDs):

                offset = i * 0.15

                cycledR = GetCycledColor(255, tick, maxTickCount, -2.09 + offset)
                cycledG = GetCycledColor(255, tick, maxTickCount, offset)
                cycledB = GetCycledColor(255, tick, maxTickCount, 2.09 + offset)

                NeopixelHandler.currentColors[i] = [cycledR, cycledG, cycledB]
        #endregion

        #region ---------------------------------- [LOADING]
        if(NeopixelHandler.currentMode == RGBModes.loading):
            for i in range(NeopixelHandler.amountOfLEDs):
                NeopixelHandler.wantedColors[i] = [0,0,0]
        #endregion

    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#

if(__name__ == "__main__"):
    Debug.enableConsole = True
    result = DriverHandler.Start()
    if(result != Execution.Passed):
        printFatalDriverError("477: Driver failed to start")
        Debug.Log("Checking if driver is initialized.")
        if(DriverHandler.initialized):
            result = DriverHandler.Close(message="CRASHED")
            if(result != Execution.Passed):
                printFatalDriverError("482: Failed to properly close the driver.")
        printDriverHeader("CRASHED")
    else:
        printDriverHeader("STARTED")

        result = Execution.Passed
        while result == Execution.Passed:
            result = HandleDriver()
            if(result != Execution.Passed):
                printFatalDriverError("836: HandleDriver failed to execute.")
                DriverHandler.Close()
                break
    printDriverHeader("STOPPED")

LoadingLog.End("driver.py")