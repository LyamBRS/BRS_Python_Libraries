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
from .Enums import Execution
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
    #endregion
    #region   --------------------------- METHODS
    #region   -------------------- Public
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

            countedData = (countedData + passenger.value_8bits[1]) % 256
        Debug.Log(f"Counted passenger data resulted in {countedData}.")
        Debug.End()
        return countedData          
    # ------------------------------------
    def _VerifyPlaneChecksum(plane:list) -> Execution:
        """
            _VerifyPlaneChecksum:
            =====================
            Summary:
            --------
            Private method that confirms
            if a given plane's checksum
            checks out with what we
            counted.
        """
        pass
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

    classesSizes:list = []
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
    
    classes:list = []
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

    passengers:list = []
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
            Debug.Log(boardedPassengerClass)
            if(boardedPassengerClass == None):
                Debug.Error("Failed to board passengers for the specified type.")
                Debug.End()
                return Execution.Failed

            self.classes.append(boardedPassengerClass)

            for passenger in boardedPassengerClass.passengers:
                self.passengers.append(passenger)
            Debug.Log("Passengers from a class boarded the plane.")

            del boardedPassengerClass

        Debug.Log("Pilot is boarding the plane")
        planePilot = Passenger(PassengerTypes.Start, planeID)
        self.passengers.insert(0, planePilot)

        Debug.Log("Co-pilot is doing checklist")
        checklistResult = BFIO._GetPlaneChecklist(self.passengers)
        coPilot = Passenger(PassengerTypes.Check, checklistResult)

        self.passengers.append(coPilot)
        Debug.Log("All passengers are in the plane! Ready for 9/11")
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
    value_10bits:int = None
    """
        The regular 10 bits BFIO protocol
        value.
    """
    value_8bits:list = None
    """
        A list of 2 bytes representing
        the BFIO data in a byte protocol
        format.

        - [0] : type
        - [1] : 8 bits data
    """
    type:int = None
    """
        Compare with memebers of 
        :ref:`PassengersType` 
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
        Debug.Start("Passenger -> Building")

        if(byte < 0 or byte > 255):
            Debug.Error(f"FATAL PASSENGER ERROR. Passenger cant hold bytes of {byte}")
            Debug.End()
            return Execution.Failed
        
        if(type != PassengerTypes.Byte and type != PassengerTypes.Check and type != PassengerTypes.Div and type != PassengerTypes.Start):
            Debug.Error(f"Passenger's specified type; {type} isn't valid.")
            Debug.End()
            return Execution.Failed
        
        self.value_10bits = byte + type
        self.value_8bits = [type >> 8, byte]
        self.type = type

        Debug.End()
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
    passengers:list = None
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
    originalVariable = None
    """
        Holds the original variable with
        which the passengers were built.
    """
    originalVariableType:str = None
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
            bytes = list(struct.pack(varType, variable))
            sizeOf = len(bytes)
            Debug.Log(f"There is {sizeOf} bytes to convert.")
        except:
            Debug.Error(f"Failed to create passengers from {type(variable)} typed variable to {varType}")
            Debug.End()
            return Execution.Failed
        
        Debug.Log("Converting bytes to passengers...")
        for byte in bytes:
            passenger = Passenger(PassengerTypes.Byte, byte)
            if(passenger == None):
                Debug.Error("Failed to build one of the passengers.")
            self.passengers.append(passenger)
        
        attendant = Passenger(byte=0, type=PassengerTypes.Div)
        self.passengers.insert(0, attendant)

        amountOfPassengers = len(self.passengers)
        Debug.Log(f"{amountOfPassengers} passengers and attendant now listed in the class.")
        Debug.End()
    #endregion
    pass

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
        Debug.Log(f"    - Regular passenger carrying {passenger.value_10bits} BFIO values.")
    if(passenger.type == PassengerTypes.Check):
        Debug.Log(f"    - Copilot passenger with a checklist of {passenger.value_8bits[1]}")
    if(passenger.type == PassengerTypes.Start):
        Debug.Log(f"    - Pilot piloting a plane with callsign {passenger.value_8bits[1]}")
    if(passenger.type == PassengerTypes.Byte):
        Debug.Log(f"    - Flight attendant.")

LoadingLog.End("AppLoading.py")