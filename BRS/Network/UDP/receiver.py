#====================================================================#
# File Information
#====================================================================#
"""
    receiver.py
    ===========
    Summary:
    --------
    This file contains a driver class made to create a thread
    that constantly reads all UDP messages addressed to your
    device from anywhere on the local network. This class is a backend
    class and must not be initialized more than once.

    See :ref:`UDPReader`.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("UDPReader.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import time
import threading
import socket

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
class UDPReader:
    """
        UDPReader:
        ========
        Summary:
        --------
        Class made to create a thread
        that constantly reads all UDP messages addressed to your
        device from anywhere on the local network. This class is a backend
        class and must not be initialized more than once.
    """

    thread = None
    """ private thread object from :ref:`Threading`."""
    stop_event = threading.Event()
    isStarted: bool = False

    listToSend:list = None

    timeoutInSeconds:int = 5
    """
        timeoutInSeconds:
        =================
        Summary:
        --------
        How long in seconds do the UDP function
        get stuck in its receiving method.
        Defaults to 5 seconds.
        Changing this after the thread is started
        will have no effect.
    """

    port:int = 4211
    """
        port:
        =====
        Summary:
        --------
        Holds the port that the UDPReader
        will read from. Changing this
        after starting the thread through
        StartDriver will have no effect.

        Defaults to 4211
    """

    lock = threading.Lock()

    listOfMessageReceived:list = []
    """
        listOfMessageReceived:
        ======================
        Summary:
        --------
        A list of all the received
        messages that were gotten
        in the reading thread.

        While its not adviced to pop
        the first message and discard it
        if its not what we want... eh...
    """

    @staticmethod
    def _reading_thread(udpClass):
        counter = 0

        # Create a UDP socket
        Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of 5 seconds for the socket
        Socket.settimeout(udpClass.timeoutInSeconds)

        # Bind the socket to the IP address and port
        Socket.bind(("0.0.0.0", udpClass.port))

        while True:
            if udpClass.stop_event.is_set():
                break

            try:
                # Receive data and the address of the sender
                try:
                    data, addr = Socket.recvfrom(1024)  # Adjust the buffer size as per your requirements
                except:
                    print("TX ERR")
                with udpClass.lock:
                    udpClass.listOfMessageReceived.append({addr[0]:data})
                    if(len(udpClass.listOfMessageReceived) > 50):
                        udpClass.listOfMessageReceived.pop(0)
            except:
                pass

        # Close the socket
        Socket.close()
        udpClass.isStarted = False

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts the UDP listener / reader
            thread. The UDP socket object
            has a buffer of 1024, reads from
            any addresses but can have the port
            specified to it through a member of
            this class. (:ref:`UDPReader.port`)
        """
        Debug.Start("UDPReader -> StartDriver")
        if UDPReader.isStarted == False:
            if not UDPReader.thread or not UDPReader.thread.is_alive():
                UDPReader.stop_event.clear()
                UDPReader.thread = threading.Thread(target=UDPReader._reading_thread, args=(UDPReader,))
                UDPReader.thread.daemon = True
                UDPReader.thread.start()
                UDPReader.isStarted = True
                Debug.Log("UDPReader is started.")
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Thread is already started. You cannot start more than one.")
            Debug.End()
            return Execution.Failed
        Debug.Log("UDPReader is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the driver from reading anymore
            UDP stuff. DOES NOT CLEAR THE BUFFER
            OF THIS CLASS
        """
        Debug.Start("UDPReader -> StopDriver")
        UDPReader.stop_event.set()
        if UDPReader.thread and UDPReader.thread.is_alive():
            UDPReader.thread.join()
        Debug.Log("Thread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def ClearBuffer():
        """
            ClearBuffer:
            ============
            Summary:
            --------
            Clears the saved message buffer.
        """
        Debug.Start("UDPReader -> ClearBuffer")
        UDPReader.listOfMessageReceived = []
        Debug.End()

    @staticmethod
    def GetOldestMessage(DontDebug=True) -> list:
        """
            GetOldestMessage:
            =================
            Summary:
            --------
            Returns the oldest UDP message
            read by the UDP class.

            Returns:
            --------
            - `None` = No messages or thread not started.
        """
        Debug.Start("GetOldestMessage", DontDebug=True)
        if UDPReader.isStarted:
            with UDPReader.lock:
                Debug.Log("Returning values from the thread")

                if(len(UDPReader.listOfMessageReceived) == 0):
                    Debug.End(ContinueDebug=True)
                    return None

                Debug.End(ContinueDebug=True)
                return UDPReader.listOfMessageReceived.pop(0)
        else:
            Debug.Log("THREAD IS NOT STARTED. NO UDP MESSAGES CAN BE RETURNED")
            Debug.End(ContinueDebug=True)
            return None

    @staticmethod
    def GetNewestMessage() -> list:
        """
            GetNewestMessage:
            =================
            Summary:
            --------
            Returns the newest UDP message
            read by the UDP class.

            Returns:
            --------
            - `None` = No messages or thread not started.
        """
        Debug.Start("GetNewestMessage")
        if UDPReader.isStarted:
            with UDPReader.lock:
                Debug.Log("Returning values from the thread")

                if(len(UDPReader.listOfMessageReceived) == 0):
                    Debug.End()
                    return None

                Debug.End()
                return UDPReader.listOfMessageReceived.pop(-1)
        else:
            Debug.Log("THREAD IS NOT STARTED. NO UDP MESSAGES CAN BE RETURNED")
            Debug.End()
            return None

    @staticmethod
    def SetNewPeriodicSender(listOfIntsToSend:list) -> list:
        """
            SetNewPeriodicSender:
            =====================
            Summary:
            --------
            Sends some bytes each time
            we loop in this 10 times.

            Returns:
            --------
            - `None` = No messages or thread not started.
        """
        Debug.Start("SetNewPeriodicSender")
        if UDPReader.isStarted:
            with UDPReader.lock:
                Debug.Log("Returning values from the thread")

                UDPReader.listToSend = listOfIntsToSend.copy()

                Debug.End()
                return Execution.Passed
        else:
            Debug.Log("THREAD IS NOT STARTED. NO UDP MESSAGES CAN BE SENT")
            Debug.End()
            return None

#====================================================================#
LoadingLog.End("UDPReader.py")