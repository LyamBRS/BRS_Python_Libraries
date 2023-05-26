#====================================================================#
# File Information
#====================================================================#
"""
    bfio.py
    =======
    This file is used to handle BFIO communications conversions.
    It does not handle the actual communication but is used to
    create planes to depart and unload passengers from arrived
    planes.

    This file also contains base classes for airports, terminals,
    runways and gates.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from typing import Any
from ...BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("bfio.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import struct
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ..Debug.consoleLog import Debug
from .Enums import Execution, VarTypes
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#
def pack_string(string):
    encoded_string = string.encode('utf-8')  # Encode string to bytes
    length = len(encoded_string)
    packed_data = struct.pack(f'{length}s', encoded_string)
    return packed_data

def unpack_string(packed_data):
    length = len(packed_data)
    unpacked_data = struct.unpack(f'{length}s', packed_data)
    decoded_string = unpacked_data[0].decode('utf-8')  # Decode bytes to string
    return decoded_string

class MandatoryPlaneIDs:
    """
        MandatoryPlaneIDs:
        ==================
        Summary:
        --------
        A class containing 
        members that represents
        each mandatory BFIO function
        IDs. Your device should use
        this when identifying arrived
        pilots.
    """
    ping:int = 0
    status:int = 1
    handshake:int = 2
    errorMessage:int = 3
    deviceType:int = 4
    uniqueID:int = 5
    restartProtocol:int = 6
    universalInfo:int = 7
    communicationError:int = 8

MandatoryFunctionRequestVarTypeLists = {
    MandatoryPlaneIDs.ping               : [VarTypes.Bool],
    MandatoryPlaneIDs.status             : [VarTypes.Unsigned.Char],
    MandatoryPlaneIDs.handshake          : [],
    MandatoryPlaneIDs.errorMessage       : [VarTypes.String],
    MandatoryPlaneIDs.deviceType         : [VarTypes.Unsigned.Char],
    MandatoryPlaneIDs.uniqueID           : [VarTypes.Unsigned.LongLong],
    MandatoryPlaneIDs.restartProtocol    : [],
    MandatoryPlaneIDs.universalInfo      : [VarTypes.Unsigned.LongLong, VarTypes.Unsigned.LongLong, VarTypes.Unsigned.Char, VarTypes.Unsigned.Char, VarTypes.String, VarTypes.String, VarTypes.String],
    MandatoryPlaneIDs.communicationError : []
}
"""
    MandatoryFunctionRequestVarTypeLists:
    =====================================
    Summary:
    --------
    A dictionary of lists that represents
    the var types lists passed to plane
    object builders when a mandatory
    plane is received.

    If you receive a PING pilot for example,
    you'll take the list of passengers of that
    plane and build a :ref:`NewArrival` by giving
    it the received passengers objects and the
    list of vartypes associated with Ping.
