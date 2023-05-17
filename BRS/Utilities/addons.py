#====================================================================#
# File Information
#====================================================================#
"""
    addons.py
    =========
    Summary:
    --------
    This file contains the addon class and its subclasses which is 
    used by your application to handle BRS styled installable addons
    so your application can access their functions in one place.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("addons.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ..Debug.consoleLog import Debug
from .Enums import Execution
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Enums classes
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("Addons")
class Addons:
    #region   --------------------------- DOCSTRING
    """
        Addons:
        =========
        Summary:
        --------
        Global class that saves all the addons such
        as hardware addons, external addons, extensions
        and much more into one place to be accessed
        by your application globally.

        Attention:
        ----------
    """
    #endregion
    #region   --------------------------- MEMBERS
    _listedAddons:dict = {}
    """
        _listedAddons:
        ==============
        Summary:
        --------
        This private member holds a dictionary
        defaulted to {} that saves all the
        hardware addons's functions. Please note
        that these are aimed towards BRS Kontrol
        but can easily be adapted to your own
        application. The application can then
        run a for loop to execute all functions
        at once.

        Example:
        --------
        ```
        "Accelerometer" : {
            "Launch"        : <function>, 
            "Stop"          : <function>,
            "Uninstall"     : <function>,
            "Update"        : <function>
            "GetState"      : <function>, 
            "ClearProfile"  : <function>, 
            "SaveProfile"   : <function>, 
            "ChangeProfile" : <function>, 
            "LoadProfile"   : <function>,
            "GetAllHardwareControls"        : <function>,
            "GetAllSoftwareActions"         : <function>,
            "ChangeButtonBinding"           : <function>,
            "ChangeAxisBinding"             : <function>,
            "ChangeButtonActionBinding"     : <function>,
            "ChangeAxisActionBinding"       : <function>,

            "information" : {
                    "version" : 1,
                    "name" : "ADXL343",
                    "type" : "addon
                    "repository" : "http://somethingSomething-GitHub.tho"
                    "description" : "Soldered on Kontrol's accelerometer addon."
                    "outputsHardwareControls" : False,
                    "canReadSoftwareControls" : True,
                    "isCompatible" : True
                }
            }
        ```
        Dictionary's Content:
        =====================
        "Launch":
        ---------
            * [Summary]:
                - A function that launches your addon regardless of its type.
                    if its a driver, it starts the driver, if its an extension
                    card, it launches its driver, if its a device, it launches
                    its GUI and so on.

            * [Arguments]:
                - None

            * [Returns]:
                - `Execution.Passed` = It launched successfully.
                - `Execution.Failed` = Something went wrong.
                - `Execution.Incompatible` = That can't execute on your device.

        "Stop":
        -------
            * [Summary]:
                - A function that stops your addon regardless of its type.
                If its an hardware addon, it stops its driver. If its an
                expansion card, it unlists it and disconnects it. If its a
                device driver, it force quits the GUI.

            * [Arguments]:
                - None

            * [Returns]:
                - `Execution.Passed` = It stopped successfully.
                - `Execution.Failed` = Something went wrong.
                - `Execution.Unecessary` = Addon was never launched.
                - `Execution.Incompatible` = This addon cannot execute on your device.

        "Uninstall":
        ------------
            * [Summary]:
                - A function that attempts to uninstall a downloaded
                addon, deleting it permanently and removing it from
                this list in the process.

            * [Arguments]:
                - None

            * [Returns]:
                - `Execution.Passed` = Addon successfully reduced to atoms.
                - `Execution.Failed` = Something went wrong.
                - `Execution.Unecessary` = That addon is already uninstalled.

        "Update":
        ---------
            * [Summary]:
                - A function that attempts to update the addon through
                git libraries.

            * [Arguments]:
                - None

            * [Returns]:
                - `Execution.Passed` = Addon was updated successfully.
                - `Execution.Failed` = Addon couldn't update itself.
                - `Execution.Unecessary` = That addon is up to date.
                - `Execution.NoConnection` = Can't update due to no connections.

        "GetState":
        -----------
            * [Summary]:
                - A function that returns the current state of the
                addon. 

            * [Arguments]:
                - None

            * [Returns]:
                - `True` = Addon is currently running.
                - `False` = Addon isn't running.

        "ClearProfile":
        ---------------
            * [Summary]:
                - A function that removes a profile from the
                profiles saved by this addon. This means deleting
                that profile from the addon's cache basically.

            * [Arguments]:
                - `profileToClear:str` = The name of the profile to clear.

            * [Returns]:
                - `Execution.Passed` = Profile is now deleted
                - `Execution.Failed` = Couldn't delete the given profile.
                - `Execution.Incompatibility` = The addon does not support profiles.

        "SaveProfile":
        ---------------
            * [Summary]:
                - A function that saves the current profile in the
                addon's cache. This means taking the current profile
                and saving the currently loaded information in it, then
                saving the JSON file.

            * [Arguments]:
                - `profileToSave:str` = Optional parameter that specifies which profile to save the content under.

            * [Returns]:
                - `Execution.Passed` = Save was successful. JSON was updated with new data.
                - `Execution.Failed` = Couldn't save the given or current profile in cache.
                - `Execution.Incompatibility` = The addon does not support profiles.

        "ChangeProfile":
        ---------------
            * [Summary]:
                - This function's purpose is to replace the name
                of a saved profile with another. This is used when
                the user edit its profile name and saves it.

            * [Arguments]:
                - `newProfileName:str` = string representing the new profile to save.
                - `oldProfileName:str` = sring representing the previous profile's name.

            * [Returns]:
                - `Execution.Passed` = old profile is now saved under new profile
                - `Execution.Failed` = Couldn't change oldProfile to newProfile
                - `Execution.Incompatibility` = The addon does not support profiles.

        "LoadProfile":
        --------------
            * [Summary]:
                - This function loads a specified profile from
                its cached JSONs. if the profile does not exist,
                its created with default parameters, then loaded.

            * [Arguments]:
                - `profileToLoad:str` = string representing the profile to load.

            * [Returns]:
                - `Execution.Passed` = Profile is created / loaded
                - `Execution.Failed` = Couldn't load that profile and couldn't create a new one.
                - `Execution.Incompatibility` = The addon does not support profiles.

        "GetAllHardwareControls":
        -------------------------
            * [Summary]:
                - Function that returns a dictionary of
                all the hardware controls that the addon
                can give to your application.

            * [Arguments]:
                - `None`

            * [Returns]:
                - {
                    "buttons" : {
                        "hardware-name" : {
                            "binded" : False, 
                            "bindedTo" : "software_name",
                            "getter" : <function>
                        }                 
                    }, 
                    "axes" : {
                        "hardware-name" : {
                            "binded" : False, 
                            "bindedTo" : "software_name",
                            "getter" : <function>
                        }                 
                    }
                   }
                - `Execution.Failed` = Couldn't get the hardware controls of the addon
                - `Execution.Incompatibility` = The addon does not support hardware outputs.

        "GetAllSoftwareActions":
        ------------------------
            * [Summary]:
                - Function that returns a dictionary of software
                specific actions that your application can make 
                the addon perform. Such as: turn on the lights,
                surface, dive, cruise control and much more.

            * [Arguments]:
                - `None`

            * [Returns]:
                - {
                    "buttons" : {
                        "action-name" : {
                            "binded" : False, 
                            "bindedTo" : "software_name",
                            "executer" : <function>
                        }                 
                    }, 
                    "axes" : {
                        "action-name" : {
                            "binded" : False, 
                            "bindedTo" : "software_name",
                            "executer" : <function>
                        }                 
                    }
                   }
                - `Execution.Failed` = Couldn't get the actions of the addon
                - `Execution.Incompatibility` = The addon does not support actions.

        "ChangeButtonBinding":
        ----------------------
            * [Summary]:
                - Function that changes the software button
                binded to an addon's hardware button.

            * [Arguments]:
                - `nameOfSoftwareButton:str` = Name from `SoftwareButtons` class
                - `nameOfHardwareButton:str` = Name extracted from `GetAllHardwareControls()`

            * [Returns]:
                - `Execution.Passed` = New software button binded to this one.
                - `Execution.Failed` = Failed to bind the specified button.
                - `Execution.Incompatibility` = The addon does not support hardware buttons.

        "ChangeAxisBinding":
        ----------------------
            * [Summary]:
                - Function that changes the software axis
                binded to an addon's hardware axis.

            * [Arguments]:
                - `nameOfSoftwareAxis:str` = Name from `SoftwareAxis` class
                - `nameOfHardwareAxis:str` = Name extracted from `GetAllHardwareControls()`

            * [Returns]:
                - `Execution.Passed` = New software axis binded to this one.
                - `Execution.Failed` = Failed to bind the specified axis.
                - `Execution.Incompatibility` = The addon does not support hardware axis.

        "ChangeButtonActionBinding":
        ----------------------------
            * [Summary]:
                - Function that binds a software button with an
                addon's button like action. Like binding "on" to
                a submarine's "light-on" 

            * [Arguments]:
                - `nameOfSoftwareButton:str` = Name from `SoftwareAxis` class
                - `nameOfActionToBind:str` = Name extracted from `GetAllActions()`

            * [Returns]:
                - `Execution.Passed` = New software button binded to this action.
                - `Execution.Failed` = Failed to bind the specified action with that software button.
                - `Execution.Incompatibility` = The addon does not support action binding.

        "ChangeAxisActionBinding":
        --------------------------
            * [Summary]:
                - Function that binds a software axis with an
                addon's axis like action. Like binding "right"
                with a submarine's "right"

            * [Arguments]:
                - `nameOfSoftwareButton:str` = Name from `SoftwareAxis` class
                - `nameOfActionToBind:str` = Name extracted from `GetAllActions()`

            * [Returns]:
                - `Execution.Passed` = New software button binded to this action.
                - `Execution.Failed` = Failed to bind the specified action with that software button.
                - `Execution.Incompatibility` = The addon does not support action binding.

    """
    #endregion
    #region   --------------------------- METHODS
    def AddNewAddon(newAddonsName, addonsInformation:dict) -> Execution:
        """
            AddNewAddon:
            ============
            Summary:
            --------
            Adds an addon to the list of
            addons. Your addon will be
            verified for correctness.

            Arguments:
            ----------
            - `newAddonsName:str` : string reprenting the name of your addon.
            - `addonsInformation:dict` : mega dictionary of all the information and functions of your addon. See :ref:`_listedAddons`
            
            Returns:
            --------
            - `Execution.Passed` : Your addon is now listed and ready to use by the application.
            - `Execution.Failed` : Cannot put specified informations in :ref:`_listedAddons`.
            - `Execution.Unecessary` : already in :ref:`_listedAddons`.
        """
        Debug.Start("AddNewAddon")

        if(newAddonsName in Addons._listedAddons):
            Debug.Error(f"{newAddonsName} is already listed. You can only add an addon once.")
            Debug.End()
            return Execution.Unecessary
        
        # Checking all keys of the specified dictionary:
        Debug.Warn("DO-ME: Checks for addon's passed dictionaries are bypassed.")

        Addons._listedAddons[newAddonsName] = addonsInformation
        Debug.Log(f"{newAddonsName} is now listed as an Addon.")
        Debug.End()
        return Execution.Passed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.Class("AddonInfoHandler")
class AddonInfoHandler:
    #region   --------------------------- DOCSTRING
    """
        AddonInfoHandler:
        =================
        Summary:
        --------
        Class built in your drivers that allows
        them to easily create their dictionaries
        to add to the regular Addons class
    """
    #endregion
    #region   --------------------------- MEMBERS
    information:dict = {
            "Launch"        : None, 
            "Stop"          : None,
            "Uninstall"     : None,
            "Update"        : None,
            "GetState"      : None, 
            "ClearProfile"  : None, 
            "SaveProfile"   : None, 
            "ChangeProfile" : None, 
            "LoadProfile"   : None,
            "GetAllHardwareControls"        : None,
            "GetAllSoftwareActions"         : None,
            "ChangeButtonBinding"           : None,
            "ChangeAxisBinding"             : None,
            "ChangeButtonActionBinding"     : None,
            "ChangeAxisActionBinding"       : None,

            "information" : {
                "version" : 1,
                "name" : None,
                "type" : None,
                "repository" : None,
                "description" : None,
                "outputsHardwareControls" : False,
                "canReadSoftwareControls" : False,
                "isCompatible" : False
            }
        }
    """
        information:
        ============
        Summary:
        --------
        Dictionary that will be added to the
        main addon dictionary once this
        class is built.
    """
    #endregion
    #region   --------------------------- METHODS
    def DockAddonToApplication(self, canAddonFunctionProperly:bool) -> Execution:
        """
            DockAddonToApplication:
            =======================
            Summary:
            --------
            If your addon can successfully work on the
            device that is executing the python script,
            you then need to call this function to ensure
            that the application has full access to its
            main mandatory functions.

            Otherwise, call this anyways and specify
            that it cannot work properly on this
            device by using the input parameter.
        """
        Debug.Start("DockAddonToApplication")

        Debug.Log("Saving compatibility in dictionary...")
        self.information["information"]["isCompatible"] = canAddonFunctionProperly
        Debug.Log(f"Can this addon work on this device? {canAddonFunctionProperly}")

        Debug.Log("Attempting to add the addon to the application's list of addons.")
        result = Addons.AddNewAddon(self.information["information"]["name"], self.information)
        if(result != Execution.Passed):
            Debug.Error("Something went wrong when trying to add the addon in the application's list.")
            Debug.Error(f"Error code: {result}")
            Debug.End()
            return Execution.Failed
        
        Debug.Log(">>> Success")
        Debug.End()
        return Execution.Passed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 name:str,
                 description:str,
                 version:str,
                 type:str,
                 repository:str,
                 outputsHardwareControls:bool,
                 canReadSoftwareControls:bool,

                 LaunchFunction,
                 StopFunction,
                 UninstallFunction,
                 UpdateFunction,
                 GetStateFunction,
                 ClearProfileFunction,
                 SaveProfile,
                 ChangeProfile,
                 LoadProfile,
                 GetAllHardwareControls,
                 GetAllSoftwareActions,
                 ChangeButtonBinding,
                 ChangeAxisBinding,
                 ChangeButtonActionBinding,
                 ChangeAxisActionBinding
                 ):
        """
            AddonInfoHandler:
            =================
            Summary:
            --------
            Class built in your drivers that allows
            them to easily create their dictionaries
            to add to the regular Addons class

            Arguments:
            ----------
            Please refer to :ref:`Addons` class's _list private member.
            it will explain in great details each one of these as well
            as their expected returned values and input parameters.
        """
        Debug.Start("AddonInfoHandler -> __init__")

        Debug.Log("Saving regular informations...")
        informationsToSave:dict = {
                "version" : version,
                "name" : name,
                "type" : type,
                "repository" : repository,
                "description" : description,
                "outputsHardwareControls" : outputsHardwareControls,
                "canReadSoftwareControls" : canReadSoftwareControls,
                "isCompatible" : False 
        }
        self.information["information"] = informationsToSave
        Debug.Log(">>> Success")

        Debug.Log("Saving functions...")
        Debug.Warn("TODO: Addon's functions are not tested.")

        self.information["Launch"] = LaunchFunction
        self.information["Stop"] = StopFunction
        self.information["Uninstall"] = UninstallFunction
        self.information["Update"] = UpdateFunction
        self.information["GetState"] = GetStateFunction
        self.information["ClearProfile"] = ClearProfileFunction
        self.information["SaveProfile"] = SaveProfile
        self.information["ChangeProfile"] = ChangeProfile
        self.information["LoadProfile"] = LoadProfile
        self.information["GetAllHardwareControls"] = GetAllHardwareControls
        self.information["GetAllHardwareControls"] = GetAllHardwareControls
        self.information["GetAllSoftwareActions"] = GetAllSoftwareActions
        self.information["ChangeButtonBinding"] = ChangeButtonBinding
        self.information["ChangeAxisBinding"] = ChangeAxisBinding
        self.information["ChangeButtonActionBinding"] = ChangeButtonActionBinding
        self.information["ChangeAxisActionBinding"] = ChangeAxisActionBinding
        Debug.Log(">>> Success")
        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.Class("AddonFoundations")
class AddonFoundations:
    #region   --------------------------- DOCSTRING
    """
        AddonFoundations:
        =================
        Summary:
        --------
        Class herited by installed addons so that
        they all have their default functions
        working and you won't have to create
        them by hand if you're not using them.
    """
    #endregion
    #region   --------------------------- MEMBERS
    state:bool = False
    """
        state
        =====
        Summary:
        --------
        Holds the current state of your addon:
        - `True` = running
        - `False` = not running
    """
    #endregion
    #region   --------------------------- METHODS
    def Launch() -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            Execution.ByPassed until its defined
            in your class.
        """
        Debug.Start("Launch")
        Debug.Warn("BYPASSED - NOT DEFINED")
        Debug.End()
        return Execution.ByPassed
    # -------------------------------------------
    def Stop() -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            Execution.ByPassed until its defined
            in your class.
        """
        Debug.Start("Stop")
        Debug.Warn("BYPASSED - NOT DEFINED")
        Debug.End()
        return Execution.ByPassed
    # -------------------------------------------
    def Uninstall() -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("Uninstall")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def Update() -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("Update")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def GetState() -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("GetState")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def ClearProfile(profileToClear:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("ClearProfile")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def SaveProfile(profileToSave:str = None) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("SaveProfile")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def ChangeProfile(newProfileName:str, oldProfileName:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("ChangeProfile")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def LoadProfile(profileToLoad:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("LoadProfile")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def GetAllHardwareControls() -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("GetAllHardwareControls")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def GetAllSoftwareActions(profileToLoad:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("GetAllSoftwareActions")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def ChangeButtonBinding(nameOfSoftwareButton:str, nameOfHardwareButton:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("ChangeButtonBinding")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def ChangeAxisBinding(nameOfSoftwareAxis:str, nameOfHardwareAxis:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("ChangeAxisBinding")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def ChangeButtonActionBinding(nameOfSoftwareButton:str, nameOfActionToBind:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("ChangeButtonActionBinding")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    # -------------------------------------------
    def ChangeAxisActionBinding(nameOfSoftwareAxis:str, nameOfActionToBind:str) -> Execution:
        """
            `Attention`:
            ==========
            This function is not yet defined in
            this addon. It will return 
            `Execution.Incompatibility` until 
            its defined in your class. This means
            that the application will think that
            it isn't a supported function.
        """
        Debug.Start("ChangeAxisActionBinding")
        Debug.Warn("NOT SUPPORTED")
        Debug.End()
        return Execution.Incompatibility
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 name:str,
                 description:str,
                 version:str,
                 type:str,
                 repository:str,
                 outputsHardwareControls:bool,
                 canReadSoftwareControls:bool,

                 LaunchFunction,
                 StopFunction,
                 UninstallFunction,
                 UpdateFunction,
                 GetStateFunction,
                 ClearProfileFunction,
                 SaveProfile,
                 ChangeProfile,
                 LoadProfile,
                 GetAllHardwareControls,
                 GetAllSoftwareActions,
                 ChangeButtonBinding,
                 ChangeAxisBinding,
                 ChangeButtonActionBinding,
                 ChangeAxisActionBinding
                 ):
        """
            AddonInfoHandler:
            =================
            Summary:
            --------
            Class built in your drivers that allows
            them to easily create their dictionaries
            to add to the regular Addons class

            Arguments:
            ----------
            Please refer to :ref:`Addons` class's _list private member.
            it will explain in great details each one of these as well
            as their expected returned values and input parameters.
        """
        Debug.Start("AddonInfoHandler -> __init__")

        Debug.Log("Saving regular informations...")
        informationsToSave:dict = {
                "version" : version,
                "name" : name,
                "type" : type,
                "repository" : repository,
                "description" : description,
                "outputsHardwareControls" : outputsHardwareControls,
                "canReadSoftwareControls" : canReadSoftwareControls,
                "isCompatible" : False 
        }
        self.information["information"] = informationsToSave
        Debug.Log(">>> Success")

        Debug.Log("Saving functions...")
        Debug.Warn("TODO: Addon's functions are not tested.")

        self.information["Launch"] = LaunchFunction
        self.information["Stop"] = StopFunction
        self.information["Uninstall"] = UninstallFunction
        self.information["Update"] = UpdateFunction
        self.information["GetState"] = GetStateFunction
        self.information["ClearProfile"] = ClearProfileFunction
        self.information["SaveProfile"] = SaveProfile
        self.information["ChangeProfile"] = ChangeProfile
        self.information["LoadProfile"] = LoadProfile
        self.information["GetAllHardwareControls"] = GetAllHardwareControls
        self.information["GetAllHardwareControls"] = GetAllHardwareControls
        self.information["GetAllSoftwareActions"] = GetAllSoftwareActions
        self.information["ChangeButtonBinding"] = ChangeButtonBinding
        self.information["ChangeAxisBinding"] = ChangeAxisBinding
        self.information["ChangeButtonActionBinding"] = ChangeButtonActionBinding
        self.information["ChangeAxisActionBinding"] = ChangeAxisActionBinding
        Debug.Log(">>> Success")
        Debug.End()
    #endregion
    pass


LoadingLog.End("addons.py")