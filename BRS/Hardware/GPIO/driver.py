#====================================================================#
# File Information
#====================================================================#
"""
    driver.py
    =============
    This file contains a python class that starts and stops a thread
    that reads GPIO each X amount of time. That class can also be used
    by your application to detect behaviors of specific GPIO pins.

    DO NOT USE THIS CLASS FOR FAST READINGS. THIS USES TERMINAL AND
    IS NOT EFFICIENT.

    DO NOT EXECUTE THIS FILE MANUALLY.
    ----------------------------------
"""

#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import time
import threading

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ...Utilities.Enums import Execution
from ...Debug.consoleLog import Debug
from .Utilities import GetGPIOInformation, GpioEnum
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class GPIO:
    """
        GPIO:
        =====
        Summary:
        --------
        Backend driver that reads at slow intervals the state
        of all GPIO pins of your Raspberry Pi in a thread by
        using GPIO terminal commands.
    """
    thread = None
    stop_event = threading.Event()
    isStarted: bool = False

    gpioList:list = []
    lock = threading.Lock()

    @staticmethod
    def _reading_thread(gpioClass):
        import time
        while True:
            if gpioClass.stop_event.is_set():
                break

            newListJustDropped = GetGPIOInformation()

            for timeSlept in range(300):
                time.sleep(0.01)
                with gpioClass.lock:
                    gpioClass.gpioList = newListJustDropped
        gpioClass.isStarted = False

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts a thread that reads
            all the informations of GPIO
            pins at intervals of 3 seconds

            Returns:
            --------
        """
        Debug.Start("StartDriver")

        if(Information.platform != "Linux"):
            Debug.Error(f"You cannot use this driver on your platform: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility

        if GPIO.isStarted == False:
            if not GPIO.thread or not GPIO.thread.is_alive():
                GPIO.stop_event.clear()
                GPIO.thread = threading.Thread(target=GPIO._reading_thread, args=(GPIO,))
                GPIO.thread.daemon = True
                GPIO.thread.start()
                GPIO.isStarted = True
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Thread is already started. You cannot start more than one.")
            Debug.End()
            return Execution.Failed
        Debug.Log("GPIO is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the thread that reads
            GPIO pins values through
            terminal.
        """
        Debug.Start("StopDriver")
        GPIO.stop_event.set()
        if GPIO.thread and GPIO.thread.is_alive():
            GPIO.thread.join()

        GPIO.isStarted = False
        Debug.Log("Thread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def GetList() -> list:
        """
            GetList:
            ========
            Summary:
            --------
            Returns a list that contains
            dictionary that explains everything
            about the current GPIO of your
            Raspberry Pi.

            Returns:
            --------
            - [{},{},{} ...]
            - `Execution.Failed` = Thread isn't started.
        """
        Debug.Start("GetList")
        if GPIO.isStarted:
            with GPIO.lock:
                Debug.Log("Returning values from the thread")
                Debug.End()
                return GPIO.gpioList
        else:
            Debug.Log("THREAD WAS NOT STARTED. 0 is returned")
            Debug.End()
            return Execution.Failed

    @staticmethod
    def GetGPIOLevel(gpioNumber:int, accountForPullMode:bool = False) -> bool:
        """
            GetGPIOLevel:
            =============
            Summary:
            --------
            Function that returns the level of a specified
            GPIO number.

            Arguments:
            ----------
            - `gpioNumber:int` = Which GPIO to extract the level from.
            - `accountForPullMode:bool` = Defaults to False. Decides if we should inverse the return if the GPIO is a pull up.

            Returns:
            --------
            - `Execution.Failed` = Thread is not started
            - `Execution.Unecessary` = GPIO could not be found in the current list.
            - `True` = level of GPIO is HIGH - ON - VCC - 3.3V
            - `False` = level of GPIO is LOW - OFF - GND - 0V
        """
        Debug.Start("GetGPIOLevel")

        if(GPIO.isStarted):
            for gpio in GPIO.gpioList:
                if(gpio[GpioEnum.gpio] == gpioNumber):
                    level = gpio[GpioEnum.level]
                    if(accountForPullMode == False):
                        Debug.End()
                        return level==1

                    pull = gpio[GpioEnum.pullMode]
                    if(pull == "UP"):
                        level = 1-level
                    Debug.End()
                    return level==1
            Debug.Warn(f"GPIO {gpioNumber} was not found in the current list.")
            Debug.End()
            return Execution.Unecessary
        else:
            Debug.Log("GPIO THREAD WAS NOT STARTED.")
            Debug.End()
            return Execution.Failed

        Debug.End()
#====================================================================#
LoadingLog.End("driver.py")