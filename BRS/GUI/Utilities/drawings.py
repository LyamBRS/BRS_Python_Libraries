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
from kivy.animation import Animation
#====================================================================#
# Functions
#====================================================================#
def UpdateEllipse(Properties, widget, type:str, ellipse):
    Debug.Start("UpdateEllipse")
    """Updates an already existing Ellipse from DrawingProperties"""

    if(type == "Track"):
        # Debug.Log("\nGetting Track ellipse")
        ellipse.pos  = (widget.pos[0] + Properties.trackWidth/2,
                        widget.pos[1] + Properties.trackWidth/2)
        ellipse.size = (widget.size[0] - Properties.trackWidth,
                        widget.size[1] - Properties.trackWidth)

        ellipse.angle_start = Properties.startAngle
        ellipse.angle_end   = Properties.endAngle

        # Debug.Log("Value = {}".format(Properties.value))
        # Debug.Log("Widget Size: {}".format(widget.size))
        # Debug.Log("Ellipse Size: {}".format(ellipse.size))
        # Debug.Log("Track width: {}".format(Properties.trackWidth))
        # Debug.Log("Max = {}".format(Properties.max))
    else:
        # Debug.Log("\nGetting Filling ellipse")
        ellipse.pos  = (widget.pos[0] + Properties.fillingWidth/2,
                        widget.pos[1] + Properties.fillingWidth/2)
        ellipse.size = (widget.size[0] - Properties.fillingWidth,
                        widget.size[1] - Properties.fillingWidth)

        ratio = (Properties.value - Properties.min) / (Properties.max - Properties.min)
        ellipse.angle_start = Properties.startAngle
        ellipse.angle_end =  ((1-ratio) * (Properties.startAngle - Properties.endAngle)) + Properties.endAngle

        # Debug.Log("Value = {}".format(Properties.value))
        # Debug.Log("Widget Size: {}".format(widget.size))
        # Debug.Log("Ellipse Size: {}".format(ellipse.size))
        # Debug.Log("Filling width: {}".format(Properties.fillingWidth))
        # Debug.Log("Angle end = {}".format(ellipse.angle_end))
        # Debug.Log("max = {}".format(Properties.max))
        # Debug.Log("min = {}".format(Properties.min))
        # Debug.Log("Ratio = {}".format(ratio))

    width   = widget.size[0] - Properties.fillingWidth
    height  = widget.size[1] - Properties.trackWidth

    Debug.End()

