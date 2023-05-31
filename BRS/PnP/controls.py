#====================================================================#
# File Information
#====================================================================#
"""
    controls.py
    =============
    Summary:
    --------
    This file holds the control class which can be used throughout
    your application to store inputs and keybinds for global
    accessibilities. The class  held is also used in asyncronous 
    drivers such as Accelerometers and BrSpand card readings.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("controls.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ..Debug.consoleLog import Debug
from ..Utilities.Enums import Execution
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
class SoftwareButtons:
    """
        SoftwareButtons:
        ================
        Summary:
        --------
        Static class that holds
        the name of all the software
        buttons used by the `Controls`
        class.

        Attention:
        ----------
        DO NOT OVERWRITE THE VALUES STORED
        IN THIS FUCKING CLASS ALRIGHT?
    """
    up        :str = "up"        
    down      :str = "down"      
    left      :str = "left"      
    right     :str = "right"     
    forward   :str = "forward"   
    backward  :str = "backward"  
    fire      :str = "fire"     
    explode   :str = "explode"  
    select    :str = "select"   
    cancel    :str = "cancel"   
    confirm   :str = "confirm"  
    mute      :str = "mute"     
    record    :str = "record"   
    save      :str = "save"     
    reset     :str = "reset"    
    refresh   :str = "refresh"  
    quit      :str = "quit"     
    stop      :str = "stop"     
    shutdown  :str = "shutdown" 
    edit      :str = "edit"     
    add       :str = "add"      
    remove    :str = "remove"   
    copy      :str = "copy"     
    paste     :str = "paste"    
    cut       :str = "cut"      
    undo      :str = "undo"     
    redo      :str = "redo"     
    print     :str = "print"    
    close     :str = "close"    
    open      :str = "open"     
    fill      :str = "fill"     
    empty     :str = "empty"    
    like      :str = "like"     
    dislike   :str = "dislike"  
    lock      :str = "lock"     
    unlock    :str = "unlock"   
    on        :str = "on"       
    off       :str = "off"      
    custom_1  :str = "custom-1"  
    custom_2  :str = "custom-2"  
    custom_3  :str = "custom-3"  
    custom_4  :str = "custom-4"  
    custom_5  :str = "custom-5"  
    custom_6  :str = "custom-6"  
    custom_7  :str = "custom-7"  
    custom_8  :str = "custom-8"  
    custom_9  :str = "custom-9"  
    custom_10 :str = "custom-10" 
    custom_11 :str = "custom-11" 
    custom_12 :str = "custom-12" 
    custom_13 :str = "custom-13" 
    custom_14 :str = "custom-14" 
    custom_15 :str = "custom-15" 
    custom_16 :str = "custom-16" 
    custom_17 :str = "custom-17" 
    custom_18 :str = "custom-18" 
    custom_19 :str = "custom-19" 
    custom_20 :str = "custom-20" 
    custom_21 :str = "custom-21" 
    custom_22 :str = "custom-22" 
    custom_23 :str = "custom-23" 
    custom_24 :str = "custom-24" 
    custom_25 :str = "custom-25" 
    custom_26 :str = "custom-26" 
    custom_27 :str = "custom-27" 
    custom_28 :str = "custom-28" 
    custom_29 :str = "custom-29" 
    custom_30 :str = "custom-30" 
    custom_31 :str = "custom-31" 
    custom_32 :str = "custom-32" 
    custom_33 :str = "custom-33" 
    custom_34 :str = "custom-34" 
    custom_35 :str = "custom-35" 
    custom_36 :str = "custom-36" 
    custom_37 :str = "custom-37" 
    custom_38 :str = "custom-38" 
    custom_39 :str = "custom-39" 
    custom_40 :str = "custom-40" 
    custom_41 :str = "custom-41" 
    custom_42 :str = "custom-42" 
    custom_43 :str = "custom-43" 
    custom_44 :str = "custom-44" 
    custom_45 :str = "custom-45" 
    custom_46 :str = "custom-46" 
    custom_47 :str = "custom-47" 
    custom_48 :str = "custom-48" 
    custom_49 :str = "custom-49" 
    custom_50 :str = "custom-50"

class SoftwareAxes:
    """
        SoftwareAxes:
        =============
        Summary:
        --------
        Static class that lists
        all the possible software
        axes that drivers and
        your application can access.

        Attention:
        ----------
        DO NOT OVERWRITE THE VALUES STORED
        IN THIS FUCKING CLASS ALRIGHT?
    """
    left       : str = "left"   
    right      : str = "right"
    up         : str = "up"
    down       : str = "down"
    forward    : str = "forward"
    backward   : str = "backward"
    pitch_up   : str = "pitch-up"
    pitch_down : str = "pitch-down"
    roll_left  : str = "roll-left"
    roll_right : str = "roll-right"
    yaw_left   : str = "yaw-left"
    yaw_right  : str = "yaw-right"
    custom_1   : str = "custom-1"
    custom_2   : str = "custom-2"
    custom_3   : str = "custom-3"
    custom_4   : str = "custom-4"
    custom_5   : str = "custom-5"
    custom_6   : str = "custom-6"
    custom_7   : str = "custom-7"
    custom_8   : str = "custom-8"
#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("Controls")
class Controls:
    #region   --------------------------- DOCSTRING
    """
        Controls:
        =========
        Summary:
        --------
        Class used throughout your application
        to directly get inputs of variosu plugged
        devices as long as they have direct BRS supports.
        This class is used in asynchronous threads
        and is thus constantly updated if certain
        things are initialized.

        Attention:
        ----------
        - BRS Device Drivers may read from this class.
        - BrSpand cards may read and write in this class
        - Drivers may write asynchronously in separated threads in this class.
        
        Reading is prioritised over writing.
    """
    #endregion
    #region   --------------------------- MEMBERS
    _initialized:bool = False
    """
        _initialized:
        =============
        Summary:
        --------
        Private member used by
        methods to see if they
        are called from an object
        or a random ass static
        class. Also used to
        avoid
        constant re-initialisation
        of this class by drivers.
    """

    _axes = {
        "left"          : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "right"         : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "up"            : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "down"          : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "forward"       : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "backward"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "pitch-up"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "pitch-down"    : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "roll-left"     : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "roll-right"    : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "yaw-left"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "yaw-right"     : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-1"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-2"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-3"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-4"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-5"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-6"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-7"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-8"      : {"value":0, "binded":False, "bindedTo":None, "bindedAs": None, "getter":None},
    }
    """
        _axes:
        ======
        Summary:
        --------
        Private member which holds each
        axis values as 2 seperated values.
        They are held separately instead of being values
        from -1 to 1 to allow analog triggers to perform
        the same as a joystick would.

        Values:
        -------
        - `_axes["name"]["value"]`    Write or read the value ranging from 0 to 1. DONT DO THIS. (Deprecated)
        - `_axes["name"]["binded"]`   See or set this axis to being used.
        - `_axes["name"]["bindedTo"]` Says who writes to this axis.
        - `_axes["name"]["bindedAs"]` Says what hardware axis `bindedTo` binded this axis to.
        - `_axes["name"]["getter"]`   A function with no parameters that returns the value from 0-1 directly from the binded hardware.
        
        Warning:
        --------
        DO NOT MANUALLY USE THIS MEMBER.
        THE CLASS HANDLES THAT FOR YOU.
    """
    # -----------------------------------------------------
    _buttons = {
        # Movements
        "up"        : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "down"      : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "left"      : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "right"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "forward"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "backward"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},

        # Weaponery
        "fire"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "explode"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},

        # UI
        "select"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "cancel"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "confirm"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},

        # Audio and Video
        "mute"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "record"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},

        # App Actions
        "save"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "reset"    : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "refresh"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "quit"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "stop"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "shutdown" : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "edit"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "add"      : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "remove"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "copy"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "paste"    : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "cut"      : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "undo"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "redo"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "print"    : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},

        # Generic actions
        "close"    : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "open"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "fill"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "empty"    : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "like"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "dislike"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "lock"     : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "unlock"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "on"       : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "off"      : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},

        # Custom actions
        "custom-1"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-2"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-3"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-4"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-5"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-6"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-7"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-8"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-9"   : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-10"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-11"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-12"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-13"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-14"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-15"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-16"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-17"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-18"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-19"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-20"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-21"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-22"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-23"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-24"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-25"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-26"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-27"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-28"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-29"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-30"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-31"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-32"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-33"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-34"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-35"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-36"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-37"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-38"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-39"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-40"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-41"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-42"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-43"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-44"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-45"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-46"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-47"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-48"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-49"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
        "custom-50"  : {"state" : False, "mode" : "held", "binded" : False, "bindedTo":None, "bindedAs": None, "getter":None},
    }
    """
        _buttons:
        =========
        Summary:
        --------
        This private member holds the standard BRS actions that any given
        button can do.
    """
    #endregion
    #region   --------------------------- METHODS
    def BindButton(nameOfTheHardwareBinding:str, nameOfSoftwareButton:str, bindedAs:str, GetterFunction) -> Execution:
        """
            bindButton:
            ===========
            Summary:
            --------
            Allows drivers to bind one of their own hardware
            button or switches to one of the many available
            software representation of that button.

            Since a user may want Button1 to perform as ON
            and an other user may want Button2 of an other
            driver to perform as ON as well.

            Arguments:
            ----------
            - `nameOfTheHardwareBinding`: Says which hardware binded that specific button.
            - `nameOfSoftwareButton` : key or action to bind to the hardware representation.
            - `bindedAs` : Says the name of the hardware button that is binded to that.

            Returns:
            --------
            - `Execution.Passed`: Binding was successful
            - `Execution.Failed`: Software button does not exist
            - `Execution.Incompatibility`: Button is already binded.    
        """
        Debug.Start("bindButton")
        Debug.Log(f"Attempting to bind {nameOfTheHardwareBinding}'s {bindedAs} to {nameOfSoftwareButton}...")

        # Does the button exist?
        if(nameOfSoftwareButton not in Controls._buttons):
            Debug.Error(f"{nameOfSoftwareButton} isn't a valid button that can be binded.")
            Debug.End()
            return Execution.Failed

        # Is the button binded already?
        buttonAlreadybinded = Controls._buttons[nameOfSoftwareButton]["binded"]
        whoeverBindedIt = Controls._buttons[nameOfSoftwareButton]["bindedTo"]

        if(buttonAlreadybinded):
            Debug.Error(f"{nameOfSoftwareButton} is already binded to {whoeverBindedIt}")
            Debug.End()
            return Execution.Incompatibility

        # Welp, looks like we can bind the button!
        Controls._buttons[nameOfSoftwareButton]["bindedTo"] = nameOfTheHardwareBinding
        Controls._buttons[nameOfSoftwareButton]["bindedAs"] = bindedAs
        Controls._buttons[nameOfSoftwareButton]["binded"] = True
        Controls._buttons[nameOfSoftwareButton]["getter"] = GetterFunction

        Debug.Log(">>> Success")
        Debug.End()
        return Execution.Passed

    def BindAxis(nameOfTheHardwareBinding:str, nameOfSoftwareAxis:str, bindedAs:str, GetterFunction) -> Execution:
        """
            BindAxis:
            ===========
            Summary:
            --------
            Allows drivers to bind one of their own hardware
            axis to one of the many available
            software representation of that axis.

            Since a user may want left to perform as right
            and an other user may want up of an other
            driver to perform as left as well.

            Arguments:
            ----------
            - `nameOfTheHardwareBinding`: Says which hardware binded that specific button.
            - `nameOfSoftwareAxis` : software axis that will hold the hardware value.
            - `bindedAs` : Says the name of the hardware button that is binded to that.

            Returns:
            --------
            - `Execution.Passed`: Binding was successful
            - `Execution.Failed`: Software button does not exist
            - `Execution.Incompatibility`: Button is already binded.    
        """
        Debug.Start("BindAxis")

        Debug.Log(f"Attempting to bind {nameOfTheHardwareBinding}'s {bindedAs} to {nameOfSoftwareAxis}...")

        # Does the button exist?
        if(nameOfSoftwareAxis not in Controls._axes):
            Debug.Error(f"{nameOfSoftwareAxis} isn't a valid axis that can be binded.")
            Debug.End()
            return Execution.Failed
        
        # Is the button binded already?
        axisAlreadybinded = Controls._axes[nameOfSoftwareAxis]["binded"]
        whoeverBindedIt = Controls._axes[nameOfSoftwareAxis]["bindedTo"]

        if(axisAlreadybinded):
            Debug.Error(f"{nameOfSoftwareAxis} is already binded to {whoeverBindedIt}")
            Debug.End()
            return Execution.Incompatibility
        
        # Welp, looks like we can bind the button!
        Controls._axes[nameOfSoftwareAxis]["bindedTo"] = nameOfTheHardwareBinding
        Controls._axes[nameOfSoftwareAxis]["bindedAs"] = bindedAs
        Controls._axes[nameOfSoftwareAxis]["getter"] = GetterFunction
        Controls._axes[nameOfSoftwareAxis]["binded"] = True

        Debug.Log(">>> Success")
        Debug.End()
        return Execution.Passed

    def UnbindButton(nameOfTheHardwareBinding:str, nameOfSoftwareButton:str):
        """
            UnbindButton:
            ============
            Summary:
            --------
            Function that unbinds a given
            software buttons from the class.

            Arguments:
            ----------
            - `nameOfTheHardwareBinding:str` : Who wants to unbind?
            - `nameOfSoftwareButton:str` : Name of the button that will be unbinded.

            Attention:
            ----------
            The button is only un-binded
            if the :ref:`nameOfTheHardwareBinding`
            passed matches the one currently
            saved under that software button.
        """
        Debug.Start("UnbindButton")

        # Does the button exist?
        if(nameOfSoftwareButton not in Controls._buttons):
            Debug.Error(f"{nameOfSoftwareButton} isn't a valid button that can be un-binded.")
            Debug.End()
            return Execution.Failed

        # Is the button binded?
        binded = Controls._buttons[nameOfSoftwareButton]["binded"]
        whoeverBindedIt = Controls._buttons[nameOfSoftwareButton]["bindedTo"]

        if(not binded):
            Debug.Error(f"{nameOfSoftwareButton} is not binded.")
            Debug.End()
            return Execution.Unecessary

        if(whoeverBindedIt != nameOfTheHardwareBinding):
            Debug.Error(f"{nameOfTheHardwareBinding} cannot un-bind buttons binded to {whoeverBindedIt}")
            Debug.End()
            return Execution.Failed

        Controls._buttons[nameOfSoftwareButton]["bindedTo"] = None
        Controls._buttons[nameOfSoftwareButton]["bindedAs"] = None
        Controls._buttons[nameOfSoftwareButton]["getter"] = None
        Controls._buttons[nameOfSoftwareButton]["state"] = False
        Controls._buttons[nameOfSoftwareButton]["binded"] = False
        Debug.Log(f"{nameOfSoftwareButton} is no longer binded.")
        Debug.End()
        return Execution.Passed

    def UnbindAxis(nameOfTheHardwareBinding:str, nameOfSoftwareAxis:str):
        """
            UnbindAxis:
            ============
            Summary:
            --------
            Function that unbinds a given
            software axis from the class.

            Arguments:
            ----------
            - `nameOfTheHardwareBinding:str` : Who wants to unbind?
            - `nameOfSoftwareAxis:str` : Name of the axis that will be un-binded.

            Attention:
            ----------
            The axis is only un-binded
            if the :ref:`nameOfTheHardwareBinding`
            passed matches the one currently
            saved under that software axis.
        """
        Debug.Start("UnbindAxis")

        # Does the button exist?
        if(nameOfSoftwareAxis not in Controls._axes):
            Debug.Error(f"{nameOfSoftwareAxis} isn't a valid axis that can be un-binded.")
            Debug.End()
            return Execution.Failed

        # Is the button binded?
        binded = Controls._axes[nameOfSoftwareAxis]["binded"]
        whoeverBindedIt = Controls._axes[nameOfSoftwareAxis]["bindedTo"]

        if(not binded):
            Debug.Error(f"{nameOfSoftwareAxis} is not binded.")
            Debug.End()
            return Execution.Unecessary

        if(whoeverBindedIt != nameOfTheHardwareBinding):
            Debug.Error(f"{nameOfTheHardwareBinding} cannot un-bind axis binded to {whoeverBindedIt}")
            Debug.End()
            return Execution.Failed

        Controls._axes[nameOfSoftwareAxis]["bindedTo"] = None
        Controls._axes[nameOfSoftwareAxis]["bindedAs"] = None
        Controls._axes[nameOfSoftwareAxis]["getter"] = None
        Controls._axes[nameOfSoftwareAxis]["state"] = False
        Controls._axes[nameOfSoftwareAxis]["binded"] = False
        Debug.Log(f"{nameOfSoftwareAxis} is no longer binded.")
        Debug.End()
        return Execution.Passed

    def UnbindHardware(nameOfTheHardwareToUnbind) -> Execution:
        """
            UnbindHardware:
            ===============
            Summary:
            --------
            Removes an entire hardware's binded buttons
            and axes from the control class.

            Arguments:
            ----------
            `nameOfTheHardwareToUnbind`: The name of the hardware that will be unbinded from the lists.

            Returns:
            --------
            - `Execution.Passed` : Function ran successfully.
        """
        Debug.Start("UnbindHardware")

        Debug.Log(f"Unbinding {nameOfTheHardwareToUnbind} from axes...")
        for axis in Controls._axes:
            if(Controls._axes[axis]["bindedTo"] == nameOfTheHardwareToUnbind):
                Controls._axes[axis]["bindedTo"] = None
                Controls._axes[axis]["bindedAs"] = None
                Controls._axes[axis]["getter"] = None
                Controls._axes[axis]["binded"] = False
                Controls._axes[axis]["value"] = 0
                Debug.Log(f"{axis} unbinded from {nameOfTheHardwareToUnbind}")

        Debug.Log(f"Unbinding {nameOfTheHardwareToUnbind} from buttons...")
        for button in Controls._buttons:
            if(Controls._buttons[button]["bindedTo"] == nameOfTheHardwareToUnbind):
                Controls._buttons[button]["bindedTo"] = None
                Controls._buttons[button]["bindedAs"] = None
                Controls._buttons[button]["getter"] = None
                Controls._buttons[button]["state"] = False
                Controls._buttons[button]["binded"] = False
                Debug.Log(f"{button} unbinded from {nameOfTheHardwareToUnbind}")

        Debug.End()
        return Execution.Passed
    def GetAxisValue(nameOfTheAxis:str) -> float:
        """
            GetAxisValue:
            =============
            Summary:
            --------
            Returns a value from 0 to 1 of one of
            the many software axes.

            Arguments:
            ----------
            - `nameOfTheAxis` : Software axis to get the value from.

            Returns:
            --------
            - `float` : value from 0 to 1 of the axis
            - `Execution.Crashed` : fatal error when reading.
            - `Execution.Failed` : axis isnt valid.
        """
        Debug.Start("GetAxisValue")

        if(nameOfTheAxis not in Controls._axes):
            Debug.Error(f"Tried to read inexisting axis value: {nameOfTheAxis}")
            Debug.End()
            return Execution.Failed
        
        thisValue = Controls._axes[nameOfTheAxis]["value"]
        thatHardware = Controls._axes[nameOfTheAxis]["bindedTo"]

        Debug.Log(f"{nameOfTheAxis} binded by {thatHardware} is currently {thisValue}")
        Debug.End()
        return thisValue

    def GetButtonState(nameOfTheButton:str) -> bool:
        """
            GetButtonState:
            ===============
            Summary:
            --------
            Returns a state `True` or `False`
            of one of the many software buttons.

            Arguments:
            ----------
            - `nameOfTheButton` : Software button to get the state from.

            Returns:
            --------
            - `float` : value from 0 to 1 of the axis
            - `Execution.Crashed` : fatal error when reading.
            - `Execution.Failed` : axis isnt valid.
        """
        Debug.Start("GetButtonState")

        if(nameOfTheButton not in Controls._buttons):
            Debug.Error(f"Tried to read inexisting axis value: {nameOfTheButton}")
            Debug.End()
            return Execution.Failed
        
        thisState = Controls._buttons[nameOfTheButton]["state"]
        thatHardware = Controls._buttons[nameOfTheButton]["bindedTo"]

        Debug.Log(f"{nameOfTheButton} binded by {thatHardware} is currently {thisState}")
        Debug.End()
        return thisState
    
    def _UpdateAxisValue(hardwareTryingToUpdate:str, axisToUpdate:str, newAxisValue:float) -> Execution:
        """
            _UpdateAxisValue:
            =================
            Summary:
            --------
            This function allows drivers accross your
            application to easily update an axis
            that they binded through `BindAxis`.
            
            The updated values are checked and errors
            will be returned if they are not expected
            or simply don't fit nor exists.

            Arguments:
            ----------
            - `hardwareTryingToUpdate` : string reprenting the name of the hardware that wants to update an axis.
            - `axisToUpdate` : string reprenting the software name of the axis to update
            - `newAxisValue` : Value ranging from 0 to 1 that will be placed in the software axis.

            Returns:
            --------
            - `Execution.Passed` = Value was successfully placed in the software axis.
            - `Execution.Crashed` = try catch catched something fatal preventing axis from being saved
            - `Execution.Failed` = The axis does not exist. or the value is not between 0 and 1
            - `Execution.Incompatibility` = The axis is already binded to an other driver.
        """
        Debug.Start("_UpdateAxisValue")

        if(axisToUpdate not in Controls._axes):
            Debug.Error(f"Failed to update the value of {axisToUpdate} because its not a valid axis.")
            Debug.End()
            return Execution.Failed
        
        hardwareThatBindedTheAxis = Controls._axes[axisToUpdate]["bindedTo"]
        if(hardwareThatBindedTheAxis != hardwareTryingToUpdate):
            Debug.Error(f"{axisToUpdate} is not binded to {hardwareTryingToUpdate}. {hardwareThatBindedTheAxis} binded it already.")
            Debug.End()
            return Execution.Incompatibility
        
        if(newAxisValue > 1 or newAxisValue < 0):
            Debug.Error(f"{hardwareTryingToUpdate} failed to update {axisToUpdate}'s value to {newAxisValue} because its not between 0 and 1")
            Debug.End()
            return Execution.Failed
    
        # Updating the value cuz all the tests above passed
        try:
            Controls._axes[axisToUpdate]["value"] = newAxisValue
            Debug.Log(">>> Success")
            Debug.End()
            return Execution.Passed
        except:
            Debug.Error(f"Crashed when trying to set {newAxisValue} as {axisToUpdate}'s new value.")
            Debug.End()
            return Execution.Crashed
    
    def _UpdateButtonState(hardwareTryingToUpdate:str, buttonToUpdate:str, newButtonState:bool) -> Execution:
        """
            _UpdateButtonState:
            ===================
            Summary:
            --------
            This function allows drivers accross your
            application to easily update a button
            that they binded through `BindButton`.
            
            The updated state is checked and errors
            will be returned if its not expected
            or simply don't fit nor exists.

            Arguments:
            ----------
            - `hardwareTryingToUpdate` : string reprenting the name of the hardware that wants to update an axis.
            - `buttonToUpdate` : string reprenting the software name of the button to update
            - `newButtonState` : boolean that will be placed in the software button.

            Returns:
            --------
            - `Execution.Passed` = State was successfully placed in the software button.
            - `Execution.Crashed` = Try catch catched something fatal preventing button from being saved
            - `Execution.Failed` = The button does not exist. or the state is not true or false
            - `Execution.Incompatibility` = The button is already binded to an other driver.
        """
        Debug.Start("_UpdateButtonState")

        if(buttonToUpdate not in Controls._buttons):
            Debug.Error(f"Failed to update the state of {buttonToUpdate} because its not a valid button.")
            Debug.End()
            return Execution.Failed
        
        hardwareThatBindedTheButton = Controls._buttons[buttonToUpdate]["bindedTo"]
        if(hardwareThatBindedTheButton != hardwareTryingToUpdate):
            Debug.Error(f"{buttonToUpdate} is not binded to {hardwareTryingToUpdate}. {hardwareThatBindedTheButton} binded it already.")
            Debug.End()
            return Execution.Incompatibility
        
        if(newButtonState != True and newButtonState != False):
            Debug.Error(f"{hardwareTryingToUpdate} failed to update {buttonToUpdate}'s state to {newButtonState} because its not True or False")
            Debug.End()
            return Execution.Failed
    
        # Updating the value cuz all the tests above passed
        # try:
        Controls._buttons[buttonToUpdate]["state"] = newButtonState
        Debug.Log(">>> Success")
        Debug.End()
        return Execution.Passed
        # except:
            # Debug.Error(f"Crashed when trying to set {newButtonState} as {buttonToUpdate}'s new state.")
            # Debug.End()
            # return Execution.Crashed
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("controls.py")