"""

class PassengerTypes:
    """
        PassengerTypes:
        ===============
        Summary:
        --------
        Class containing the possible passenger types.
    """
    Start:int = 512
    Byte:int = 0
    Div:int = 256
    Check:int = 768

    Pilot:int = 512
    Passenger:int = 0
    Attendant:int = 256
    CoPilot:int = 768
#====================================================================#
# Classes
#====================================================================#
class BFIO:
    #region   --------------------------- DOCSTRING
    """
        BFIO:
        =====
        Summary:
        --------
        This class handles boarding of passengers,
        debarkation of passengers, TSA approvals and
        some more BFIO utilities.
    """
    #endregion
    #region   --------------------------- MEMBERS
    class UDP:
        """
            BFIO: UDP
            ==========
            Summary:
            ---------
            This class holds references used
            when BFIO is used through an UDP
            protocol.
        """
        portToSendToAccessPoint:int = 4210
        portToReceiveFromAccessPoint:int = 4211

    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
    # ------------------------------------
    def GetPassengersFromDualBytes(listOfBytes:bytes) -> list:
        """
            GetPassengersFromDualBytes:
            ===========================
            Summary:
            --------
            This function's purpose is to
            convert receivd bytes (0-255)
            to a list of :ref:`Passengers` objects.

            This function is to be used in
            communication protocols that only
            works with bytes and can't work with
            series of 10 bits values.

            The orders of your ints must be:
            - [identifiant, value, identifiant, value ...]
        """
        val = struct.unpack('B' * len(listOfBytes), listOfBytes)
        listOfInts = list(val)

        passengers:list = []

        for index in range(0, len(listOfInts), 2):
            typeOfPassenger = listOfInts[index]
            luggage = listOfInts[index + 1] if index + 1 < len(listOfInts) else None

            typeOfPassenger = typeOfPassenger << 8
            passenger = Passenger(typeOfPassenger, luggage)

            passengers.append(passenger)
        
        return passengers
    # ------------------------------------
    def BuildAndBoardPlane() -> list:
        """
            BuildAndBoardPlane:
            ===================
            Summary:
            --------
            This function's purpose is to build
            a custom plane based on the amount
            of given passengers and a given plane
            ID.
        """
        pass
    # ------------------------------------
    def GetPlanesTSAReport(plane:list) -> Execution:
        """
            GetPlanesTSAReport:
            ===================
            Summary:
            --------
            Function that returns a dictionary
            of information based on the plane
            given to the function.

            Attention:
            ----------
            It is imperative that you verify the
            `passed-tsa` parameter of the dictionary
            before you do anything with it.
        """
        pass
    # ------------------------------------
    def IsPassengerGroupAMandatoryPlane(passengers:list):
        """
            IsPassengerGroupAMandatoryPlane:
            ================================
            Summary:
            --------
            Function that tells you if the group
            of passengers ya got is a mandatory function
            typed plane. Returns `True` and `False` if not.
        """
        Debug.Start("IsPassengerGroupAMandatoryPlane")
        
        pilot = passengers[0]
        PrintPassenger(pilot)

        if(passengers[0].value_8bits[1] < 10):
            Debug.Log("That group is made for mandatory functions")
            Debug.End()
            return True
        else:
            Debug.Log("That group is not a mandatory functions")
            Debug.End()
            return False
    # ------------------------------------
    def ParsePassengersIntoMandatoryPlane(passengers:list):
        """
            ParsePassengersIntoMandatoryPlane:
            ==================================
            Summary:
            --------
            Takes a list of passengers object
            and attempts to build them into a
            :ref:`NewArrival` object based on mandatory
            functions.
        """
        Debug.Start("ParsePassengersIntoMandatoryPlane")
        pilot = passengers[0]
        callsign = pilot.value_8bits[1]
        MandatoryPlane = NewArrival(passengers, MandatoryFunctionRequestVarTypeLists[callsign])

        Debug.End()
        return MandatoryPlane
    #endregion
    #region   ------------------- Private
    def _CheckPlaneID(planeID:int) -> Execution:
        """
            _CheckPlaneID:
            ==============
            Summary:
            --------
            Checks if a plane ID is within
            allowed ranges of 0 to 255.
        """
        Debug.Start("_CheckPlaneID")
        if(planeID < 0 or planeID > 255):
            Debug.Error(f"Plane ID cannot be {planeID}. 0-255 max.")
            Debug.End()
            return Execution.Failed
        Debug.End()
        return Execution.Passed
    # ------------------------------------
    def _GetPlaneChecklist(passengers:list) -> int:
        """
            _GetPlaneChecklist:
            =========================
            Summary:
            --------
            Returns the plane's expected
            checklist. A checklist is 
            a checksum really...

            Arguments:
            ----------
            - `Passengers` : How many passengers are in the plane 
        """
        countedData = 0

        Debug.Start("_GetPlaneChecklist")
        for seatNumber in range(len(passengers)):
            passenger:Passenger = passengers[seatNumber]

            if(passenger.type == PassengerTypes.Check):
                Debug.Log("We finished going through each seat.")
                Debug.Log("Unless the copilot is stupid and seated himself with the passengers.")
                Debug.End()
                return countedData

            countedData = (countedData + passenger.value_8bits[1]) % 256
        Debug.Log(f"Counted passenger data resulted in {countedData}.")
        Debug.End()
        return countedData
    # ------------------------------------
    def _VerifyPassengersChecksum(passengers:list) -> Execution:
        """
            _VerifyPassengersChecksum:
            =========================
            Summary:
            --------
            Private method that confirms
            if a given plane's checksum
            checks out with what we
            counted.
        """
        Debug.Start("_VerifyPassengersChecksum")
        passengerCount = len(passengers)
        copilot = passengers[passengerCount-1]
        if(copilot.type != PassengerTypes.CoPilot):
            Debug.Error("Last passenger is not a copilot.")
            Debug.End()
            return Execution.Failed

        copilotsCheckList = copilot.value_8bits[1]
        calculatedCheckList = BFIO._GetPlaneChecklist(passengers)

        if(copilotsCheckList != calculatedCheckList):
            Debug.Error(f"The copilot's checklist: {copilotsCheckList} did not match the calculated checklist: {calculatedCheckList}")
            Debug.End()
            return Execution.Failed

        Debug.End()
        return Execution.Passed
    # ------------------------------------
    def _GetPlaneID(plane:list) -> Execution:
        """
            _GetPlaneID:
            ============
            Summary:
            --------
            Returns a plane ID from
            a complete given plane.
            Returns an Execution error
            if the ID is either not found
            or isnt right.
        """
        pass
    # ------------------------------------
    def _GetPassengerClassCount(plane:list) -> Execution:
        """
            _GetPassengerClassCount:
            ========================
            Summary:
            --------
            Counts how many classes of passengers
            there is. A class of passenger is
            basically a parameter that the plane
            was transporting.
        """
        pass
    # ------------------------------------
    def _GetPassengersFromVariable(variable, varType:str, typeOfPassenger) -> list:
        """

        """
        pass
    # ------------------------------------
    def _GetClassesFromPassengers(passengers:list, varTypes:list) -> list:
        """
            _GetClassesFromPassengers:
            ==========================
            Summary:
            --------
            This method's purpose is to
            return a list of passengerClass
            objects that represents the
            objects within a class.

            Returns:
            --------
            - `Execution.Unecessary` = Plane doesnt have passengers
            - `Execution.Failed` = Plane doesn't make any sense
            - `list` a list of :ref:`PassengerClass`
        """
        Debug.Start("_GetClassesFromPassengers")

        def divide_passenger_list(passenger_list):
            sublists = []
            sublist_start = 0

            for i in range(1, len(passenger_list)):
                if passenger_list[i].type == PassengerTypes.Attendant and passenger_list[i - 1].type == PassengerTypes.Passenger:
                    sublist = passenger_list[sublist_start:i]
                    sublists.append(sublist)
                    sublist_start = i

            # Append the last sublist from the last 1 encountered to the end of the list
            last_sublist = passenger_list[sublist_start:]
            sublists.append(last_sublist)

            return sublists

        passengers.pop(0)  # Remove pilot
        passengers.pop(-1)  # Remove copilot

        secondPassenger:Passenger = passengers[0]
        if(secondPassenger.type != PassengerTypes.Attendant):
            Debug.Warn("Second passenger is not an attendant.")
            if(secondPassenger.type == PassengerTypes.CoPilot):
                Debug.Warn(f"No passenger classes in this plane")
                Debug.End()
                return Execution.Unecessary
            Debug.Error(f"THIS PLANE IS WRONG AF DAWG")
            Debug.End()
            return Execution.Failed

        dividedPassengers = divide_passenger_list(passengers)

        ListOfClasses = []
        amountOfClasses = len(dividedPassengers)
        for classNumber in range(amountOfClasses):

            if(classNumber > len(varTypes)-1):
                Debug.Error("Too many classes compared to var types")
                Debug.End()
                return Execution.Failed

            Debug.Log(f"Converting to type {varTypes[classNumber]}")
            ListOfClasses.append(ArrivalPassengerClass(dividedPassengers[classNumber], varTypes[classNumber]))

        Debug.End()
        return ListOfClasses
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
class Plane:
    #region   --------------------------- DOCSTRING
    """
        Plane:
        ======
        Summary:
        --------
        A class that is built from the data
        received from a plane.
    """
    #endregion
    #region   --------------------------- MEMBERS
    planeID:int = None
    """
        planeID:
        ========
        Summary:
        --------
        The ID retreived from a plane.
        ID ranges from 0 to 255 and depends
        on the other device's airport and gates.
        Defaults to `None`
    """

    amountOfClasses:int = None
    """
        amountOfClasses:
        ==========================
        Summary:
        --------
        Says how many classes of regular passengers
        there is in your plane or the plane analyzed.
        A class is basically a function parameter.
    """

    classesSizes:list = None
    """
        classesSizes:
        =============
        Summary:
        --------
        list of integers that tells you
        how many passengers in each classes
        there is in that plane.
        The list is a list of `int` and
        is of size :ref:`amountOfClasses`
    """

    passedTSA:bool = None
    """
        passedTSA:
        ==========
        Summary:
        --------
        boolean variable that is set
        to `True` if the plane managed
        to get verified fully and passed
        through TSA. Otherwise, if
        problems are detected, its set to
        `False`. Defaults to `None`.
    """

    classes:list = None
    """
        classes:
        ==========
        Summary:
        --------
        This member holds all PassengerClass objects
        of this plane.
        Used to decode each classes of passengers
        individually after the class is initialized.
    """

    passengers:list = None
    """
        list of Passenger objects consisting of
        the entire plane.
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
    #endregion
    #region   ------------------- Private
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, planeID:int, variables:list, wantedClasses:list):
        """
            Plane:
            ======
            Summary:
            --------
            This constructor builds a plane from
            a planeID and a given list of variables.

            Arguments:
            ----------
            - `planeID`:  ID that the plane should have. 0-255
            - `variables`:  a list of variables to make passengers from. Must be same size as :ref:`wantedClasses`
            - `wantedClasses`: a list of VariableType associated with the list of passengers
        """
        Debug.Start("Plane -> Building and Boarding.")

        self.classes = []
        self.classesSizes = []
        self.passengers = []

        tsaResult = BFIO._CheckPlaneID(planeID)
        if(tsaResult != Execution.Passed):
            Debug.Error(f"You cannot build a plane with an ID of {planeID}")
            Debug.End()
            return Execution.Failed
        self.passedTSA = tsaResult

        if(len(variables) != len(wantedClasses)):
            Debug.Error("There is more or less variables or classes. They must be the same length bruh.")
            Debug.End()
            return Execution.Failed

        self.amountOfClasses = len(wantedClasses)

        for currentClassNumber in range(len(variables)):
            variableToConvert = variables[currentClassNumber]
            typeToConvertItTo = wantedClasses[currentClassNumber]

            boardedPassengerClass = PassengerClass(variableToConvert, typeToConvertItTo)
            if(boardedPassengerClass == None):
                Debug.Error("Failed to board passengers for the specified type.")
                Debug.End()
                return Execution.Failed

            self.classes.append(boardedPassengerClass)

            for passenger in boardedPassengerClass.passengers:
                self.passengers.append(passenger)

            del boardedPassengerClass

        Debug.Log(f"All passengers are aboard the plane")

        Debug.Log("The pilot is boarding the plane")
        planePilot = Passenger(PassengerTypes.Start, planeID)
        self.passengers.insert(0, planePilot)

        Debug.Log("The co-pilot is doing checklist")
        checklistResult = BFIO._GetPlaneChecklist(self.passengers)
        coPilot = Passenger(PassengerTypes.Check, checklistResult)

        self.passengers.append(coPilot)
        Debug.Log("All passengers are in the plane! Ready for 9/11")
        self.passedTSA = True
        Debug.End()
    #endregion
    pass
