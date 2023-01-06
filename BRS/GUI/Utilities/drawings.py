#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
import math
from BRS.Debug.consoleLog import Debug
from kivy.clock import Clock
from kivy.graphics import Ellipse
from kivy.graphics import Line
#====================================================================#
# Functions
#====================================================================#
def UpdateEllipse(Properties, widget, type:str, ellipse):
    Debug.Start()
    """Draws an ellipse from given values"""

    if(type == "Track"):
        Debug.Log("\nGetting Track ellipse")
        ellipse.pos  = (widget.pos[0] + Properties.trackWidth/2,
                        widget.pos[1] + Properties.trackWidth/2)
        ellipse.size = (widget.size[0] - Properties.trackWidth,
                        widget.size[1] - Properties.trackWidth)

        ellipse.angle_start = Properties.startAngle
        ellipse.angle_end   = Properties.endAngle

        Debug.Log("Value = {}".format(Properties.value))
        Debug.Log("Widget Size: {}".format(widget.size))
        Debug.Log("Ellipse Size: {}".format(ellipse.size))
        Debug.Log("Track width: {}".format(Properties.trackWidth))
        Debug.Log("Max = {}".format(Properties.max))
    else:
        Debug.Log("\nGetting Filling ellipse")
        ellipse.pos  = (widget.pos[0] + Properties.fillingWidth/2,
                        widget.pos[1] + Properties.fillingWidth/2)
        ellipse.size = (widget.size[0] - Properties.fillingWidth,
                        widget.size[1] - Properties.fillingWidth)

        ratio = (Properties.value - Properties.min) / (Properties.max - Properties.min)
        ellipse.angle_start = Properties.startAngle
        ellipse.angle_end =  ((1-ratio) * (Properties.startAngle - Properties.endAngle)) + Properties.endAngle

        Debug.Log("Value = {}".format(Properties.value))
        Debug.Log("Widget Size: {}".format(widget.size))
        Debug.Log("Ellipse Size: {}".format(ellipse.size))
        Debug.Log("Filling width: {}".format(Properties.fillingWidth))
        Debug.Log("Angle end = {}".format(ellipse.angle_end))
        Debug.Log("max = {}".format(Properties.max))
        Debug.Log("min = {}".format(Properties.min))
        Debug.Log("Ratio = {}".format(ratio))

    width   = widget.size[0] - Properties.fillingWidth
    height  = widget.size[1] - Properties.trackWidth

    Debug.End()

def GetEllipse(Properties, widget, type:str):
    Debug.Start()
    """Draws an ellipse from given values"""

    if(type == "Track"):
        Debug.Log("Getting Track ellipse")
        ellipseWidth = Properties.trackWidth
        startAngle = Properties.startAngle
        endAngle = Properties.endAngle
        Debug.Log("Max = {}".format(Properties.max))
        Debug.Log("Start angle: {}".format(startAngle))
        Debug.Log("End angle: {}".format(endAngle))
    else:
        Debug.Log("Getting Filling ellipse")
        ellipseWidth = Properties.fillingWidth
        ratio = (Properties.value - Properties.min) / (Properties.max - Properties.min)
        startAngle = Properties.startAngle
        endAngle =  (ratio * (Properties.max - Properties.min)) + Properties.min
        Debug.Log("Max = {}".format(Properties.max))
        Debug.Log("Start angle: {}".format(startAngle))
        Debug.Log("End angle: {}".format(endAngle))

    position = (widget.pos[0] + ellipseWidth, widget.pos[1] + ellipseWidth)

    width   = widget.size[0] - (Properties.fillingWidth * 2)
    height  = widget.size[1] - (Properties.trackWidth * 2)

    Debug.End()
    return Ellipse(pos = position, size = (width, height), angle_start = startAngle, angle_end = endAngle)
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
    value   : float = 50
    """Holds the current real represented value of the drawing"""
    min     : float = 0
    """Absolute minimum that the value can reach"""
    middle  : float = 0
    """Considered the middle point between min and max. This is used to offset the 0 of a drawing"""
    max     : float = 100
    """Absolute maximum that the value can reach"""

    startAngle : float = 0
    """Starting angle. (angle when value=min) This is only used in circular drawings"""
    endAngle : float = 360
    """Ending angle. (angle when value=max) This is only used in circular drawings"""

    showTrack : bool = True
    """Enables the filling's background"""
    trackWidth : float = 10
    """The width of the track's (diameter)"""

    showFilling : bool = True
    """Defines if the filling should be displayed"""
    fillingWidth : float = 5
    """The width of the filling above the track (diameter)"""

    trackColor = [0,0,0,0]
    """The current track color. The track is underneath the filling. """
    fillingColor = [0,0,0,0]
    """The current filling color. The filling is shown above the track and represents the displayed value"""
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------
class Animated:
    pass