#====================================================================#
# File Information
#====================================================================#
"""
    Handles the loading, saving and handling of various types of file.
    More specifically JSON files.
"""
#====================================================================#
# Imports
#====================================================================#
from .Enums import Execution, FileIntegrity
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("FileHandler.py")

import errno, os, sys, time
import json
from ..Debug.consoleLog import Debug
#====================================================================#
# Functions
#====================================================================#

# Sadly, Python fails to provide the following magic number for us.
ERROR_INVALID_NAME = 123
'''
Windows-specific error code indicating an invalid pathname.

See Also
----------
https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-
    Official listing of all such codes.
'''

def IsPathValid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
# -------------------------------------------------------------------
def GetJsonData(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
# -------------------------------------------------------------------
def CompareKeys(struct, obj, prefix=''):
    """
        CompareKeys:
        ------------
        This function's purpose is to recursively compare the keys
        in a Json file with a structure variable.
        If the keys don't match, `FileIntegrity.Corrupted` is returned.
        Otherwise, `FileIntegrity.Good` is returned

        struct : JsonStructure
        obj : JSONData
    """
    Debug.Start("CompareKeys")
    for key in struct.keys():
        Debug.Log(f"Checking: {key}")
        if key not in obj:
            Debug.Log(f"Key '{prefix}.{key}' not found in loaded JSON file.")
            Debug.End()
            return FileIntegrity.Corrupted
        elif isinstance(struct[key], dict):
            if not isinstance(obj[key], dict):
                Debug.Log(f"Value of '{prefix}.{key}' in loaded JSON file is not a dictionary.")
                Debug.End()
                return FileIntegrity.Corrupted
            else:
                CompareKeys(struct[key], obj[key], f"{prefix}.{key}")
    Debug.End()
    return FileIntegrity.Good
# -------------------------------------------------------------------
def AppendPath(pathA:str, pathB:str):
    """
        AppendPath:
        -----------
        Append path is used to add and get a new path from another
        one. os.getcwd() will define if \\ or / is used in
        the path.
    """
    Debug.Start("AppendPath", DontDebug=True)

    reference = os.getcwd()

    if("\\" in reference):
        Debug.Log("Path is using \\")
        pathB = pathB.replace("/","\\")
        pathA = pathA.replace("/","\\")
    elif("/" in reference):
        Debug.Log("Path is using /")
        pathB = pathB.replace("\\","/")
        pathA = pathA.replace("\\","/")

    Debug.End(ContinueDebug=True)
    return pathA + pathB
# -------------------------------------------------------------------
def GetParentPath(path) -> str:
    """
        GetParentPath:
        ================
        Summary:
        --------
        This function returns the path of the parent folder
        of the specified path.

        Returns:
        --------
        - `Execution.Failed` : Could not get the parent folder
        - `str` : name of the parent folder
    """
    Debug.Start("GetParentFolder", DontDebug=True)

    Debug.Log("Checking path validitiy")
    isValid = IsPathValid(path)
    if(isValid):
        parentPath = path.rstrip(os.path.basename(path))
        Debug.Log(f"Parent path: {parentPath}")
        Debug.End(ContinueDebug=True)
        return parentPath
    else:
        Debug.Error("PATH IS NOT VALID")
        Debug.End(ContinueDebug=True)
        return Execution.Failed
# -------------------------------------------------------------------
def GetFolderFromPath(path) -> str:
    """
        GetFolderFromPath:
        ==================
        Summary:
        --------
        Returns the last directory of a given path.
    """
    return os.path.basename(os.path.normpath(path))
# -------------------------------------------------------------------
def CompareList(expected:list, current:list, exceptions:list=None, DontDebug:bool=True) -> Execution:
    """
        CompareList:
        ============
        Summary:
        --------
        This function compares an expected list with an other list
        and depending on the comparaison results, an `Execution` enum
        value is returned.

        exception parameter is used as an optional input list that is
        simply not taken into account when comparing the 2 other lists.
        This means you can specify things that won't be taken into
        account during comparaison if they are found in the 2 other
        lists.
    """
    Debug.Start("CompareList", DontDebug=DontDebug)
    ContinueDebug = True

    if exceptions != None:
        Debug.Log(f">>> Removing exceptions from given lists: {exceptions}")
        current = [item for item in current if item not in exceptions]
        expected = [item for item in expected if item not in exceptions]

    #region ------------------------------------- [0]
    Debug.Log("[0]: List sizes")
    if(len(expected) != len(current)):
        Debug.Error(">>> Lenght of current did not match lenght of expected.")
        Debug.End(ContinueDebug=ContinueDebug)
        return Execution.Failed
    #endregion
    #region ------------------------------------- [1]
    Debug.Log("[1]: List content")
    if all(elem in current for elem in expected):
        Debug.Log(">>> SUCCESS")
    else:
        Debug.Error(">>> Content did not match.")
        Debug.End(ContinueDebug=ContinueDebug)
        return Execution.Failed
    #endregion
    #region ------------------------------------- [2]
    Debug.Log(">>> Comparaison successful.")
    Debug.End(ContinueDebug=ContinueDebug)
    return Execution.Passed
    #endregion
#====================================================================#
# Classes
#====================================================================#
class JSONdata:
    #region   --------------------------- DOCSTRING
    """
        This class is used to hold the configuration data loaded from
        a JSON file.
        
        The class holds a path which needs to be set to where your application's
        JSON files are located. You can then build JSONdata classes for each
        files located within that folder.

        You can then access the data from a JSON file by using this class.
    """
    #endregion
    #region   --------------------------- MEMBERS
    pathToDirectory: str = None
    """
        Path to the directories where your application's JSONs are saved.
    """

    fileName: str = None
    """
        The name of the JSON file to parse at the location specified by `pathToDirectory`
    """

    jsonData: dict = None
    """
        Holds the retrived JSON data. Build the class to have access to this.
    """
    
    fullJsonPath:str = None
    """
        fullJsonPath:
        =============
        Summary:
        --------
        Private variable that stores the full path to the JSON file.
    """
    #endregion
    #region   --------------------------- METHODS
    def SaveFile(self) -> bool:
        #region   --------------------------- DOCSTRING
        """
            This function puts JSONdata in the loaded
            path.

            Returns True if successful, False if not.
        """
        #endregion
        Debug.Start("SaveFile")
        # Check if JSONdata has anything
        if(len(self.jsonData) > 0):
            try:
                if (self.pathToDirectory.endswith("\\") or self.pathToDirectory.endswith("/")):
                    pass
                else:
                    self.pathToDirectory = AppendPath(self.pathToDirectory, "\\")

                with open(self.pathToDirectory + self.fileName, "w") as file:
                    Debug.Log(f"Saved file at: {self.pathToDirectory + self.fileName}")
                    json.dump(self.jsonData, file)
                    file.close()
                Debug.End()
                return True
            except:
                Debug.Error("COULD NOT SAVE JSON DATA")
                Debug.End()
                return False
        else:
            Debug.Error("jsonData is of lenght 0")
            Debug.End()
            return False
    def CreateFile(self, structure) -> bool:
        #region   --------------------------- DOCSTRING
        """
            This function creates a JSON file that
            follows a specified architecture and uses
            the data from when this class was built to save it.

                - `True` : Success
        """
        #endregion
        Debug.Start("JSONdata -> CreateFile")
        # Attempt to save the JSON structure.
        try:
            Debug.Log(f">>> self.pathToDirectory = {self.pathToDirectory}")
            Debug.Log(f">>> self.fileName = {self.fileName}")
            with open(self.pathToDirectory + self.fileName, "w") as file:
                json.dump(structure, file)
                file.close()
            Debug.Log(">>> CreateFile -> SUCCESS")
            Debug.End()
            return True
        except:
            Debug.Error(">>> CreateFile -> COULD NOT SAVE JSON DATA")
            Debug.End()
            return False
    def ReadFile(self) -> bool:
        """
            ReadFile:
            =========
            Summary:
            --------
            Tries to read the file it was
            initialized with.

            Returns:
            -------
            - `True`: The file was read successfully.
            - `False`: The file failed to be read
        """
        Debug.Start("ReadFile")
        data = {}
        try:
            with open(self.fullJsonPath, 'r') as file:
                data = json.load(file)
                self.jsonData = data
                file.close()
            Debug.Log(">>> SUCCESS")
            Debug.End()
            return True
        except:
            Debug.Error(f"[BRS]: Could not open {self.fullJsonPath}")
            Debug.Log(">>> Second try using read")
            time.sleep(0.01)
            try:
                with open(self.fullJsonPath, 'r') as file:
                    data = json.load(file)
                    self.jsonData = data
                    file.close()
                Debug.Log(">>> SUCCESS")
                Debug.End()
                return True
            except:
                Debug.Error("Failed at the second try. Please create the file before loading it.")
                Debug.Error(f"data -> {data}")
                Debug.End()
                return False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, fileName:str = "", path:str = None) -> None:
        # Test given paths
        Debug.Start("JSONdata -> __init__")
        if(path == None):
            if(self.pathToDirectory == None):
                raise Exception("[BRS]: JSONdata: NO PATH SPECIFIED")
            else:
                Debug.Log(f">>> Using self.pathToDirectory: {self.pathToDirectory}")
        else:
            if(IsPathValid(path)):
                Debug.Log(">>> Path specified is valid.")
                self.pathToDirectory = path
            else:
                Debug.End()
                raise Exception("[BRS]: Invalid path given to JSONdata.")

        # Check the class and parameter's file name.
        if(fileName == None):
            if(self.fileName == None):
                Debug.End()
                raise Exception("[BRS]: No file name specified")
            else:
                Debug.Log(f">>> Using self.fileName: {self.fileName}")
        else:
            if(fileName.__contains__(".json") or fileName.__contains__(".JSON")):
                self.fileName = fileName
                Debug.Log(f">>> self.fileName = {fileName}")
            else:
                fileName = f"{fileName}.json"
                self.fileName = fileName
                Debug.Log(f">>> self.fileName = {fileName}")

        # Create the path to the specified JSON and try to open it.
        if(self.pathToDirectory.endswith("/") or self.pathToDirectory.endswith("\\")):
            jsonPath = AppendPath(self.pathToDirectory, self.fileName)
        else:
            jsonPath = AppendPath(self.pathToDirectory, "/" + self.fileName)
        data = None

        Debug.Log(f">>> jsonPath = {jsonPath}")
        self.fullJsonPath = jsonPath

        # Validate that the path can exist.
        if(IsPathValid(jsonPath)):
            Debug.Log(">>> jsonPath is valid")
            try:
                with open(jsonPath, 'r') as file:
                    data = json.load(file)
                Debug.Log(">>> SUCCESS")
            except:
                Debug.Error(f"[BRS]: Could not open {self.fileName} at {self.pathToDirectory}")
                Debug.Log(">>> Second try using read")
                try:
                    with open(jsonPath, 'r') as file:
                        data = json.load(file)

                    Debug.Log(">>> SUCCESS")
                except:
                    Debug.Error("Failed at the second try. Please create the file before loading it.")
                    Debug.Error(f"data -> {data}")
        else:
            Debug.End()
            raise Exception(f"[BRS]: JSONdata path is not valid once built: {jsonPath}")

        #Put the data in the class.
        self.jsonData = data
        Debug.End()
    #endregion
    pass