#====================================================================#
class NewArrival:
    #region   --------------------------- DOCSTRING
    """
        NewArrival:
        ===========
        Summary:
        --------
        Builds a plane with a different name.
        This class builds a plane from arrived
        passengers basically.
    """
    #endregion
    #region   --------------------------- MEMBERS
    planeID:int = None
    """
        planeID:
        ========
        Summary:
        --------
        The ID retreived from a plane.
        ID ranges from 0 to 255 and depends
        on the other device's airport and gates.
        Defaults to `None`
    """

    amountOfClasses:int = None
    """
        amountOfClasses:
        ==========================
        Summary:
        --------
        Says how many classes of regular passengers
        there is in your plane or the plane analyzed.
        A class is basically a function parameter.
    """

    classesSizes:list = None
    """
        classesSizes:
        =============
        Summary:
        --------
        list of integers that tells you
        how many passengers in each classes
        there is in that plane.
        The list is a list of `int` and
        is of size :ref:`amountOfClasses`
    """

    passedTSA:bool = None
    """
        passedTSA:
        ==========
        Summary:
        --------
        boolean variable that is set
        to `True` if the plane managed
        to get verified fully and passed
        through TSA. Otherwise, if
        problems are detected, its set to
        `False`. Defaults to `None`.
    """

    classes:list = None
    """
        classes:
        ==========
        Summary:
        --------
        This member holds all PassengerClass objects
        of this plane.
        Used to decode each classes of passengers
        individually after the class is initialized.
    """

    passengers:list = None
    """
        list of Passenger objects consisting of
        the entire plane.
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
    def GetParameter(self, parameterNumber:int):
        """
            GetParameter:
            =============
            Summary:
            --------
            Extracts a parameter from this plane.
        """
        Debug.Start("NewArrival -> GetParameter")
        if(not self.passedTSA):
            Debug.Error("CANNOT EXTRACT PARAMETERS FROM SELF CUZ WE DIDN'T PASS TSA.")
            Debug.End()
            return Execution.Failed

        if(parameterNumber > len(self.classes)-1):
            Debug.Error(f"Parameter is out of bound. This plane only has {len(self.classes)} parameters")
            Debug.End()
            return Execution.Incompatibility

        passengerClass:ArrivalPassengerClass
        passengerClass = self.classes[parameterNumber]
        if(not passengerClass.passedTSA):
            Debug.Error(f"Parameter is corrupted.")
            Debug.End()
            return Execution.Failed

        Debug.Log(f">>> Success. Returning: {passengerClass.originalVariable}")
        Debug.End()
        return passengerClass.originalVariable


    #endregion
    #region   ------------------- Private
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR

    def __init__(self, passengers:list, wantedClasses:list):
        """
            Plane:
            ======
            Summary:
            --------
            This constructor builds a new arrival
            from a list of passengers and a list of
            expected classes.

            Arguments:
            ----------
            - `passengers`:  list of :ref:`Passenger` objects
            - `wantedClasses`: a list of VariableType associated with the list of passengers
        """
        Debug.Start("Plane -> Analyzing Arrival.")
        self.classes = []
        self.classesSizes = []
        self.passengers = []

        self.passengers = passengers
        passengerCount = len(passengers)

        pilot:Passenger = passengers[0]
        if(pilot.type != PassengerTypes.Pilot):
            Debug.Error(f"The first passenger of this plane is not a pilot!")
            self.passedTSA = False
            Debug.End()
            return

        copilot:Passenger = passengers[passengerCount-1]
        if(copilot.type != PassengerTypes.CoPilot):
            Debug.Error(f"The last passenger of this plane is not a copilot!")
            self.passedTSA = False
            Debug.End()
            return

        result = BFIO._VerifyPassengersChecksum(passengers)
        if(result != Execution.Passed):
            Debug.Error(f"_VerifyPassengersChecksum returned code: {result}")
            self.passedTSA = False
            Debug.End()
            return

        planeCallsign = pilot.value_8bits[1]
        self.planeID = planeCallsign
        Debug.Log(f"Plane's call sign is {self.planeID} and carries {passengerCount} passengers.")

        classes = BFIO._GetClassesFromPassengers(passengers, wantedClasses)
        if(classes == Execution.Failed):
            Debug.Error("One or more classes failed conversion.")
            self.passedTSA = False
            Debug.End()
            return
        if(classes == Execution.Crashed):
            Debug.Error("One or more classes crashed.")
            self.passedTSA = False
            Debug.End()
            return

        self.classes = classes
        self.amountOfClasses = len(self.classes)
        self.passedTSA = True
        Debug.End()
    #endregion
    pass
#====================================================================#
class Passenger:
    #region   --------------------------- DOCSTRING
    """
        Passenger:
        ==========
        Summary:
        --------
        An object of a passenger
    """
    #endregion
    #region   --------------------------- MEMBERS
    value_10bits:int
    """
        The regular 10 bits BFIO protocol
        value.
    """
    value_8bits:list
    """
        A list of 2 bytes representing
        the BFIO data in a byte protocol
        format.

        - [0] : type
        - [1] : 8 bits data
    """
    type:int
    """
        Compare with memebers of 
        :ref:`PassengersType` 
    """
    passedTSA:bool = None
    """
        passedTSA:
        ==========
        Summary:
        --------
        tells you if your passenger is a valid working
        member of society and can be used when you build
        your plane. If this isn't `True` after you build
        a Passenger object... discard it, its a terrorist!
    """
    initErrorMessage:str = None
    """
        initErrorMessage:
        =================
        Summary:
        --------
        The error message generated
        when a Passenger class built
        wasn't right. This is paired with
        :ref:`passedTSA`
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
    #endregion
    #region   ------------------- Private
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, type:int, byte:int):
        """
            Plane:
            ======
            Summary:
            --------
            This constructor builds a plane from
            a planeID and a given list of variables.
        """
        Debug.Start("Passenger -> Building", DontDebug=True)

        self.type = None
        self.value_10bits = None
        self.value_8bits = []

        if(byte < 0 or byte > 255):
            Debug.Error(f"FATAL PASSENGER ERROR. Passenger cant hold bytes of {byte}")
            self.initErrorMessage = f"FATAL PASSENGER ERROR. Passenger cant hold bytes of {byte}"
            self.passedTSA = False
            Debug.End()
            return

        if(type != PassengerTypes.Byte and type != PassengerTypes.Check and type != PassengerTypes.Div and type != PassengerTypes.Start):
            Debug.Error(f"Passenger's specified type; {type} isn't valid.")
            self.initErrorMessage = f"Passenger's specified type; {type} isn't valid."
            self.passedTSA = False
            Debug.End()
            return

        self.value_10bits = byte + type
        self.value_8bits = [type >> 8, byte]
        self.type = type

        # PrintPassenger(self)
        self.initErrorMessage = ""
        self.passedTSA = True

        Debug.End(ContinueDebug=True)
    #endregion
    pass
#====================================================================#
class PassengerClass:
    #region   --------------------------- DOCSTRING
    """
        PassengerClass:
        ===============
        Summary:
        --------
        An object built from a variable
        and consists of multiple passengers
        and an air attendant. (div chunk)
    """
    #endregion
    #region   --------------------------- MEMBERS
    passengers:list
    """
        passengers:
        ===========
        Summary:
        --------
        A list of :ref:`Passenger` objects
        built when this class was built.

        The first passenger of a class
        is always the air
        attendant.
    """
    originalVariable:Any
    """
        Holds the original variable with
        which the passengers were built.
    """
    originalVariableType:str
    """
        Holds the original type
        given to this class to build
        the passengers.
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
    #endregion
    #region   ------------------- Private
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, variable, varType:str):
        """
            PassengerClass:
            ======
            Summary:
            --------
            An object built from a variable
            and consists of multiple passengers
            and an air attendant. (div chunk)

            Arguments:
            ----------
            - `variable` any variables to convert
            - `varType` the type of the class.
        """
        Debug.Start("PassengerClass -> Building")

        self.originalVariable = variable
        self.originalVariableType = varType
        self.passengers = []

        try:
            if(varType != VarTypes.String):
                bytes = list(struct.pack(varType, variable))
                sizeOf = len(bytes)
                Debug.Log(f"There is {sizeOf} bytes to convert.")
            else:
                bytes = list(pack_string(variable))
        except:
            Debug.Error(f"Failed to create passengers from {type(variable)} typed variable to {varType}")
            Debug.End()
            return Execution.Failed

        attendant = Passenger(byte=0, type=PassengerTypes.Div)
        self.passengers.append(attendant)

        for byte in bytes:
            passenger = Passenger(PassengerTypes.Byte, byte)
            if(passenger == None):
                Debug.Error("Failed to build one of the passengers.")
            self.passengers.append(passenger)

        amountOfPassengers = len(self.passengers)
        Debug.Log(f"{amountOfPassengers-1} passengers and 1 attendant now listed in the class.")
        Debug.End()
    #endregion
    pass
#====================================================================#
class ArrivalPassengerClass:
    #region   --------------------------- DOCSTRING
    """
        ArrivalPassengerClass:
        ======================
        Summary:
        --------
        Class that is built from passengers
        to be able to extract a variable
        from a class of passengers.
    """
    #endregion
    #region   --------------------------- MEMBERS
    passengers:list
    """
        passengers:
        ===========
        Summary:
        --------
        A list of :ref:`Passenger` objects
        built when this class was built.

        The first passenger of a class
        is always the air
        attendant.
    """
    originalVariable:Any
    """
        Holds the original variable with
        which the passengers were built.
    """
    originalVariableType:str
    """
        Holds the original type
        given to this class to build
        the passengers.
    """
    passedTSA:bool = None
    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
    #endregion
    #region   ------------------- Private
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, passengers:list, varType:str):
        """
            ArrivalPassengerClass:
            ======
            Summary:
            --------
            Object built that extracts a variable
            from an arrived passenger class.
            The passengers list must start with
            an attendant tho.

            Arguments:
            ----------
            - `variable` any variables to convert
            - `varType` the type of the class.
        """
        Debug.Start("ArrivalPassengerClass -> Building")
        Debug.Log(f"Converting to type {varType}")
        self.originalVariableType = varType

        # for passenger in passengers:
            # PrintPassenger(passenger)

        if(passengers[0].type != PassengerTypes.Attendant):
            Debug.Error(f"The first passenger of this class is not an attendant.")
            self.passedTSA = False
            Debug.End()
            return

        # passengers.pop(0)
        listOfBytes:list = []
        passengerCount = len(passengers)
        for passengerNumber in range(1, passengerCount):
            listOfBytes.append(passengers[passengerNumber].value_8bits[1])

        # Debug.Log(f"Trying to convert {listOfBytes} to type {varType}")

        try:
            if varType != VarTypes.String:
                byteString = bytes(listOfBytes)
                variable = struct.unpack(varType, byteString)[0]
            else:
                byteString = bytes(listOfBytes)
                variable = unpack_string(byteString)
        except:
            Debug.Error(f"Failed to create {varType} typed variable from {listOfBytes}")
            self.passedTSA = False
            Debug.End()
            return
        
        Debug.Log(f"Variable is: {variable}")

        self.originalVariable = variable
        self.originalVariableType = varType
        self.passengers = passengers
        self.passedTSA = True

        Debug.End()
    #endregion
    pass
#====================================================================#
# class GateFoundation:
#     #region   --------------------------- DOCSTRING
#     """
#         GateFoundation:
#         ======================
#         Summary:
#         --------
#         A class to be inherited by gate classes.
#         This class contains all the standard functions
#         used by the gates you will be building.
#     """
#     #endregion
#     #region   --------------------------- MEMBERS
#     maxPassengerCapacity:int = None
#     """
#         maxPassengerCapacity:
#         =====================
#         Summary:
#         --------
#         How many passengers can planes that
#         are docked to this gate carry?
#         This include
#     """

#     id:int = None
#     """
#         id:
#         ===
#         Summary:
#         ---------
#         The ID of the gate. This is used to build
#         planes as well as verify the ones attempting
#         to dock to your gate.
#     """
    
#     state:int = None
#     """
#         state:
#         ======
#         Summary:
#         --------
#         Holds the state of the gate.

#         - 0: Out of service.
#         - 1: Request needs to be sent.
#         - 2: Answer needs to be sent.
#         - 3: Gate is available for anything.

#         Defaults to `None`
#     """

#     varTypesToSendAsAnswers:list = None
#     """
#         varTypesToSendAsAnswers:
#         ========================
#         Summary:
#         --------
#         A list of types of variables
#         that are to be sent when this
#         gate will build an answer plane
#         to a master's function execution
#         request.

#         This should be set in your __init__

#         Example:
#         --------
#         varTypesToSendAsAnswers = [
#             VarTypeEnum.Bool,
#             VarTypeEnum.Bool
#         ]
#     """

#     varTypesToSendAsRequests:list = None
#     """
#         varTypesToSendAsRequests:
#         ========================
#         Summary:
#         --------
#         A list of types of variables
#         that are to be sent when this
#         gate will build a request plane
#         to ask a device to execute the
#         function associated with the ID.

#         This should be set in your __init__

#         Example:
#         --------
#         varTypesToSendAsAnswers = [
#             VarTypeEnum.Bool,
#             VarTypeEnum.Bool
#         ]
#     """

#     masterVarGetter:Any = None
#     """
#         masterVarGetter:
#         ================
#         Summary:
#         --------
#         This member needs to be replaced
#         by a function that returns a list
#         of variables (in the same order as :ref:`varTypesToSendAsRequests`)
#         The gate will execute that
#         getter function when the runway
#         wants to have a function request plane.

#         You need to tell the gate in your __init__ what that
#         function is.
#     """

#     slaveVarGetter:Any = None
#     """
#         slaveVarGetter:
#         ================
#         Summary:
#         --------
#         This member needs to be replaced
#         by a function that returns a list
#         of variables (in the same order as :ref:`varTypesToSendAsAnswers`)
#         The gate will execute that
#         getter function when it will
#         need to build an answer to a function request.

#         You need to tell the gate in your __init__ what that
#         function is.
#     """
    
#     isMasterOnly:bool = None
#     """
#         isMasterOnly:
#         =============
#         Summary:
#         --------
#         Decides if this plane should
#         execute anything if a master
#         plane is received.

#         Should be set in your __init__
#     """

#     receivedData:list = None
#     """
#         receivedData:
#         =============
#         Summary:
#         --------
#         This member holds a list of
#         parsed and decoded variables
#         in the same order of :ref:`varTypesToSendAsAnswers`
#         It is updated when a plane is docked
#         in this gate.
#     """
#     #endregion
#     #region   --------------------------- METHODS
#     #region   -------------------- Public
#     #endregion
#     #region   ------------------- Private
#     def _GetFunctionRequestPlane(self) -> Execution:
#         """
#             _GetFunctionRequestPlane:
#             ==========================
#             Summary:
#             --------
#             This function returns a plane
#             object built to be sent on your
#             function request or master runway
#             to be sent to a device that will
#             perform the function of the plane.

