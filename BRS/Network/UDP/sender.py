#====================================================================#
# File Information
#====================================================================#
"""
    sender.py
    ===========
    Summary:
    --------
    This file contains a driver class made to create a thread
    that writes on a specified UDP socket. This class is static
    as of now and therefor cannot be used more than once in your
    application.

    See :ref:`UDPSender`.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("sender.py")
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
class UDPSender:
    """
        UDPSender:
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

    _thingToSend = None

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

    ipAddress:str = "198.162.4.2"
    """
        ipAddress:
        ==========
        Summary:
        --------
        The IP address where this class will
        be sending packets. Defaults to
        `"198.162.4.2"`
    """

    port:int = 4210
    """
        port:
        =====
        Summary:
        --------
        Holds the port that the UDPSender
        will read from. Changing this
        after starting the thread through
        StartDriver will have no effect.

        Defaults to 4210
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
    def _Thread(udpClass):
        counter = 0

        # Create a UDP socket
        Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout of 5 seconds for the socket
        Socket.settimeout(udpClass.timeoutInSeconds)

        # Bind the socket to the IP address and port
        Socket.bind((udpClass.ipAddress, udpClass.port))

        thingToSend = None
        while True:
            if udpClass.stop_event.is_set():
                break

            try:
                # Receive data and the address of the sender

                if(thingToSend != None):
                    if(type(thingToSend) != bytes):
                        bytesToSend = bytes(thingToSend)
                    else:
                        bytesToSend = thingToSend

                    Socket.sendto(bytesToSend, (udpClass.ipAddress, udpClass.port))
                    thingToSend = None

                with udpClass.lock:
                    thingToSend = udpClass._thingToSend
                    udpClass._thingToSend = None
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
            Starts the UDP sender
            thread. The UDP socket object
            has a buffer of 1024, writes to a
            specific addresses.
        """
        Debug.Start("UDPSender -> StartDriver")
        if UDPSender.isStarted == False:
            if not UDPSender.thread or not UDPSender.thread.is_alive():
                UDPSender.stop_event.clear()
                UDPSender.thread = threading.Thread(target=UDPSender._Thread, args=(UDPSender,))
                UDPSender.thread.daemon = True
                UDPSender.thread.start()
                UDPSender.isStarted = True
                Debug.Log("UDPSender is started.")
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Thread is already started. You cannot start more than one.")
            Debug.End()
            return Execution.Failed
        Debug.Log("UDPSender is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the driver from sending anymore
            UDP stuff. DOES NOT CLEAR THE BUFFER
            OF THIS CLASS
        """
        Debug.Start("UDPSender -> StopDriver")
        UDPSender.stop_event.set()
        if UDPSender.thread and UDPSender.thread.is_alive():
            UDPSender.thread.join()
        Debug.Log("Thread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def SendThing(thingToSend) -> Execution:
        """
            SendThing:
            ==========
            Summary:
            --------
            Sets what to send on the UDP.
            It will be set back to `None` once
            its sent.
        """
        Debug.Start("SendThing")

        if(UDPSender.isStarted):
            with UDPSender.lock:
                UDPSender._thingToSend = thingToSend
            Debug.Log("New thing to send has been specified.")
        else:
            Debug.Log("THREAD IS NOT STARTED. NO UDP MESSAGES CAN BE RETURNED")
            Debug.End()
            return Execution.Failed

        Debug.End()
#====================================================================#
LoadingLog.End("sender.py")