def GetEllipse(Properties, widget, type:str):
    # Debug.Start()
    """Draws an ellipse from given values"""

    if(type == "Track"):
        # Debug.Log("Getting Track ellipse")
        ellipseWidth = Properties.trackWidth
        startAngle = Properties.startAngle
        endAngle = Properties.endAngle
        # Debug.Log("Max = {}".format(Properties.max))
        # Debug.Log("Start angle: {}".format(startAngle))
        # Debug.Log("End angle: {}".format(endAngle))
    else:
        # Debug.Log("Getting Filling ellipse")
        ellipseWidth = Properties.fillingWidth
        ratio = (Properties.value - Properties.min) / (Properties.max - Properties.min)
        startAngle = Properties.startAngle
        endAngle =  (ratio * (Properties.max - Properties.min)) + Properties.min
        # Debug.Log("Max = {}".format(Properties.max))
        # Debug.Log("Start angle: {}".format(startAngle))
        # Debug.Log("End angle: {}".format(endAngle))

    position = (widget.pos[0] + ellipseWidth, widget.pos[1] + ellipseWidth)

    width   = widget.size[0] - (Properties.fillingWidth * 2)
    height  = widget.size[1] - (Properties.trackWidth * 2)

    # Debug.End()
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
    #region   --------------------------- DOCSTRING
    '''
        Object containing the main animatable variables of a BRS widget.
        These are automatically used in Build_ classes which
        builds Animation() with needed parameters automatically for you.

        Only set variables you know you'll use and animate to avoid useless
        calculations.

        Use variables starting with "wanted" to define the new value that
        the real variable need to reach.

        bind an on_progress function manually afterwards for either Shape
        animations or Color animations in order to make your widget's real
        variable be equal to this class's variables (the one that don't start
        with wanted).

        To update your widget's position in your binded on_progress Animation:
        self.pos = Animated.pos
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _animated_wantedBackgroundColor         = [0,0,0,0]
    """
        Private variable used to store the wanted primary color of
        the widget. Defaults to [0,0,0,0].

        Only set this before starting your animation.
    """
    _animated_backgroundColor               = [0,0,0,0]
    """
        Private variable used to store the current primary color of
        the widget. Defaults to [0,0,0,0].

        Use this to update the widget's
        real primary color in your Animation binded on_progress function.
    """
    _animated_wantedTrackColor    = [0,0,0,0]
    """
        Private variable used to store the wanted color of the widget's
        Track. Defaults to [0,0,0,0].

        Only set this before starting your animation.
    """
    _animated_trackColor          = [0,0,0,0]
    """
        Private variable used to store the current color of the widget's
        Track. Defaults to [0,0,0,0].

        Use this to update the widget's
        real Track color in your Animation binded on_progress function.
    """
    _animated_wantedFillingColor  = [0,0,0,0]
    """
        Private variable used to store the wanted color of the widget's
        Filling. Defaults to [0,0,0,0].

        Only set this before starting your animation.
    """
    _animated_fillingColor        = [0,0,0,0]
    """
        Private variable used to store the current color of the widget's
        Filling. Defaults to [0,0,0,0].

        Use this to update the widget's
        real filling color in your Animation binded on_progress function.
    """
    _animated_wantedValue         = 0
    """
        Used to Animate the transition between your widget's current
        value and a new value.

        Only set this before starting your animation.
    """
    _animated_value               = 0
    """
        Represents the current value of your widget.

        Use this to set your Widget's real Value variable when
        the Animation's on_progress is called
    """
    _animated_pos                 = (0,0)
    """
        Represents your widget's current position
        (x,y).
        Defaults to (0,0)

        Use this to update the widget's
        real position in your Animation binded on_progress function.
    """
    _animated_wantedPos           = (0,0)
    """
        Represents the wanted new position of your widget.
        Defaults to (0,0)

        Only set this before starting your animation.
    """
    _animated_size                = (0,0)
    """
        Private variable representing your widget's current
        size. (width, height).
        Defaults to (0,0)

        Use this to update the widget's
        real size in your Animation binded on_progress function.
    """
    _animated_wantedSize          = (0,0)
    """
        Private variable which represents the
        new size to animate towards. (width, height)
        Defaults to (0,0)

        Only set this before starting your animation.
    """
    _animated_radius              = 0
    """
        Private variable which represents your widget's real
        radius. Defaults to 0.

        Use this to update the widget's
        real radius in your Animation binded on_progress function.
    """
    _animated_wantedRadius        = 0
    """
        Private variable representing the new radius needed for your
        widget. Defaults to 0.

        Only set this before starting your animation.
    """
    _animated_startAngle          = 0
    """
        Private variable representing your widget's starting angle
        in degrees. Defaults to 0.

        Use this to update the widget's
        real startAngle in your Animation binded on_progress function.
    """
    _animated_wantedStartAngle    = 0
    """
        Private variable representing your widget's new startAngle.
        Defaults to 0.

        Only set this before starting your animation.
    """
    _animated_endAngle            = 0
    """
        Private variable representing your widget's end angle in
        degrees. Defaults to 0.

        Use this to update the widget's
        real endAngle in your Animation binded on_progress function.
    """
    _animated_wantedEndAngle      = 0
    """
        Private variable representing your widget's new startAngle.
        Defaults to 0.

        Only set this before starting your animation.
    """
    #endregion
    #region   --------------------------- METHODS
    def _StartShapeAnimation(self, duration=0.1, transition:str="in_out_cubic"):
        Debug.Start("StartShapeAnimation")
        """
            Call this instead of manually building your widget's
            animation objects each time you need to transition values.
            It will automatically determine which value to put in the
            Animation's constructor and return you an Animation object.

            use the on_progress parameter to pass the function you want
            to bind with the updating of your widget's shapes.

            Will automatically start the animation
        """
        # region --- [Step 0]: Build argument dictionary
        # Debug.Log("Building original arguments for Animation")
        arguments = {
                        "_animated_value"         : self._animated_wantedValue,
                        "_animated_pos"           : self._animated_wantedPos,
                        "_animated_size"          : self._animated_wantedSize,
                        "_animated_radius"        : self._animated_wantedRadius,
                        "_animated_endAngle"      : self._animated_wantedEndAngle,
                        "_animated_startAngle"    : self._animated_wantedStartAngle
                    }

        comparator = {
                        "_animated_value"         : self._animated_value,
                        "_animated_pos"           : self._animated_pos,
                        "_animated_size"          : self._animated_size,
                        "_animated_radius"        : self._animated_radius,
                        "_animated_endAngle"      : self._animated_endAngle,
                        "_animated_startAngle"    : self._animated_startAngle
                    }
        Debug.Log(str(arguments))
        # endregion
        # region --- [Step 1]: Pop arguments equal to themselves
        # Debug.Log("Removing unused arguments from argument list...")
        keys_to_remove = []

        for current, wanted in arguments.items():
            Debug.Log("current: {}, wanted:{}".format(current,wanted))
            if arguments[current] == comparator[current]:
                keys_to_remove.append(current)

        for key in keys_to_remove:
            arguments.pop(key)

        # Add duration and transition
        arguments["d"] = duration
        arguments["t"] = transition
        # Debug.Log("Success")
        # endregion
        # region --- [Step 2]: Build and return the Animation to execute
        Debug.Log(str(arguments))
        animation = Animation(**arguments)
        animation.bind(on_progress = self._AnimatingShapes)
        animation.start(self)
        # endregion
        Debug.End()
        pass
    def _StartColorAnimation(self, duration:float=0.1, transition:str="in_out_cubic"):
        Debug.Start("StartColorAnimation")
        """
            Call this instead of manually building your widget's
            animation objects each time you need to transition values.
            It will automatically determine which value to put in the
            Animation's constructor, bind you an on_progress and start
            the animation for you.

            use the on_progress parameter to pass the function you want
            to bind with the updating of your widget's shapes.

            Will automatically start the animation
        """
        # region --- [Step 0]: Build argument dictionary
        Debug.Log("Building original arguments for Animation")
        arguments = {
                        "_animated_backgroundColor"   : self._animated_wantedBackgroundColor,
                        "_animated_trackColor"        : self._animated_wantedTrackColor,
                        "_animated_fillingColor"      : self._animated_wantedFillingColor,
                    }

        comparator= {
                        "_animated_backgroundColor"   : self._animated_backgroundColor,
                        "_animated_trackColor"        : self._animated_trackColor,
                        "_animated_fillingColor"      : self._animated_fillingColor,
                    }
        # endregion
        # region --- [Step 1]: Pop arguments equal to themselves
        Debug.Log("Removing unused arguments from argument list...")
        keys_to_remove = []

        for current, wanted in arguments.items():
            if arguments[current] == comparator[current]:
                keys_to_remove.append(current)

        for key in keys_to_remove:
            arguments.pop(key)

        # Add duration and transition
        arguments["d"] = duration
        arguments["t"] = transition
        Debug.Log("Success")
        # endregion
        # region --- [Step 2]: Build and return the Animation to execute
        Debug.Log("Generating and launching Animation()")
        animation = Animation(**arguments)
        animation.bind(on_progress = self._AnimatingColors)
        animation.start(self)
        Debug.Log("End of function")
        # endregion
        Debug.End()
        pass
    def _InstantAnimation(self):
        """ Will make all values equal to their wanted equivalent """
        self._animated_backgroundColor = self._animated_wantedBackgroundColor
        self._animated_fillingColor = self._animated_wantedFillingColor
        self._animated_trackColor = self._animated_wantedTrackColor

        self._animated_size = self._animated_wantedSize
        self._animated_pos = self._animated_wantedPos
        self._animated_radius = self._animated_wantedRadius
        self._animated_value = self._animated_wantedValue

        self._animated_endAngle = self._animated_wantedEndAngle
        self._animated_startAngle = self._animated_wantedStartAngle
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass