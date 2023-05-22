#====================================================================#
# File Information
#====================================================================#
"""
    Utilities.py
    =============
    This file contains a bunch of functions that can be used
    by a Raspberry Pi to analyze its GPIO without any circuit python
    necessary.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ast import In
from ....BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Utilities.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import subprocess
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ....BRS.Debug.consoleLog import Debug
from ...Utilities.Enums import Execution
from ...Utilities.Information import Information
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Classes
#====================================================================#
class GpioEnum:
    """
        GpioEnum:
        =========
        Summary:
        --------
        Holds the current values of the keys
        stored in a GPIO dictionary.
    """
    gpio:str = "gpio"
    level:str = "level"
    pullMode:str = "pull-mode"
    function:str = "function"
    functionSelected:str = "function-selected"
    altSelected:str = "alt-selected"

#====================================================================#
# Functions
#====================================================================#
#region ----------------------------------------------------- Private
def _GetGpioNumber(line:str):
    """
        Private function that
        extracts a GPIO number
        from a string.
    """
    if(type(line) != str):
        return None

    if("GPIO" not in line):
        return None

    try:
        line = line.split(":")[0]
        line = line.replace("GPIO","")
        line = int(line)
        return line
    except:
        return None

def _GetGPIOLevel(line:str):
    """
        Private function that
        extracts a GPIO level
        from a string.
        1 = High
        0 = Low
    """
    if(type(line) != str):
        return False

    if("level" not in line):
        return False

    try:
        line = line.split("level=")[1][0]
        return int(line)
    except:
        return False

def _GetGPIOPullMode(line:str) -> str:
    """
        Private function that
        extracts a GPIO pull up
        pull down or no pull
        from a string.
    """
    if(type(line) != str):
        return False

    if("pull" not in line):
        return False

    try:
        line = line.split("pull=")[1]
        return line
    except:
        return False

def _GetGPIOFunction(line:str) -> str:
    """
        Private function that
        extracts a func
        from a string. Most
        common are INPUT and
        OUTPUT
    """
    if(type(line) != str):
        return False

    if("func" not in line):
        return False

    try:
        line = line.split("func=")[1]
        line = line.split("pull=")[0]
        line = line.strip()
        return line
    except:
        return False

def _GetGPIOfunctionSelect(line:str) -> int:
    """
        Private function that
        extracts a GPIO function
        selected from a string.
        returns a number.
    """
    if(type(line) != str):
        return False

    if("fsel" not in line):
        return False

    try:
        line = line.split("fsel=")[1]
        line = line.split(" ")[0]
        line = line.strip()
        return int(line)
    except:
        return False

def _GetGPIOAlt(line:str) -> int:
    """
        Private function that
        extracts a GPIO alternate
        mode from a string.
        If `None` is returned,
        no alt was found in that
        string. Otherwise, a number
        is returned.
    """
    if(type(line) != str):
        return None

    if("alt" not in line):
        return None

    try:
        line = line.split("alt=")[1]
        line = line.split(" ")[0]
        line = line.strip()
        return int(line)
    except:
        return None

def _GetGPIOInfoFromLine(line:str) -> dict:
    """
        Function that builds a
        dictionary based off the
        content of a line printed
        out in the terminal when all
        GPIOs were printed.
    """
    if(type(line) != str):
        return None

    if("BANK" in line):
        return None

    gpioNumber      = _GetGpioNumber(line)
    if(gpioNumber == None):
        return None
    level           = _GetGPIOLevel(line)
    pullMode        = _GetGPIOPullMode(line)
    function        = _GetGPIOFunction(line)
    functionSelect  = _GetGPIOfunctionSelect(line)
    alt             = _GetGPIOAlt(line)

    returnedDictionary = {
        GpioEnum.gpio : gpioNumber,
        GpioEnum.level : level,
        GpioEnum.pullMode : pullMode,
        GpioEnum.function : function,
        GpioEnum.functionSelected : functionSelect,
        GpioEnum.altSelected : alt
    }
    return returnedDictionary

#endregion

def GetGPIOInformation() -> list:
    """
        GetGPIOInformation:
        ===================
        Summary:
        --------
        Function that returns a list of dictionaries.
        There is as many dictionaries as there is GPIO
        pins.

        Warnings:
        ---------
        This function only works on Raspbian OS
        on Raspberry Pis that have the GPIO tools
        installed on them. You need to have initialized
        the Information class (simply by importing it)
        before calling this class.

        Dictionary example:
        -------------------
        ```
            [
                {
                    "gpio" : int # GPIO number,
                    "level" : int # 1 or 0 depending on HIGH or LOW,
                    "pull-mode" : str # UP or DOWN or NONE,
                    "function" : str # OUTPUT or INPUT or something else,
                    "function-selected" : int,
                    "alt-selected" : int # None if not applicable
                },
                {
                    "gpio" : 1,
                    "level" : 0,
                    "pull-mode" : "UP",
                    "function" : "INPUT",
                    "function-selected" : 1,
                    "alt-selected" : None
                },
            ]
        ```

        Returns:
        --------
        - `list` = The function worked.
        - `Execution.Failed` = Something didn't work out.
        - `Execution.Incompatibility` = Your device cannot use this function.
    """
    Debug.Start("GetGPIOInformation")

    if(not Information.initialized):
        Debug.Error("You cannot use GetGPIOInformation if Information isn't initialized")
        Debug.End()
        return Execution.Failed

    if(Information.platform != "Linux"):
        Debug.Error(f"Your platform does not support GPIO: {Information.platform}")
        Debug.End()
        return Execution.Incompatibility

    command = 'sudo raspi-gpio get'
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
    except:
        Debug.Error(f"Failed to execute '{command}' on your device. You cannot use GPIO functions")
        Debug.End()
        return

    resultedList = []
    for line in output.splitlines():
        information = _GetGPIOInfoFromLine(line)
        if(information != None):
            resultedList.append(information)
    Debug.End()
    return resultedList


#====================================================================#
LoadingLog.End("AppLoading.py")