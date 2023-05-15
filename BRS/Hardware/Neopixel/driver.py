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
    currentAnimationPeriod:float = 0

    currentSequencedLed:int = 0

    blinkState:bool = False
    """
        Oscillates between True and False each time the
        period count is reached.
    """

    blinkCounter:int = 0

    halfPeriodCounter:int = 0

    aboveHalfAnimationDuration:bool = True
    """Flips its state each time half an animation is completed."""

    animationFlipFlop:bool = False
    """ Changes state each time an animation is finished """

    currentLedToDisplay:int = 0
    """ Incremented each time the current tick divided by time per led returns 0"""

    currentLedToDisplayCounter:float = 0
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
    "Version" : 1.1,
    "LedCount": 3,
    "State" : "OFF",
    "Brightness" : 1,
    "Mode": "CUSTOM",
    "Colors": [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ],
    "Animation":{
        "Duration" : 1000,
        "LerpDelta" : 0.01,
        "BlinkPeriod": 100,
        "BlinkMode" : "SEQUENTIAL",
        "BlinkCount" : [0,0,0],
        "LEDToUse" : [False, False, False]
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
    ```
    {
        "Version" : 1.1,
        "LedCount": 3,
        "State" : "OFF",
        "Brightness" : 1,
        "Mode": "CUSTOM",
        "Colors": [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ],
        "Animation":{
            "Duration" : 1000,
            "LerpDelta" : 0.01,
            "BlinkPeriod": 100,
            "BlinkMode" : "SEQUENTIAL",
            "BlinkCount" : [0,0,0],
            "LEDToUse" : [False, False, False]
        }
    }
    ```

    Values:
    --------
    - `Version` : The JSON's version.
    - `LedCount` : How many LEDs the driver needs to drive. This directly impacts `Colors`
    - `State` : Wanted driver state. "ON" = The driver needs to run. "OFF" the driver will turn off.
    - `Brightness` : Value from 0 to 1 that sets how bright the LEDs can be.
    - `Mode` : See `RGBModes` class.
    - `Colors` : A list of lists of 3 elements [R,G,B]. each element can only go from 0 to 255.
    - `Animation`: Dictionary containing animation properties.
        - `Duration` : How long, in milliseconds, will an animation last.
        - `LerpDelta` : How much delta to apply to leds. Set to 1 for none.
        - `BlinkPeriod` : How long should an LED stay on during blinking.
        - `BlinkCounts`: List of how many times each LEDs should blink.
        - `BlinkMode` : The blinking mode. "SEQUENTIAL" = LEDs blink one after the other. "NORMAL" = Everything blinks at the same time.
        - `LEDToUse` : List of boolean indicating which LED should be used in the animation.
"""

listOfKeyA = ["Version", "LedCount","State","Brightness","Mode","Colors","Animation"]
listOfKeyB = ["Duration", "LerpDelta","BlinkPeriod","BlinkMode","BlinkCount","LEDToUse"]

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

        Members:
        --------
        - `off` = All LEDs will turn off.
        - `static` = All LEDs will display a static color.
        - `cycling` = RGB Gamer mode
        - `pulse` = LEDs are pulsed one after the other depending on BlinkMode
        - `loading` = LEDs display a loading animation.
        - `blink` = LEDs blink according to set Animation properties.
    """
    off:str = "OFF"
    static:str = "STATIC"
    cycling:str = "CYCLING"
    pulse:str = "PULSE"
    loading:str = "LOADING"
    blink:str = "BLINK"
#====================================================================#
# Global RGB functions
#====================================================================#
def GetCycledColor(colorToCycle, RadianOffset) -> float:
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
    ratio = GlobalVariables.currentAnimationTick / NeopixelHandler.animationDuration
    ratio = ratio * 6.28

    temporary = math.sin(ratio + RadianOffset)
    temporary = math.pow(temporary, 4) * colorToCycle

    return temporary
# -------------------------------------------------------------------
def GetLerpedColors(currentColors:list, wantedColors:list, globalDelta:float):
    """
        GetLerpedColor:
        ===============
        Summary:
        --------
        Returns a lerped singular color.
    """
    wantedR = wantedColors[0]
    wantedG = wantedColors[1]
    wantedB = wantedColors[2]

    currentR = currentColors[0]
    currentG = currentColors[1]
    currentB = currentColors[2]

    def Lerp(current,wanted):
        return current * (1-globalDelta) + wanted * globalDelta

    newR = Lerp(currentR, wantedR)
    newG = Lerp(currentG, wantedG)
    newB = Lerp(currentB, wantedB)

    # print("------------------------------------------------")
    # print(f"current:  R:{currentR}, G:{currentG}, B:{currentB}")
    # print(f"wanted:   R:{currentR}, G:{currentG}, B:{currentB}")
    # print(f"resulted: R:{currentR}, G:{currentG}, B:{currentB}")

    return [newR, newG, newB]
# -------------------------------------------------------------------
def GetBlinkedColor(wantedColor:list, blinkMode:str, ledNumber:int) -> list:
    pass
# -------------------------------------------------------------------
def CalculateMultiplierIfLedIsUsed(currentList:list, ledIsUsed:bool) -> list:
    if(ledIsUsed):
        return currentList
    else:
        lerped = GetLerpedColors(currentList, [0,0,0], NeopixelHandler.lerpDelta/255)
        return lerped
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
    GlobalVariables.currentAnimationPeriod = GlobalVariables.currentAnimationPeriod + ANIMATION_NEW_FRAME_DELAY
    GlobalVariables.currentLedToDisplayCounter = GlobalVariables.currentLedToDisplayCounter + ANIMATION_NEW_FRAME_DELAY

    # counts up to X amount of LED in a single animation.
    if(GlobalVariables.currentLedToDisplayCounter >= (NeopixelHandler.animationDuration / NeopixelHandler.amountOfLEDs)):
        GlobalVariables.currentLedToDisplayCounter = 0

        if(GlobalVariables.currentLedToDisplay > NeopixelHandler.amountOfLEDs - 1):
            GlobalVariables.currentLedToDisplay = 0
        else:
            GlobalVariables.currentLedToDisplay = GlobalVariables.currentLedToDisplay + 1
        print(GlobalVariables.currentLedToDisplay)

    # Used to tell when we reached half the animation's duration.
    if(GlobalVariables.currentAnimationTick > NeopixelHandler.animationDuration/2):
        GlobalVariables.aboveHalfAnimationDuration = True
    else:
        GlobalVariables.aboveHalfAnimationDuration = False

    if(GlobalVariables.currentAnimationPeriod >= NeopixelHandler.animationPeriod):
        GlobalVariables.currentAnimationPeriod = 0
        GlobalVariables.halfPeriodCounter = GlobalVariables.halfPeriodCounter + 1

        if(GlobalVariables.halfPeriodCounter == 1):
            GlobalVariables.blinkState = True
            GlobalVariables.blinkCounter = GlobalVariables.blinkCounter + 1
            GlobalVariables.halfPeriodCounter = 0

            #Leds blinks one after the other.
            if(NeopixelHandler.blinkMode == "SEQUENTIAL"):
                if (GlobalVariables.blinkCounter >= NeopixelHandler.blinkCounts[GlobalVariables.currentSequencedLed]):
                    GlobalVariables.blinkCounter = 0
                    GlobalVariables.currentSequencedLed = GlobalVariables.currentSequencedLed + 1

                    if(GlobalVariables.currentSequencedLed > NeopixelHandler.amountOfLEDs-1):
                        GlobalVariables.currentSequencedLed = 0
        else:
            GlobalVariables.blinkState = False


    if(int((GlobalVariables.currentAnimationTick*100)%10) == 0):
        # Time to update the JSONs!
        result = DriverHandler.Update()
        if(result != Execution.Passed):
            printDriverHeader("STOPPING")
            NeopixelHandler.currentMode = "OFF"
            NeopixelHandler.CalculateColorMultipliers(GlobalVariables.currentAnimationTick, ANIMATION_DURATION)
            NeopixelHandler.UpdatePixelsWithCurrentValues(dontShowDebugTraceback=True)
            return result
        result = NeopixelHandler.UpdateFromJson()
        if(result != Execution.Passed):
            printDriverHeader("STOPPING")
            NeopixelHandler.currentMode = "OFF"
            NeopixelHandler.CalculateColorMultipliers(GlobalVariables.currentAnimationTick, ANIMATION_DURATION)
            NeopixelHandler.UpdatePixelsWithCurrentValues(dontShowDebugTraceback=True)
            return result

    # Reached the end of the animation duration. Everything is reset.
    if(GlobalVariables.currentAnimationTick > NeopixelHandler.animationDuration):
        GlobalVariables.currentAnimationTick = 0
        GlobalVariables.currentSequencedLed = 0
        GlobalVariables.currentAnimationPeriod = 0
        GlobalVariables.currentLedToDisplay = 0
        GlobalVariables.currentLedToDisplayCounter = 0
        GlobalVariables.animationFlipFlop = not GlobalVariables.animationFlipFlop
        NeopixelHandler.UpdateFromJson()

    # Update the LEDs.
    NeopixelHandler.CalculateColorMultipliers(GlobalVariables.currentAnimationTick, ANIMATION_DURATION)
    NeopixelHandler.UpdatePixelsWithCurrentValues(dontShowDebugTraceback=True)
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
            printFatalDriverError("537: FAILED TO GET DATA FROM ToDriver.json")
            Debug.End()
            return Execution.Crashed
        Debug.Log("File's content gathered successfully.")
        #endregion

        #region ------------------------- Comparing file content with expected content
        Debug.Log("Comparing JSON content...")
        result = CompareKeys(_defaultToDriverJsonStructure, DriverHandler.InputJsonObject.jsonData)
        if(result != FileIntegrity.Good):
            Debug.Error("JSON file's data does not match expected data")
            printFatalDriverError("548: ToDriver.py has corrupted data in it.")
        #endregion
        
        #region ------------------------- Reading State of ToDriver
        Debug.Log("Reading JSON driver state...")
        try:
            if(DriverHandler.InputJsonObject.jsonData["State"] != "ON"):
                Debug.Log("Driver should close")
                printFatalDriverError("556: Driver started with json set to OFF...")
                Debug.End()
                return Execution.Failed
            Debug.Log("State is ON, the application wants to handle LEDs")
        except:
            Debug.Error("FATAL: Crashed when attempting to set STATE to ON")
            printFatalDriverError("562: Crashed when trying to read if ToDriver's state is ON")
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
        if(result != True):
            printFatalDriverError("607: Failed to save ToApplication.json")
            Debug.Error("oh no... err welp, looks like your application will have to figure out itself that the neopixel driver shutted down lmfao! Good luck!")
            Debug.End()
            return Execution.Failed

        Debug.Log("Successfully indicated to Application that the driver is no longer operational.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def GetAttribute(valueA:str, valueB:str=None) -> Execution:
        """
            GetAttribute:
            =============
            Summary:
            --------
            This method returns an attribute
            from the ToDriver.json file and
            allows easy handling of the JSON
            object responsible for it.

            Arguments:
            ----------
            -`valueA:str` = First key in the dictionary
            -`valueB:str` = Optional second key within the first key.

            Example:
            --------
            - How to get the animation duration?

            ```
                currentDuration = DriverHandler.GetAttribute("Animation", "Duration")
            ```

            - How to get all the colors?

            ```
                listOfAllColors = DriverHandler.GetAttribute("Colors")
            ```

            - How to get the color of the first pixel?

            ```
                colorOfPixelA = DriverHandler.GetAttribute("Colors", 0)
            ```
        """
        Debug.Start("GetAttribute")

        if (valueA not in listOfKeyA):
            Debug.Error(f"{valueA} is not a valid first key.")
            Debug.End()
            return Execution.Failed

        if(valueB != None):
            if(valueB not in listOfKeyB):
                if(valueA == "Colors" and type(valueB) != "int"):
                    Debug.Error(f"Invalid second key for colors: {valueB}")
                    Debug.End()
                    return Execution.Failed
                elif (valueA != "Colors"):
                    Debug.Error(f"Invalid second key: {valueB}")
                    Debug.End()
                    return Execution.Failed

            Debug.Log(">>> SUCCESS")
            Debug.End()
            return DriverHandler.InputJsonObject.jsonData[valueA][valueB]
        else:
            Debug.Log(">>> SUCCESS")
            Debug.End()
            return DriverHandler.InputJsonObject.jsonData[valueA]
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
        if(result != True):
            Debug.Error("Failed to read file.")
            printFatalDriverError("638: Failed to read JSON")
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

    currentColorMultipliers = []
    """
        lists of lists of values between 0 and 1
        that represents how much each color should
        be present on each LED. This is used
        to smooth out transitions between colors.
    """
    wantedColorMultipliers = []

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

    brightness = 1
    animationDuration = 1
    lerpDelta = 0.01
    animationPeriod = 0.02
    blinkMode = "NORMAL"
    blinkCounts = [1,1,1]
    ledsToUse = [True, True, True]
    blinkerCounter = []
    """
        Keeps count of how many blinks each LEDs made.
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
        NeopixelHandler.colorMultipliers = []

        for i in range(ledCount):
            NeopixelHandler.wantedColors.append([0,0,0])
            NeopixelHandler.currentColors.append([0,0,0])
            NeopixelHandler.currentColorMultipliers.append([1,1,1])
            NeopixelHandler.wantedColorMultipliers.append([1,1,1])
            NeopixelHandler.blinkerCounter.append(0)

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

        NeopixelHandler.currentMode         = DriverHandler.GetAttribute("Mode")
        NeopixelHandler.amountOfLEDs        = DriverHandler.GetAttribute("LedCount")
        NeopixelHandler.brightness          = DriverHandler.GetAttribute("Brightness")
        NeopixelHandler.animationDuration   = DriverHandler.GetAttribute("Animation", "Duration")
        NeopixelHandler.wantedColors        = DriverHandler.GetAttribute("Colors")
        NeopixelHandler.lerpDelta           = DriverHandler.GetAttribute("Animation", "LerpDelta")
        NeopixelHandler.animationPeriod     = DriverHandler.GetAttribute("Animation", "BlinkPeriod")
        NeopixelHandler.blinkMode           = DriverHandler.GetAttribute("Animation", "BlinkMode")
        NeopixelHandler.blinkCounts         = DriverHandler.GetAttribute("Animation", "BlinkCount")
        NeopixelHandler.ledsToUse           = DriverHandler.GetAttribute("Animation", "LEDToUse")

        errorOccurred = False
        if(NeopixelHandler.currentMode == Execution.Failed):
            printFatalDriverError("1022: currentMode GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.amountOfLEDs == Execution.Failed):
            printFatalDriverError("1024: amountOfLEDs GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.brightness == Execution.Failed):
            printFatalDriverError("1026: brightness GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.animationDuration == Execution.Failed):
            printFatalDriverError("1028: animationDuration GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.wantedColors == Execution.Failed):
            printFatalDriverError("1029: wantedColors GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.lerpDelta == Execution.Failed):
            printFatalDriverError("1032: lerpDelta GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.animationPeriod == Execution.Failed):
            printFatalDriverError("1034: animationPeriod GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.blinkMode == Execution.Failed):
            printFatalDriverError("1036: blinkMode GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.blinkCounts == Execution.Failed):
            printFatalDriverError("1038: blinkCounts GetAttribute failed")
            errorOccurred = True
        if(NeopixelHandler.ledsToUse == Execution.Failed):
            printFatalDriverError("1040: ledsToUse GetAttribute failed")
            errorOccurred = True

        if(errorOccurred):
            Debug.Error("Something went hella wrong")
            Debug.End()
            return Execution.Failed

        Debug.End()
        return Execution.Passed
    # -------------------------------------------
    def CalculateColorMultipliers(tick:int, maxTickCount:int) -> Execution:
        """
            CalculateColorMultipliers:
            ==============
            Summary:
            --------
            Calculates the current values of
            color multipliers depending on modes.
            This needs to be called at a fixed
            interval so that its updating
            RGB LEDs smoothly. Please note that
            this function does not account for the
            speed at which ticks are executed.

            Arguments:
            ----------
            - `tick:int` = the current tick that the animation is at.
            - `maxTickCount:int` = The maximum ticks in an animation.
        """
        if(DriverHandler.initialized != True):
            printFatalDriverError("846: Attempting to Update pixels while driver is not initialized")
            return Execution.Failed

        for ledNumber in range(NeopixelHandler.amountOfLEDs):
            ledIsUsed = NeopixelHandler.ledsToUse[ledNumber]
            if(ledIsUsed):
                lerped = CalculateMultiplierIfLedIsUsed(NeopixelHandler.currentColorMultipliers[ledNumber], ledIsUsed)
                NeopixelHandler.currentColorMultipliers[ledNumber] = lerped
            else:
                #region ---------------------------------- [OFF]
                if(NeopixelHandler.currentMode == RGBModes.off):
                    lerped = GetLerpedColors(NeopixelHandler.currentColorMultipliers[ledNumber], [0,0,0], NeopixelHandler.lerpDelta)
                    NeopixelHandler.currentColorMultipliers[ledNumber] = lerped
                #endregion

                #region ---------------------------------- [STATIC]
                if(NeopixelHandler.currentMode == RGBModes.static):
                    lerped = GetLerpedColors(NeopixelHandler.currentColorMultipliers[ledNumber],
                                             [NeopixelHandler.brightness, NeopixelHandler.brightness, NeopixelHandler.brightness],
                                             NeopixelHandler.lerpDelta)
                    NeopixelHandler.currentColorMultipliers[ledNumber] = lerped
                #endregion

                #region ---------------------------------- [PULSE]
                if(NeopixelHandler.currentMode == RGBModes.pulse):
                    multiplierToCycle = NeopixelHandler.wantedColorMultipliers[ledNumber]
                    wantedR = GetCycledColor(multiplierToCycle[0], 0)
                    wantedG = GetCycledColor(multiplierToCycle[1], 0)
                    wantedB = GetCycledColor(multiplierToCycle[2], 0)

                    NeopixelHandler.currentColorMultipliers[ledNumber] = [wantedR, wantedG, wantedB]
                #endregion

                #region ---------------------------------- [CYCLING]
                if(NeopixelHandler.currentMode == RGBModes.cycling):
                    offset = ledNumber * 0.15

                    multiplierToCycle = NeopixelHandler.wantedColorMultipliers[ledNumber]
                    wantedR = GetCycledColor(multiplierToCycle[0], -2.09 + offset)
                    wantedG = GetCycledColor(multiplierToCycle[1], offset)
                    wantedB = GetCycledColor(multiplierToCycle[2], 2.09 + offset)

                    NeopixelHandler.currentColorMultipliers[ledNumber] = [wantedR, wantedG, wantedB]
                #endregion

                #region ---------------------------------- [LOADING]
                if(NeopixelHandler.currentMode == RGBModes.loading):

                    if(GlobalVariables.animationFlipFlop):
                        if(ledNumber <= GlobalVariables.currentLedToDisplay):
                            lerped = GetLerpedColors(NeopixelHandler.currentColorMultipliers[ledNumber],
                                                    [NeopixelHandler.brightness, NeopixelHandler.brightness, NeopixelHandler.brightness],
                                                    NeopixelHandler.lerpDelta)
                            NeopixelHandler.currentColorMultipliers[ledNumber] = lerped
                        else:
                            lerped = GetLerpedColors(NeopixelHandler.currentColorMultipliers[ledNumber],
                                                    [0, 0, 0],
                                                    NeopixelHandler.lerpDelta)
                            NeopixelHandler.currentColorMultipliers[ledNumber] = lerped
                    else:
                        lerped = GetLerpedColors(NeopixelHandler.currentColorMultipliers[ledNumber],
                                                [0, 0, 0],
                                                NeopixelHandler.lerpDelta)
                        NeopixelHandler.currentColorMultipliers[ledNumber] = lerped

                #endregion

        return Execution.Passed
    # -------------------------------------------
    def UpdatePixelsWithCurrentValues(dontShowDebugTraceback:bool = False) -> Execution:
        """
            UpdatePixelsWithCurrentValues:
            ==============================
            Summary:
            --------
            This method will update the hardware
            circuit python classes with the current
            values stored in the current list.

            Each list's values is checked manually
            by this function and prints are given
            if anything isn't within 0 to 255.
        """
        Debug.Start("UpdatePixelsWithCurrentValues", DontDebug=dontShowDebugTraceback)

        # Updating pixel object with current LEDs
        for ledNumber in range(NeopixelHandler.amountOfLEDs):

            # lerp current color with wanted color
            lerpedColors = GetLerpedColors(NeopixelHandler.currentColors[ledNumber], NeopixelHandler.wantedColors[ledNumber], NeopixelHandler.lerpDelta)
            NeopixelHandler.currentColors[ledNumber] = lerpedColors

            multipliers = NeopixelHandler.currentColorMultipliers[ledNumber]

            red   = lerpedColors[0] * multipliers[0]
            green = lerpedColors[1] * multipliers[1]
            blue  = lerpedColors[2] * multipliers[2]

            if(red > 255 or red < 0):
                printFatalDriverError(f"Red isn't within allowed range: {red}")
                Debug.End(ContinueDebug=True)
                return Execution.Failed

            if(green > 255 or green < 0):
                printFatalDriverError(f"Green isn't within allowed range: {green}")
                Debug.End(ContinueDebug=True)
                return Execution.Failed

            if(blue > 255 or blue < 0):
                printFatalDriverError(f"Blue isn't within allowed range: {blue}")
                Debug.End(ContinueDebug=True)
                return Execution.Failed

            intRed = int(red)
            intGreen = int(green)
            intBlue = int(blue)

            NeopixelHandler.pixelObject[ledNumber] = [intRed, intGreen, intBlue]

        NeopixelHandler.pixelObject.show()

        Debug.End(ContinueDebug=True)
        return Execution.Passed
    # -------------------------------------------
    def Close():
        """
            Close:
            ======
            Summary:
            --------
            Closes all the LEDs. This is called when
            the driver shuts down.
        """
        Debug.Start("Close")

        NeopixelHandler.pixelObject.fill([0, 0, 0])
        NeopixelHandler.pixelObject.show()

        Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#

if(__name__ == "__main__"):
    Debug.enableConsole = False
    result = DriverHandler.Start()
    if(result != Execution.Passed):
        printFatalDriverError("910: Driver failed to start")
        Debug.Log("Checking if driver is initialized.")
        if(DriverHandler.initialized):
            result = DriverHandler.Close(message="CRASHED")
            if(result != Execution.Passed):
                printFatalDriverError("915: Failed to properly close the driver.")
        printDriverHeader("CRASHED")
    else:
        printDriverHeader("STARTED")

        result = NeopixelHandler.Initialize()
        if(result != Execution.Passed):
            printDriverHeader("NEOPIXEL FAIL")
            DriverHandler.Close(message="CRASHED")

        result = Execution.Passed
        while result == Execution.Passed:
            result = HandleDriver()
            if(result != Execution.Passed):
                printFatalDriverError("929: HandleDriver failed to execute. Closing.")
                DriverHandler.Close()
                break
        NeopixelHandler.Close()
        DriverHandler.Close()
    printDriverHeader("STOPPED")
    print("LAST VALUES WERE:")
    print(f"amountOfLEDs:               {NeopixelHandler.amountOfLEDs}")
    print(f"animationDuration:          {NeopixelHandler.animationDuration}")
    print(f"animationPeriod:            {NeopixelHandler.animationPeriod}")
    print(f"blinkCounts:                {NeopixelHandler.blinkCounts}")
    print(f"blinkerCounter:             {NeopixelHandler.blinkerCounter}")
    print(f"blinkMode:                  {NeopixelHandler.blinkMode}")
    print(f"brightness:                 {NeopixelHandler.brightness}")
    # print(f"currentColorMultipliers:    {NeopixelHandler.currentColorMultipliers}")
    # print(f"currentColors:              {NeopixelHandler.currentColors}")
    print(f"currentMode:                {NeopixelHandler.currentMode}")
    print(f"ledsToUse:                  {NeopixelHandler.ledsToUse}")
    print(f"lerpDelta:                  {NeopixelHandler.lerpDelta}")
    # print(f"wantedColorMultipliers:     {NeopixelHandler.wantedColorMultipliers}")
    # print(f"wantedColors:               {NeopixelHandler.wantedColors}")

LoadingLog.End("driver.py")