#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#

#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Lists
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class DrawingProperties:
    #region   --------------------------- DOCSTRING
    '''
        This class holds the drawing properties associated with widgets
        that displays a value ranging from a minimum to a maximum
    '''
    #endregion
    #region   --------------------------- MEMBERS
    value   : float = 0
    """Holds the current real represented value of the drawing"""
    min     : float = 0
    """Absolute minimum that the value can reach"""
    middle  : float = 0
    """Considered the middle point between min and max. This is used to offset the 0 of a drawing"""
    max     : float = 0
    """Absolute maximum that the value can reach"""

    startAngle : float = 0
    """Starting angle. (angle when value=min) This is only used in circular drawings"""
    endAngle : float = 360
    """Ending angle. (angle when value=max) This is only used in circular drawings"""

    showTrack : bool = True
    """Enables the filling's background"""
    trackWidth : float = 5
    """The width of the track's (diameter)"""

    showFilling : bool = True
    """Defines if the filling should be displayed"""
    fillingWidth : float = 10
    """The width of the filling above the track (diameter)"""

    trackColor = [0,0,0,0]
    fillingColor = [0,0,0,0]
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass