#====================================================================#
# File Information
#====================================================================#
"""
    information.py
    =============
    This file is used to handle the gathering and other basic actions
    about your system's information. This means gathering which
    platform you are using, the OS used, processor, architectures and
    so much more. Simply build the information class once.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ....BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("information.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import platform
#endregion
#region --------------------------------------------------------- BRS
from ...Debug.consoleLog import Debug
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Information:
    #region   --------------------------- DOCSTRING
    """
        Information:
        ============
        This class allows you to gather system informations
        easily. Build it once at the start of your application.
    """
    #endregion
    #region   --------------------------- MEMBERS
    platform:str = None
    """
        Holds the platform type which is running this script.
        A platform represents the OS type that is running.
        "Windows", "Linux", "Darwin", "Java"

        Defaults to `None`
    """

    processorType:str = None
    """
        Holds the style of the processor.
        - 32-bit x86: `"i386"`, `"i486"`, `"i586"`, `"i686"`
        - 64-bit x86: `"x86_64"`, `"amd64"`, `"arm64"`
        - ARM based:  `"armv6l"`, `"armv7l"`, `"aarch64"` -> Raspberry pies IoTs
        - PowerPC:    `"ppc64"`, `"ppc64le"`
        - IBM Z:      `"s390x"`

        Defaults to `None`
    """

    pythonVersion:str = None
    """
        Holds the python version which is executing the script.

        Defaults to `None`
    """

    PCName:str = None
    """
        Holds the actual name of the device being used.
        This is used as network name and not a user/profile name
        in most cases.

        Defaults to `None`

    """

    initialized:bool = False
    """
        if `True` the class is ready to be used, otherwise don't read the values,
        they default to `None`.
    """
    #endregion
    #region   --------------------------- METHODS
    def __init__(self) -> None:
        """
            Builds the System information's class.
        """
        Debug.Start("Information -> __init__")

        self.platform = platform.system()
        self.PCName = platform.node()
        self.processorType = platform.machine()
        self.pythonVersion = platform.python_version

        try:
            Debug.Log("processor: \t"    + str(platform.processor()))
            Debug.Log("system: \t"       + str(platform.system()))
            Debug.Log("version: \t"      + str(platform.version()))
            Debug.Log("machine: \t"      + str(platform.machine()))
            Debug.Log("architecture: \t" + str(platform.architecture()))
            Debug.Log("platform: \t" + str(platform.platform()))
            Debug.Log("node: \t" + str(platform.node()))
            Debug.Log("python_branch: \t" + str(platform.python_branch()))
            Debug.Log("python_version: \t" + str(platform.python_version()))
            Debug.Log("python_revision: \t" + str(platform.python_revision()))
            Debug.Log("python_implementation: \t" + str(platform.python_implementation()))
            Debug.Log("mac_ver: \t" + str(platform.mac_ver()))
            Debug.Log("win32_ver: \t" + str(platform.win32_ver()))
            Debug.Log("win32_edition: \t" + str(platform.win32_edition()))
        except:
            Debug.Warn("Not all information could be gathered.")

        initialized = True
        Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass

Information.__init__(Information)
#====================================================================#
LoadingLog.End("information.py")