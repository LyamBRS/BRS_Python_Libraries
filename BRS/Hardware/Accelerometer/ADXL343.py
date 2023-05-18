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

        import time
        import board
        import busio
        import adafruit_adxl34x

        i2c = busio.I2C(board.SCL, board.SDA)
        accelerometer = adafruit_adxl34x.ADXL345(i2c)

        while True:
            if ADXLclass.stop_event.is_set():
                break

            xyz = accelerometer.acceleration

            with ADXLclass.lock:
                ADXLclass.realX = xyz[0]
                ADXLclass.realY = xyz[1]
                ADXLclass.realZ = xyz[2]

            # time.sleep(1)
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

    @staticmethod
    def GetValue_X_Positive() -> float:
        """
            GetValue_X_Positive:
            ====================
            Summary:
            --------
            Hardware backend control
            that reads the accelerometer
            and returns a value from
            0 to 1 based off the value
            returned from the X axis.
        """
        values = ADXL343.GetAccelerometerValues()
        xAxis = values[0]

        if(xAxis <= 0):
            return 0
        
        normalized = (xAxis / 8)
        return normalized

    @staticmethod
    def GetValue_X_Negative() -> float:
        """
            GetValue_X_Negative:
            ====================
            Summary:
            --------
            Hardware backend control
            that reads the accelerometer
            and returns a value from
            0 to 1 based off the value
            returned from the X axis.
        """
        values = ADXL343.GetAccelerometerValues()
        xAxis = values[0]

        if(xAxis >= 0):
            return 0
        
        normalized = (xAxis / -8)
        return normalized

    @staticmethod
    def GetValue_Y_Positive() -> float:
        """
            GetValue_Y_Positive:
            ====================
            Summary:
            --------
            Hardware backend control
            that reads the accelerometer
            and returns a value from
            0 to 1 based off the value
            returned from the Y axis.
        """
        values = ADXL343.GetAccelerometerValues()
        yAxis = values[1]

        if(yAxis <= 0):
            return 0
        
        normalized = (yAxis / 8)
        return normalized

    @staticmethod
    def GetValue_Y_Negative() -> float:
        """
            GetValue_Y_Negative:
            ====================
            Summary:
            --------
            Hardware backend control
            that reads the accelerometer
            and returns a value from
            0 to 1 based off the value
            returned from the Y axis.
        """
        values = ADXL343.GetAccelerometerValues()
        yAxis = values[1]

        if(yAxis >= 0):
            return 0
        
        normalized = (yAxis / -8)
        return normalized

    @staticmethod
    def GetValue_Z_Positive() -> float:
        """
            GetValue_Z_Positive:
            ====================
            Summary:
            --------
            Hardware backend control
            that reads the accelerometer
            and returns a value from
            0 to 1 based off the value
            returned from the Z axis.
        """
        values = ADXL343.GetAccelerometerValues()
        zAxis = values[2]

        if(zAxis <= 0):
            return 0
        
        normalized = (zAxis / 10)
        return normalized

    @staticmethod  
    def GetValue_Z_Negative() -> float:
        """
            GetValue_Z_Negative:
            ====================
            Summary:
            --------
            Hardware backend control
            that reads the accelerometer
            and returns a value from
            0 to 1 based off the value
            returned from the Z axis.
        """
        values = ADXL343.GetAccelerometerValues()
        zAxis = values[2]

        if(zAxis >= 0):
            return 0
        
        normalized = (zAxis / -10)
        return normalized
#====================================================================#
LoadingLog.End("ADXL343.py")