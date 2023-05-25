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

    serialPort:str = None
    """
        serialPort:
        ===========
        summary:
        --------
        The name of the serial port you want to use.
        Defaults to NONE so be careful.
    """

    serialPortObject = None

    maxGroupsSlots = 10
    """
        Defines how many groups of
        arrived passengers you can store
        in your BFIO class. Defaults to 10.
        After which, no more groups are stored.
        They are ignored.
    """

    planesToWrite:list = []
    groupsOfArrivedPassengers:list = []

    lockReading = threading.Lock()
    lockWriting = threading.Lock()

    @staticmethod
    def _reading_thread(uartClass):
        from ...Utilities.bfio import BFIO, NewArrival, PassengerTypes, MandatoryPlaneIDs

        def GetPassengerArrivals() -> list:
            """
                Only reads passengers that arrived.
                returns them in groupes of 2.
            """
            # Clear the buffer of any passengers.
            newArrivals = []
            while uartClass.serialPortObject.in_waiting >= 2:
                try:
                    data = uartClass.serialPortObject.read(2)
                    # print(f"{data[0]}, {data[1]}")
                    if(data[0] > 3):
                        print("Fuck up detected. Offsetting by 1 value.")
                        uartClass.serialPortObject.read(1)
                except:
                    print(f"Timed out when trying to read bytes.")
                passengerList = BFIO.GetPassengersFromDualBytes(data)
                
                for passenger in passengerList:
                    if(passenger.passedTSA):
                        newArrivals.append(passenger)
                    else:
                        print(f">>> {passenger.initErrorMessage} ")
            
            return newArrivals
        ################################################
        ################################################
        class stupidPython:
            receivingPlane:bool = False
            receivedPassengers:list = []
        
        def HandleNewArrivals() -> NewArrival:
            """
                Appends passengers to a list.
                Only starts doing so when it saw
                a pilot in the new arrivals.
                Stops when a co-pilot is seen.
            """
            arrivedPassengers = []
            # Get passengers that arrived.
            newArrivals = GetPassengerArrivals()
            # print(f"Concatenating arrivals to a list of {len(stupidPython.receivedPassengers)}")
            for arrival in newArrivals:
                
                if(not stupidPython.receivingPlane):
                    if(arrival.type == PassengerTypes.Pilot):
                        print("Pilot received.")
                        stupidPython.receivingPlane = True
                        stupidPython.receivedPassengers.clear()
                        stupidPython.receivedPassengers.append(arrival)
                else:
                    print(f"Adding passengers to a list of {len(stupidPython.receivedPassengers)}")
                    if(arrival.type == PassengerTypes.CoPilot):
                        # The rear of a plane was received
                        stupidPython.receivingPlane = False
                        print("Co-Pilot received")
        
                    stupidPython.receivedPassengers.append(arrival)
                    if(stupidPython.receivingPlane == False):
                        print("Passengers grouped into plane.")
                        arrivedPassengers.append(stupidPython.receivedPassengers.copy())
            return arrivedPassengers
        ################################################
        while True:
            if uartClass.stopEventReading.is_set():
                break

            arrivedGroupsOfPassengers = HandleNewArrivals()

            with uartClass.lockReading:
                if(len(arrivedGroupsOfPassengers) > 0):
                    for group in arrivedGroupsOfPassengers:
                        if(len(uartClass.groupsOfArrivedPassengers) < uartClass.maxGroupsSlots):
                            uartClass.groupsOfArrivedPassengers.append(group)
        ################################################
        uartClass.isStarted = False

    @staticmethod
    def _writing_thread(uartClass):
        from ...Utilities.bfio import Plane, Passenger
        planesReadyForTakeOff:list = []

        while True:
            if uartClass.stopEventWriting.is_set():
                break

            if(planesReadyForTakeOff != None):
                if(len(planesReadyForTakeOff) > 0):
                    # plane:Plane
                    for plane in planesReadyForTakeOff:
                        # passenger:Passenger
                        for passenger in plane.passengers:
                            uartClass.serialPortObject.write(passenger.value_8bits[0])
                            uartClass.serialPortObject.write(passenger.value_8bits[1])

            planesReadyForTakeOff.clear()
            with uartClass.lockWriting:
                planesReadyForTakeOff = uartClass.planesToWrite
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
                UART.serialPortObject = serial.Serial(UART.serialPort, baudrate=9600, timeout=0.05)
                UART.RXthread = threading.Thread(target=UART._reading_thread, args=(UART,))
                UART.TXthread = threading.Thread(target=UART._writing_thread, args=(UART,))
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
        
        Debug.Log("Stopping Serial Port Object.")
        UART.serialPortObject.close()
        Debug.Log("Success.")

        UART.isStarted = False
        Debug.Log("RXthread is stopped.")
        Debug.Log("TXthread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def GetReceivedPlanes() -> list:
        """
            GetReceivedPlanes:
            ==================
            Summary:
            --------
            Updates the received plane list. 

            Returns:
            --------
            - [{},{},{} ...]
            - `Execution.Failed` = RXthread isn't started.
        """
        Debug.Start("GetList")
        if UART.isStarted:
            with UART.lockReading:
                Debug.Log("Returning values from the RXthread")
                Debug.End()
                return UART.groupsOfArrivedPassengers
        else:
            Debug.Log("RXthread WAS NOT STARTED. Execution.Failed is returned")
            Debug.End()
            return Execution.Failed
        
    def QueuePlaneOnTaxiway(planeToTakeOff) -> Execution:
        """
            QueuePlaneOnTaxiway:
            ====================
            Summary:
            --------
            Puts a plane to be sent on Serial.

            Returns:
            --------
            - [{},{},{} ...]
            - `Execution.Failed` = RXthread isn't started.
        """
        Debug.Start("QueuePlaneOnTaxiway")
        if UART.isStarted:
            with UART.lockWriting:
                UART.planesToWrite.append(planeToTakeOff)
                Debug.End()
                return Execution.Passed
        else:
            Debug.Log("TXthread WAS NOT STARTED. Execution.Failed is returned")
            Debug.End()
            return Execution.Failed

    @staticmethod
    def GetOldestReceivedGroupOfPassengers() -> list:
        """
            GetOldestReceivedGroupOfPassengers:
            ===================================
            Summary:
            --------
            Method that returns the oldest received
            group of passengers. it also removes
            it from the list of saved groups of passengers

        """
        Debug.Start("GetOldestReceivedGroupOfPassengers")

        if(UART.isStarted):
            
            try:
                UART.GetReceivedPlanes()
                OldestGroupOfPassengers = UART.groupsOfArrivedPassengers.pop(0)
            except:
                Debug.Warn("No groups of passengers to return.")
                Debug.End()
                return None

            Debug.Log(f"Returning a group of passengers")
            Debug.End()
            return OldestGroupOfPassengers
        else:
            Debug.Log("UART RXthread WAS NOT STARTED.")
            Debug.End()
            return Execution.Failed
#====================================================================#
LoadingLog.End("driver.py")