#====================================================================#
class FilesFinder:
    #region   --------------------------- DOCSTRING
    """
        This class is used to load all the names of JSON files within
        a specific directory.

        This class does not load any data, it only loads the name of all
        the files of a specific type located at a specific location.
    """
    #endregion
    #region   --------------------------- MEMBERS
    pathToDirectory: str = None
    """
        Path to the directories where the files to load are located
    """
    fileList:list = []
    """
        Holds the a list of all the names of the files found at that
        location
    """
    fileExtension : str = None
    """
        What type of file to load from the location.
        ".json", ".txt" etc
    """
    #endregion
    #region   --------------------------- METHODS
    def LoadFiles(self) -> bool:
        #region   --------------------------- DOCSTRING
        """
            This function loads all the files of a specific
            extension at a specified path.

            If the function returns True, some files were loaded.
            If the function returns False, no files were loaded.
        """
        #endregion
        Debug.Start("LoadFiles")
        filenames:list = []
        fileFound:bool = False

        # Check class's parameters
        Valided:bool = self.SelfCheck()

        if(Valided):
            for filename in os.listdir(self.pathToDirectory):
                if filename.endswith(self.fileExtension):
                    filenames.append(filename)
                    fileFound = True
                    Debug.Log(f"found: ({filename})")

            self.fileList = filenames
            Debug.Log(f"fileFound: {fileFound}")
            Debug.End()
            return fileFound
        else:
            Debug.Error("Failed to validate FilesFinder's attributes.")
            Debug.End()
            return False
    def SelfCheck(self) -> bool:
        #region   --------------------------- DOCSTRING
        """
            This checks the variables stored in this function.
            It checks the following:
            - Is pathToDirectory valid?
            - Is fileExtension valid?
            - 
        """
        #endregion
        # Is the path specified correct?
        if(self.pathToDirectory == None):
            return False
        else:
            if(IsPathValid(self.pathToDirectory)):
                pass
            else:
                return False

        # Check file extension.
        if(self.fileExtension == None):
            return False
        else:
            if(self.fileExtension.__contains__(".") and len(self.fileExtension) > 1):
                pass
            else:
                fileName = f".{fileName}"
                self.fileName = fileName

                if(len(self.fileExtension) == 1):
                    return False

        return True

    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, fileExtension:str = "", path:str = None) -> None:
        Debug.Start("FilesFinder: __init__")
        # Check if path valid
        if(path == None):
            if(self.pathToDirectory == None):
                raise Exception("[BRS]: FilesFinder: No path specified.")
            else:
                if(IsPathValid(self.pathToDirectory)):
                    Debug.Log("specified pathToDirectory is valid")
                    pass
                else:
                    raise Exception("[BRS]: FilesFinder: stored path was not valid")
        else:
            if(IsPathValid(path)):
                Debug.Log("specified path is valid. Putting it as pathToDirectory")
                self.pathToDirectory = path
            else:
                raise Exception("[BRS]: FilesFinder: specified path is not valid")

        # Check the class's parameter's file extensions.
        if(fileExtension == None):
            if(self.fileExtension == None):
                raise Exception("[BRS]: FilesFinder: No file extension")
        else:
            if(fileExtension.__contains__(".")):
                self.fileExtension = fileExtension
                Debug.Log("specified extension already contains a dot.")
            else:
                self.fileExtension = f".{fileExtension}"
                Debug.Log("adding dot to file extension")

        Debug.Log(f"Resulted pathtodirectory: {self.pathToDirectory}")
        Debug.Log(f"Resulted fileExtension: {self.fileExtension}")
        # Check the class's parameters
        fileFound:bool = self.LoadFiles()
        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.End("FileHandler.py")