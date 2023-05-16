#====================================================================#
# File Information
#====================================================================#
"""
    accelerometerHandler.py
    =======================
    Summary:
    --------
    This file contains the functions and classes necessary
    for a Raspberry Pi to handle an Adafruit ADXl accelerometer
    board.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("accelerometerHandler.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
import sys
import subprocess
import time

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

#====================================================================#
# Classes
#====================================================================#
class Adxl343:
    #region   --------------------------- DOCSTRING
    '''
        Adxl343:
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

        Debug.Log("Verifying Information class...")
        if(not Information.initialized):
            Debug.Error("BRS Information class was not initialized")
            Debug.End()
            return Execution.ByPassed

        if(Information.platform != "Linux"):
            Debug.Error(f"Your platform does not support IOT: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility

        Debug.Log("Setting up JSON")
        result = RGB._InitializeJSON()
        if(result != Execution.Passed):
            Debug.Error(f"The JSON function failed to execute with return code: {result}")
            RGB.initialized = False
            Debug.End()
            return Execution.Failed

        Debug.Log("Jsons successfully initialized.")
        RGB.initialized = True

        Debug.Log("Launching Neopixel driver")
        result = RGB._StartNeoPixelPythonDriver()
        if(result != Execution.Passed):
            Debug.Error("Something went wrong when trying to launch neopixel driver.")
            Debug.End()
            return Execution.Failed
        Debug.Log("DRIVER IS INITIALIZED AND LAUNCHED")

        Debug.Log("Waiting for a reply from the driver...")
        result = RGB._WaitForDriverToIndicateItStarted()
        if(result != Execution.Passed):
            Debug.Error("Something went wrong during the driver's launch.")
            RGB.driverState = False
            Debug.End()
            return Execution.Crashed

        Debug.Log("Neopixel driver is now ON.")
        RGB.driverState = True
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def StopDriver() -> Execution:
        """
            StopDriver:
            ===========
            Summary:
            --------
            This methods stops the python
            driver launched when `StartDriver()`
            was called and returned `Execution.Passed`.
            It will return an `Execution` enumeration
            value that represents what happened when
            the function ran.

            Attention:
            ----------
            This method only tells the driver
            to stop through their JSON files
            pipeline. If the driver is not
            responding, as of now there is no
            way to shut it down by force.

            Returns:
            --------
            - `Execution.Passed` : The driver was stopped successfully.
            - `Execution.Unecessary` : The driver was not running.
            - `Execution.Bypassed` : The RGB class was not initialized
            - `Execution.Failed` : The RGB class failed to stop the Neopixel driver.
        """
        Debug.Start("StopDriver")

        #region -------------------- Checking Initialization
        Debug.Log("Is class initialized?")
        if (not RGB.initialized):
            Debug.Error("Class is not initialized. You cannot stop drivers if JSONs were not created successfully.")
            Debug.End()
            return Execution.ByPassed
        #endregion

        #region -------------------- Checking If Running
        Debug.Log("Is driver supposed to be running?")
        if (not RGB.driverState):
            Debug.Warn("Driver is not supposed to be running. Executing anyways.")
        #endregion

        #region -------------------- Getting state of the driver
        currentDriverState = RGB.GetStateOfDriver()

        if(currentDriverState == Execution.Crashed):
            Debug.Error("FATAL READING ERROR DETECTED.")
            Debug.End()
            return Execution.Crashed

        if(currentDriverState != "ON"):
            Debug.Warn("Driver says its not running...")

            if(currentDriverState == "OFF"):
                Debug.Warn("Driver says its already OFF.")

            if(currentDriverState == "CRASHED"):
                Debug.Error("Driver says it crashed.")
        else:
            Debug.Log("Driver is currently running.")
        #endregion

        #region -------------------- Closing driver
        result = RGB._StopNeoPixelPythonDriver()
        if(result != Execution.Passed):
            Debug.Error("Something went wrong and the class could not tell the driver to stop.")
            Debug.End()
            return Execution.Failed
        Debug.Log("JSON was updated successfully.")
        #endregion

        #region -------------------- Waiting for driver to stop
        result = RGB._WaitForDriverToIndicateItStopped()
        if(result != Execution.Passed):
            Debug.Error("The driver did not stop despite us asking it to.")
            Debug.End()
            return Execution.Failed
        #endregion

        Debug.Log("Driver successfully indicated it stopped.")
        Debug.End()
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
            subprocess.Popen(['sudo', 'python', path, '&'])
        #endregion
        Debug.Log("Success. Driver is launched.")
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def _StopNeoPixelPythonDriver() -> Execution:
        """
            _StopNeoPixelPythonDriver:
            ==========================
            Summary:
            --------
            This private method tells
            the Neopixel driver to stop
            running by setting ToDriver.json's
            wanted driver state to `OFF`.
            It does not directly force shutdown
            the driver.

            Attention:
            ----------
            This is a private method, calling
            this manually WILL cause issues
            and potential crashes. Use
            `StopDriver()` instead.

            Returns:
            --------
            - `Execution.Passed` : JSON updated successfully.
            - `Execution.Crashed` : Fatal error occurred during JSON handling
            - `Execution.Failed` : Something went wrong during the handling of the JSON files.
        """
        Debug.Start("_StopNeoPixelPythonDriver")

        #region -------------------- Try to set JSON to OFF
        Debug.Log("Trying to set ToDriver.json to OFF")
        try:
            RGB.ToDriverJsonObject.jsonData["State"] = "OFF"
            Debug.Log(">>> Success")
        except:
            Debug.Error("579: Fatal error occurred when trying to set ToDriver.json's [\"State\"] to \"OFF\"")
            Debug.End()
            return Execution.Crashed
        #endregion

        #region -------------------- Saving the JSON
        Debug.Log("Trying to save ToDriver.json ...")
        result = RGB.ToDriverJsonObject.SaveFile()
        if(result == False):
            Debug.Error("Failed to save ToDriver.json")
            Debug.End()
            return Execution.Crashed
        Debug.Log(">>> Success")
        #endregion

        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def GetStateOfDriver(showDebuggingPrints:bool=False) -> Execution:
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
        Debug.Start("GetStateOfDriver", DontDebug = (not showDebuggingPrints))

        if(RGB.initialized):

            result = RGB.ToApplicationJsonObject.ReadFile()
            if(result != True):
                Debug.Error("Failed to read the file.")
                Debug.End(ContinueDebug=True)
                return Execution.Crashed

            Debug.Log("File read successfully.")

            state = RGB.ToApplicationJsonObject.jsonData["State"]
            Debug.Log("Successfully returned the driver's current state")
            Debug.End(ContinueDebug=True)
            return state

        else:
            Debug.Error("Tried to get state from uninitialized class")
            Debug.End(ContinueDebug=True)
            return Execution.Failed
    # -----------------------------------
    def SetAttributes(colors:list = None,
            rgbMode:RGBModes = None,
            brightness:float = None,
            ledCount:int = None,
            animationDuration:int = None,
            lerpDelta:float = None,
            blinkPeriod:int = None,
            blinkMode:str = None,
            blinkCount:list = None,
            ledToUse:list = None) -> Execution:
        """
            SetAttributes:
            ==============
            Summary:
            --------
            This method allows you to tell
            the Neopixel driver to update any
            of the elements you give it.
            Note that you need to have started
            the driver prior to calling this
            method.

            Arguments:
            ----------
            - `colors`: List of ints ranging from 0 to 255 [Red,Green,Blue]. Or lists of lists: [[Red,Green,Blue]]
            - `rgbMode`: The LED mode that is wanted. See `RGBModes` for possible values.
            - `brightness`: float ranging from 0 to 1 indicating how bright the LEDs should be.
            - `ledCount`: How many LEDs does the driver need to drive.
            - `animationDuration` : How long is an animation? (seconds 1 = 1 seconds)
            - `lerpDelta` : Smoothening given to the LEDs when they change colors. Set to 1 for no smoothening. DONT SET TO 0.
            - `blinkPeriod` : How long do LEDs stay ON or OFF when in blinking mode? (1 = 1 seconds, 0.01 = 10 milliseconds)
            - `blinkMode` : How does the blinking work? `"SEQUENTIAL"` = LEDs blink one after the other. `"NORMAL"` = Everything blinks at the same time
            - `blinkCount` : How many blinks per animation? Either an int or a list of ints representing blinks for each LEDs.
            - `ledToUse` : List of boolean telling the driver which LED to use and which to turn off.

            Returns:
            --------
            - `Execution.Passed` = Everything worked out.
            - `Execution.Failed` = Some values were incorrect.
            - `Execution.Crashed` = Fatal json handling error
            - `Execution.Unecessary` = You gave no arguments...
        """
        Debug.Start("Set")
        updateTheJson = False

        if(rgbMode != None):
            Debug.Log(f"Changing wanted mode to {rgbMode}")
            RGB.ToDriverJsonObject.jsonData["Mode"] = rgbMode
            updateTheJson = True

        if(colors != None):
            Debug.Log(f"Changing wanted color to {str(colors)}")
            amountOfLed = RGB.ToDriverJsonObject.jsonData["LedCount"]
            if(type(colors[0]) != int):
                length = len(colors[0])
                if(length == 3):
                    Debug.Log("Multiple colors specified")
                    for ledNumber in range(length):
                        RGB.ToDriverJsonObject.jsonData["Colors"][ledNumber] = colors[ledNumber]
                else:
                    Debug.Error(f"INVALID COLOR(S) SPECIFIED: {colors}")
            else:
                Debug.Log("Only 1 color specified.")
                for ledNumber in range(amountOfLed):
                    RGB.ToDriverJsonObject.jsonData["Colors"][ledNumber] = colors
            updateTheJson = True

        if(brightness != None):
            if(brightness > 1 or brightness < 0):
                Debug.Error("INVALID BRIGHTNESS")
                Debug.End()
                return Execution.Failed
            else:
                RGB.ToDriverJsonObject.jsonData["Brightness"] = brightness
                updateTheJson = True

        if(ledCount != None):
            if(ledCount < 1 or ledCount > 50):
                Debug.Error(f"INVALID LED COUNT: {ledCount}")
                Debug.End()
                return Execution.Failed
            else:
                RGB.ToDriverJsonObject.jsonData["LedCount"] = ledCount
                updateTheJson = True

        if(animationDuration != None):
            if(animationDuration < 0.25 or animationDuration > 60):
                Debug.Error(f"INVALID ANIMATION DURATION: {animationDuration}")
                Debug.End()
                return Execution.Failed
            else:
                RGB.ToDriverJsonObject.jsonData["Animation"]["Duration"] = animationDuration
                updateTheJson = True

        if(lerpDelta != None):
            if(lerpDelta < 0 or lerpDelta > 1):
                Debug.Error(f"INVALID LERP DELTA: {lerpDelta}")
                Debug.End()
                return Execution.Failed
            else:
                RGB.ToDriverJsonObject.jsonData["Animation"]["LerpDelta"] = lerpDelta
                updateTheJson = True

        if(blinkPeriod != None):
            if(blinkPeriod < 0.02 or blinkPeriod > 5):
                Debug.Error(f"INVALID BLINK PERIOD: {blinkPeriod}")
                Debug.End()
                return Execution.Failed
            else:
                RGB.ToDriverJsonObject.jsonData["Animation"]["BlinkPeriod"] = blinkPeriod
                updateTheJson = True

        if(blinkMode != None):
            if(blinkMode != "SEQUENTIAL" and blinkMode != "NORMAL"):
                Debug.Error(f"INVALID BLINK MODE: {blinkMode}")
                Debug.End()
                return Execution.Failed
            else:
                RGB.ToDriverJsonObject.jsonData["Animation"]["BlinkMode"] = blinkMode
                updateTheJson = True

        if(blinkCount != None):
            amountToBlink = 0
            try:
                amountToBlink = len(blinkCount)
                if(amountToBlink < RGB.ToDriverJsonObject.jsonData["Animation"]["BlinkCount"]):
                    Debug.Error("SPECIFIED ARRAY IS SMALLER THAN LEDCOUNT")
                    Debug.End()
                    return Execution.Failed
                RGB.ToDriverJsonObject.jsonData["Animation"]["BlinkCount"] = blinkCount
                updateTheJson = True
            except:
                if(blinkCount < 0 or blinkCount > 100):
                    Debug.Error(f"INVALID BLINK COUNT: {blinkCount}")
                    Debug.End()
                    return Execution.Failed
                else:
                    for led in RGB.ToDriverJsonObject.jsonData["Animation"]["BlinkCount"]:
                        RGB.ToDriverJsonObject.jsonData["Animation"]["BlinkCount"][led] = blinkCount
                    updateTheJson = True

        if(ledToUse != None):
            try:
                amountOfLed = len(ledToUse)
                amountOfLedToHave = RGB.ToDriverJsonObject.jsonData["LedCount"]
                if(amountOfLed < amountOfLedToHave):
                    Debug.Error(f"INVALID LED TO USE: {ledToUse}. List needs to have {amountOfLedToHave} spots")
                    Debug.End()
                    return Execution.Failed

                updateTheJson = True
                RGB.ToDriverJsonObject.jsonData["Animation"]["LEDToUse"] = ledToUse
            except:
                Debug.Error("FATAL ERROR WHILE PARSING LED TO USE.")
                Debug.End()
                return Execution.Failed

        if(not updateTheJson):
            Debug.Warn("Function called without any given parameters")
            Debug.End()
            return Execution.Unecessary

        Debug.Log("Updating json.")
        result = RGB.ToDriverJsonObject.SaveFile()
        if(result != True):
            Debug.Error("Failed to save file.")
            Debug.End()
            return Execution.Crashed
        
        Debug.Log("Values were updated!")
        Debug.End()
        return Execution.Passed
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
    # -----------------------------------
    def _WaitForDriverToIndicateItStopped() -> Execution:
        """
            _WaitForDriverToIndicateItStopped:
            ==================================
            Summary:
            --------
            Private method that waits for
            ToApplication.json to say that the
            driver is OFF. There is a 1 second
            timeout.

            Returns:
            --------
            - `Execution.Passed` = Driver stopped and its state is now OFF
            - `Execution.Crashed` = Driver says that it crashed.
            - `Execution.Failed` = Timeout was reached... Driver is still going
        """
        Debug.Start("_WaitForDriverToIndicateItStopped")
        timeout:float = 1000
        secondsToWaitBetweenSteps:float = 0.1
        currentAttempt:int = 0

        Debug.Log("Start of reading attemps...")

        for currentMillisecond in range(timeout):
            if (currentMillisecond % 100 == 0):
                time.sleep(secondsToWaitBetweenSteps)
                currentAttempt = currentAttempt + 1

                currentDriverState = RGB.GetStateOfDriver()
                if(currentDriverState != "OFF" or currentDriverState != "CRASHED"):
                    Debug.Error("Driver is still running...")
                else:
                    Debug.Log(f"Driver is OFF after {currentAttempt} reading attempts.")
                    Debug.End()
                    return Execution.Passed

        Debug.Error(f"Driver is still ON after {currentAttempt} attempts over a period of {timeout} milliseconds!")
        Debug.End()
        return Execution.Failed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("rgbDriverHandler.py")