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
LoadingLog.Start("ADXL343.py")
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
# from ...Utilities.Information import Information
# from ...Utilities.FileHandler import JSONdata, CompareKeys, AppendPath
from ...Utilities.Enums import Execution
from ...Debug.consoleLog import Debug
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
class ADXL343:
    """
        ADXL343:
        ========
        Summary:
        --------
        Backend driver that starts and stop a thread that reads
        i2c accelerometer values from your Raspberry Pi.
    """

    thread = None
    stop_event = threading.Event()
    isStarted: bool = False

    realX = 0
    realY = 0
    realZ = 0
    lock = threading.Lock()

    @staticmethod
    def _reading_thread(ADXLclass):
        counter = 0
        while counter <= 25:
            if ADXLclass.stop_event.is_set():
                break
            print("Counter:", counter)
            counter += 1

            with ADXLclass.lock:
                ADXLclass.realX = counter
                ADXLclass.realY = counter
                ADXLclass.realZ = counter

            time.sleep(0.5)
        ADXLclass.isStarted = False

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts a thread that reads
            an i2c ADXL343 accelerometer
            plugged in SCL and SDA of a
            Raspberry Pi 4 using circuit
            python.
        """
        Debug.Start("StartDriver")
        if ADXL343.isStarted == False:
            if not ADXL343.thread or not ADXL343.thread.is_alive():
                ADXL343.stop_event.clear()
                ADXL343.thread = threading.Thread(target=ADXL343._reading_thread, args=(ADXL343,))
                ADXL343.thread.start()
                ADXL343.isStarted = True
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Thread is already started. You cannot start more than one.")
            Debug.End()
            return Execution.Failed
        Debug.Log("ADXL343 is now started")
        Debug.End()
        return Execution.Passed
# 
    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the thread that reads
            an i2c ADXL343 accelerometer
            plugged in SCL and SDA of a
            Raspberry Pi 4 using circuit
            python.
        """
        Debug.Start("StopDriver")
        ADXL343.stop_event.set()
        if ADXL343.thread and ADXL343.thread.is_alive():
            ADXL343.thread.join()
        Debug.Log("Thread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def GetAccelerometerValues() -> list:
        """
            GetAccelerometerValues:
            =======================
            Summary:
            --------
            Returns the current values
            read by the accelerometer.

            Returns:
            --------
            - [float, float, float]

            Max values are -8 to 8 or something like that.
        """
        Debug.Start("GetAccelerometerValues")
        if ADXL343.isStarted:
            with ADXL343.lock:
                Debug.Log("Returning values from the thread")
                Debug.End()
                return [ADXL343.realX, ADXL343.realY, ADXL343.realZ]
        else:
            Debug.Log("THREAD WAS NOT STARTED. 0 is returned")
            Debug.End()
            return [0, 0, 0]
#====================================================================#
LoadingLog.End("ADXL343.py")