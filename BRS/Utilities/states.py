#====================================================================#
# Imports
#====================================================================#
from signal import raise_signal

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
    #endregion
    #region --------------------------- CONSTRUCTORS
    #endregion
    ###########################################################################################
    class Colors:
        '''Default BRS palette for colors associated with each state'''
        ###########################################################################################
        class Default:
            '''If we use a button as an example, these would be background colors'''
            Disabled = [105/255, 105/255, 105/255, 1]
            ''' ARGB Color that text uses when disabled'''
            Inactive = [170/255, 170/255, 170/255, 1]
            ''' ARGB Color that text uses when Inactive'''
            Active = [96/255, 241/255, 241/255, 1]
            ''' ARGB Color that text uses when Active'''
            Warning = [255/255, 237/255, 101/255, 1]
            ''' ARGB Color that text uses when Warning'''
            Error = [255/255, 77/255, 77/255, 1]
            ''' ARGB Color that text uses when Error'''
            Unavailable = [221/255, 0, 0, 1]
            ''' ARGB Color that text uses when Unavailable'''
            Locked = [255/255, 170/255, 105/255, 1]
            ''' ARGB Color that text uses when Locked'''
            #------------------------------------------------------#
            def GetColor(stateToCheck):
                state_colors = {
                    States.Active: States.Colors.Default.Active,
                    States.Disabled: States.Colors.Default.Disabled,
                    States.Error: States.Colors.Default.Error,
                    States.Inactive: States.Colors.Default.Inactive,
                    States.Locked: States.Colors.Default.Locked,
                    States.Unavailable: States.Colors.Default.Unavailable,
                    States.Warning: States.Colors.Default.Warning,
                }

                color = state_colors.get(stateToCheck)
                if color is None:
                    raise ValueError("Invalid state: {}".format(stateToCheck))
                return color
        ###########################################################################################
        class Pressed: # x/1.2
            '''If we use a button as an example, these would be outline colors'''
            Disabled = [87/255, 87/255, 87/255, 1]
            ''' ARGB Color that text uses when disabled'''
            Inactive = [141/255, 141/255, 141/255, 1]
            ''' ARGB Color that text uses when Inactive'''
            Active = [80/255, 200/255, 200/255, 1]
            ''' ARGB Color that text uses when Active'''
            Warning = [212/255, 197/255, 84/255, 1]
            ''' ARGB Color that text uses when Warning'''
            Error = [212/255, 64/255, 64/255, 1]
            ''' ARGB Color that text uses when Error'''
            Unavailable = [184/255, 0, 0, 1]
            ''' ARGB Color that text uses when Unavailable'''
            Locked = [212/255, 141/255, 87/255, 1]
            ''' ARGB Color that text uses when Locked'''
            #------------------------------------------------------#
            def GetColor(stateToCheck):
                state_colors = {
                    States.Active: States.Colors.Pressed.Active,
                    States.Disabled: States.Colors.Pressed.Disabled,
                    States.Error: States.Colors.Pressed.Error,
                    States.Inactive: States.Colors.Pressed.Inactive,
                    States.Locked: States.Colors.Pressed.Locked,
                    States.Unavailable: States.Colors.Pressed.Unavailable,
                    States.Warning: States.Colors.Pressed.Warning,
                }

                color = state_colors.get(stateToCheck)
                if color is None:
                    raise ValueError("Invalid state: {}".format(stateToCheck))
                return color
        ###########################################################################################
        class Text: # x/2
            '''If we use a button as an example, these would be text colors'''
            Disabled = [52/255, 52/255, 52/255, 1]
            ''' ARGB Color that text uses when disabled'''
            Inactive = [85/255, 85/255, 85/255, 1]
            ''' ARGB Color that text uses when Inactive'''
            Active = [48/255, 120/255, 120/255, 1]
            ''' ARGB Color that text uses when Active'''
            Warning = [127/255, 118/255, 50/255, 1]
            ''' ARGB Color that text uses when Warning'''
            Error = [127/255, 38/255, 38/255, 1]
            ''' ARGB Color that text uses when Error'''
            Unavailable = [110/255, 0, 0, 1]
            ''' ARGB Color that text uses when Unavailable'''
            Locked = [127/255, 85/255, 52/255, 1]
            ''' ARGB Color that text uses when Locked'''
            #------------------------------------------------------#
            def GetColor(stateToCheck):
                state_colors = {
                    States.Active: States.Colors.Text.Active,
                    States.Disabled: States.Colors.Text.Disabled,
                    States.Error: States.Colors.Text.Error,
                    States.Inactive: States.Colors.Text.Inactive,
                    States.Locked: States.Colors.Text.Locked,
                    States.Unavailable: States.Colors.Text.Unavailable,
                    States.Warning: States.Colors.Text.Warning,
                }

                color = state_colors.get(stateToCheck)
                if color is None:
                    raise ValueError("Invalid state: {}".format(stateToCheck))
                return color