#             DO NOT OVERWRITE THIS FUNCTION.
#         """
#         pass

#     def _GetAnswerPlane(self) -> Execution:
#         """
#             _GetAnswerPlane:
#             ===============
#             Summary:
#             --------
#             This function returns a plane
#             object built to be sent as a 
#             reply to a function request given
#             to this gate.
#         """
    
#     def _TryToDockPlane(self, passengers:list) -> Execution:
#         """
#             _TryToDockPlane:
#             ================
#             Summary:
#             --------
#             Tries to dock a plane that just
#             arrived with your gate.
#             Do not overwrite this function.
#         """
#         Debug.Start("_TryToDockPlane")

#         # We build both planes just to be sure.
#         slaveArrival = NewArrival(passengers, self.varTypesToSendAsAnswers)
#         masterArrival = NewArrival(passengers, self.varTypesToSendAsRequests)
    
#         if(self.isMasterOnly == True):
#             # As of now, if anything is received, we just store it as if its an answer plane.
#             if(slaveArrival)


#     #endregion
#     #endregion
#     #region   --------------------------- CONSTRUCTOR
#     #endregion
    pass
#====================================================================#
def PrintPlane(plane:Plane):
    Debug.Start("PrintPlane")
    
    plane.passedTSA
    amountOfPassengers = len(plane.passengers)

    Debug.Log(f"This plane has {plane.planeID} as a callsign")
    if(plane.passedTSA):
        Debug.Log(f"This plane has passed TSA")
    else:
        Debug.Log(f"TSA checks did not pass.")

    Debug.Log(f"Plane has {plane.amountOfClasses} passenger classes.")
    Debug.Log(f"Passengers per classes: {plane.classesSizes}")
    Debug.Log(f"There is {amountOfPassengers} passengers in this plane.")
    Debug.Log(f"The passengers are divided in classes as follows: ")
    for passengerClass in plane.classes:
        PrintPassengerClass(passengerClass)

    Debug.Log("The plane has the following passengers in that order:")
    for passenger in plane.passengers:
        PrintPassenger(passenger) 
    
    Debug.End()

def PrintPassengerClass(passengerClass:PassengerClass):
    Debug.Start("Passenger class:")
    amountOfPassengers = len(passengerClass.passengers)
    Debug.Log(f"This class's passengers results in: {passengerClass.originalVariable}")
    Debug.Log(f"This class name is: {passengerClass.originalVariableType}")
    Debug.Log(f"There is {amountOfPassengers} passengers in this class including the flight attendant")
    Debug.Log(f"The passengers are listed in this class in the following order:")
    for passenger in passengerClass.passengers:
        PrintPassenger(passenger)

    Debug.End()

def PrintPassenger(passenger:Passenger):
    if(passenger.type == PassengerTypes.Byte):
        Debug.Log(f"    - Regular passenger carrying {passenger.value_10bits}")
    if(passenger.type == PassengerTypes.Check):
        Debug.Log(f"    - Copilot passenger with a checklist of {passenger.value_8bits[1]}")
    if(passenger.type == PassengerTypes.Start):
        Debug.Log(f"    - Pilot piloting a plane with callsign {passenger.value_8bits[1]}")
    if(passenger.type == PassengerTypes.Div):
        Debug.Log(f"    - Flight attendant.")

LoadingLog.End("AppLoading.py")