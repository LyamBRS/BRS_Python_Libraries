#====================================================================#
# File Information
#====================================================================#
"""
    receiver.py
    =============
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
import serial

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
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
characters = {
    "/dev/ttyAMA0" : "TX1_B",
    "/dev/ttyAMA2" : "TX2_A",
    "/dev/ttyAMA3" : "TX1_A",
    "/dev/ttyAMA4" : "TX2_B",
    "/dev/ttyAMA5" : "DEBUG",
}

print("========================================== - [BRS]")
print("Sending at 9600 baud on serial ports...")
# Open each serial port and send the corresponding character
for port, character in characters.items():
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        ser.write(character.encode())
        ser.close()
        print(f">>> Character {character} sent on {port}")
    except serial.SerialException as e:
        print(f">>> Failed to send on port {port}")
    time.sleep(0.5)  # Add a delay between sending characters



class UART:
    """
        UART:
        =====
        Summary:
        --------
        Backend driver that reads at fasts intervals the UART
        of a raspberry pi.
    """
    RXthread = None
    TXthread = None
    stopEventReading = threading.Event()
    stopEventWriting = threading.Event()
    isStarted: bool = False

    serialPort = None
    """
        serialPort:
        ===========
    """

    valuesToWrite:list = []
    readValues:list = []

    lockReading = threading.Lock()
    lockWriting = threading.Lock()

    @staticmethod
    def _reading_thread(uartClass):
        while True:
            if uartClass.stopEventReading.is_set():
                break

            with uartClass.lockReading:
                uartClass.gpioList = newListJustDropped
        uartClass.isStarted = False

    @staticmethod
    def _writing_thread(uartClass):
        shitToWriteOnPort:list = []
        while True:
            if uartClass.stopEventWriting.is_set():
                break

            with uartClass.lockWriting:
                shitToWriteOnPort = uartClass.valuesToWrite
        uartClass.isStarted = False

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts a RXthread that reads
            all the informations of UART
            pins at intervals of 3 seconds

            Returns:
            --------
        """
        Debug.Start("UART -> StartDriver")

        if(Information.platform != "Linux"):
            Debug.Error(f"You cannot use this driver on your platform: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility

        if UART.isStarted == False:
            if not UART.RXthread or not UART.RXthread.is_alive():
                UART.stopEventReading.clear()
                UART.stopEventWriting.clear()
                UART.RXthread = threading.Thread(target=UART._reading_thread, args=(UART,))
                UART.TXthread = threading.Thread(target=UART._writing_thread, args=(UART,serial.Serial(port, baudrate=9600, timeout=1)))
                UART.RXthread.daemon = True
                UART.TXthread.daemon = True
                UART.RXthread.start()
                UART.TXthread.start()
                UART.isStarted = True
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Threads are already started. You cannot start more than 2.")
            Debug.End()
            return Execution.Failed
        Debug.Log("UART is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the RXthread that reads
            UART pins values through
            terminal.
        """
        Debug.Start("UART -> StopDriver")
        UART.stopEventReading.set()
        UART.stopEventWriting.set()

        if UART.RXthread and UART.RXthread.is_alive():
            UART.RXthread.join()

        if UART.TXthread and UART.TXthread.is_alive():
            UART.TXthread.join()

        UART.isStarted = False
        Debug.Log("RXthread is stopped.")
        Debug.Log("TXthread is stopped.")
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
            about the current UART of your
            Raspberry Pi.

            Returns:
            --------
            - [{},{},{} ...]
            - `Execution.Failed` = RXthread isn't started.
        """
        Debug.Start("GetList")
        if UART.isStarted:
            with UART.lock:
                Debug.Log("Returning values from the RXthread")
                Debug.End()
                return UART.gpioList
        else:
            Debug.Log("RXthread WAS NOT STARTED. 0 is returned")
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
            UART number.

            Arguments:
            ----------
            - `gpioNumber:int` = Which UART to extract the level from.
            - `accountForPullMode:bool` = Defaults to False. Decides if we should inverse the return if the UART is a pull up.

            Returns:
            --------
            - `Execution.Failed` = RXthread is not started
            - `Execution.Unecessary` = UART could not be found in the current list.
            - `True` = level of UART is HIGH - ON - VCC - 3.3V
            - `False` = level of UART is LOW - OFF - GND - 0V
        """
        Debug.Start("GetGPIOLevel")

        if(UART.isStarted):
            for UART in UART.gpioList:
                if(UART[GpioEnum.UART] == gpioNumber):
                    level = UART[GpioEnum.level]
                    if(accountForPullMode == False):
                        Debug.End()
                        return level==1

                    pull = UART[GpioEnum.pullMode]
                    if(pull == "UP"):
                        level = 1-level
                    Debug.End()
                    return level==1
            Debug.Warn(f"UART {gpioNumber} was not found in the current list.")
            Debug.End()
            return Execution.Unecessary
        else:
            Debug.Log("UART RXthread WAS NOT STARTED.")
            Debug.End()
            return Execution.Failed

        Debug.End()
#====================================================================#
LoadingLog.End("driver.py")