#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from typing import TypeVar
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("states.py")
#====================================================================#
# Functions
#====================================================================#
#__StateColorsRef = TypeVar("T", bound="_StatesColor")
#====================================================================#
# Classes
#====================================================================#
class States:
    #region --------------------------- DOCSTRING
    '''
        This class is a reference style class which represents the current state that a device can be in.
        A device can be GUI or hardware.
        You don't have to use this class when defining the state of a device, but it is more convenient than
        memorizing all the numbers associated by heart.
    '''
    #endregion
    #region --------------------------- MEMBERS
    Disabled = 0
    '''To use when you want to disable a device. Meaning it cannot be used at all and events related to it won't occur.'''
    Inactive = 1
    '''To use when a device is not Active. As in it's OFF/Offline'''
    Active = 2
    '''To use when a device is ON. To indicate that your device is operational/active/online ect'''
    Warning = 3
    '''Specifies when there is a potential problem with your device or control.'''
    Error = 4
    '''Specifies when there definitely is a problem with the device or control.'''
    Unavailable = 5
    '''Specifies that the device or control is currently not available for some reasons. Not to confuse with Disabled'''
    Locked = 6
    '''Specifies that the device or control is not disabled and is available but it's locked for some reasons.'''
    Good = 7
    '''Specifies that the device or control is Good/Ok/Checked. Typically for stuff like (ok/cancel) or checkboxes'''
    #endregion
    #region   --------------------------- METHODS
    def Delete(self):
        '''For deleting this class'''
        del self.Disabled
        del self.Inactive
        del self.Active
        del self.Warning
        del self.Error
        del self.Unavailable
        del self.Locked
        del self.Good
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
class _StatesColor(States):
    #region --------------------------- DOCSTRING
    '''
        This class is used to make a class of colors associated with States
    '''
    #endregion
    #region --------------------------- MEMBERS
    Disabled = (105/255., 105/255., 105/255., 1.)
    '''RGBA color when a device's states is Disabled. See States for full definition'''
    Inactive = (170/255., 170/255., 170/255., 1.)
    '''RGBA color when a device's states is Inactive. See States for full definition'''
    Active = (96/255., 241/255., 241/255., 1.)
    '''RGBA color when a device's states is Active. See States for full definition'''
    Warning = (255/255., 237/255., 101/255., 1.)
    '''RGBA color when a device's states is Warning. See States for full definition'''
    Error = (255/255., 77/255., 77/255., 1.)
    '''RGBA color when a device's states is Error. See States for full definition'''
    Unavailable = (221/255., 0., 0., 1.)
    '''RGBA color when a device's states is Unavailable. See States for full definition'''
    Locked = (255/255., 170/255., 105/255., 1.)
    '''RGBA color when a device's states is Locked. See States for full definition'''
    Good = (38/255., 80/255., 38/255., 1.)
    '''RGBA color when a device's states is Good. See States for full definition'''
    #endregion
    #region   --------------------------- METHODS
    def GetColorFrom(self, thatState: int):
        '''
            Allows you to get a color from the list of states
        '''
        state_colors = {
            States.Active:      self.Active,
            States.Disabled:    self.Disabled,
            States.Error:       self.Error,
            States.Inactive:    self.Inactive,
            States.Locked:      self.Locked,
            States.Unavailable: self.Unavailable,
            States.Warning:     self.Warning,
            States.Good:        self.Good
        }

        color = state_colors.get(thatState)
        if color is None:
            raise ValueError("Invalid state: {}".format(thatState))
        return color
    def GetStateFrom(self, thatColor: list):
        '''
            Allows you to get the corresponding state associated with a given color stored in this class
        '''
        colors_state = {
            self.Active:      States.Active,
            self.Disabled:    States.Disabled,
            self.Error:       States.Error,
            self.Inactive:    States.Inactive,
            self.Locked:      States.Locked,
            self.Unavailable: States.Unavailable,
            self.Warning:     States.Warning,
            self.Good:        States.Good
        }
        state = colors_state.get(thatColor)
        if state is None:
            raise ValueError("Invalid color: {}".format(thatColor))
        return state
    def CopyColorsFrom(self, thatStatesColor = None):
        '''Copy a StatesColor's colors in this StatesColor'''
        if(thatStatesColor != None):
            self.Active:      thatStatesColor.Active
            self.Disabled:    thatStatesColor.Disabled
            self.Error:       thatStatesColor.Error
            self.Inactive:    thatStatesColor.Inactive
            self.Locked:      thatStatesColor.Locked
            self.Unavailable: thatStatesColor.Unavailable
            self.Warning:     thatStatesColor.Warning
            self.Good:        thatStatesColor.Good
    def MultiplyColorsBy(self, thisMultiplier:float):
        '''Allows you to darken/brighten all of the class's colors'''

        def Multiply(aList:list):
            aList[0] = aList[0] * thisMultiplier
            aList[1] = aList[1] * thisMultiplier
            aList[2] = aList[2] * thisMultiplier
            return aList

        self.Disabled =     Multiply(self.Disabled)
        self.Inactive =     Multiply(self.Inactive)
        self.Active =       Multiply(self.Active)
        self.Warning =      Multiply(self.Warning)
        self.Error =        Multiply(self.Error)
        self.Unavailable =  Multiply(self.Unavailable)
        self.Locked =       Multiply(self.Locked)
        self.Good =         Multiply(self.Good)

    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self) -> None:
        self.Disabled = [90/255, 90/255, 90/255, 1]
        self.Inactive = [150/255, 150/255, 150/255, 1]
        self.Active = [96/255, 241/255, 241/255, 1]
        self.Warning = [255/255, 237/255, 101/255, 1]
        self.Error = [255/255, 77/255, 77/255, 1]
        self.Unavailable = [221/255, 0, 0, 1]
        self.Locked = [255/255, 170/255, 105/255, 1]
        self.Good = [77/255, 210/255, 77/255, 1]
    #endregion
    pass
class StatesColors:
    #region --------------------------- DOCSTRING
    '''
        This class is refered to when a device needs
        a new color. This class holds Colors associated with states
        for Text, pressed or default values etc.
    '''
    #endregion
    #region --------------------------- MEMBERS
    Default = _StatesColor()
    Pressed = _StatesColor()
    Text    = _StatesColor()
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    Default.MultiplyColorsBy(1)
    Pressed.MultiplyColorsBy(0.5)
    Text.MultiplyColorsBy(0.25)
    #endregion
    pass
#====================================================================#
LoadingLog.End("states.py")