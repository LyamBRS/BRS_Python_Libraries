#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from BRS.Debug.consoleLog import Debug
from BRS.Utilities.states import States,StatesColors
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
        ellipse.pos  = (Properties.pos[0] + Properties.trackWidth/2,
                        Properties.pos[1] + Properties.trackWidth/2)
        ellipse.size = (Properties.size[0] - Properties.trackWidth,
                        Properties.size[1] - Properties.trackWidth)

        ellipse.angle_start = Properties.startAngle
        ellipse.angle_end   = Properties.endAngle

        # Debug.Log("Value = {}".format(Properties.value))
        # Debug.Log("Widget Size: {}".format(widget.size))
        # Debug.Log("Ellipse Size: {}".format(ellipse.size))
        # Debug.Log("Track width: {}".format(Properties.trackWidth))
        # Debug.Log("Max = {}".format(Properties.max))
    else:
        # Debug.Log("\nGetting Filling ellipse")
        ellipse.pos  = (Properties.pos[0] + Properties.fillingWidth/2,
                        Properties.pos[1] + Properties.fillingWidth/2)
        ellipse.size = (Properties.size[0] - Properties.fillingWidth,
                        Properties.size[1] - Properties.fillingWidth)

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

    position = (Properties.pos[0] + ellipseWidth, Properties.pos[1] + ellipseWidth)

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
    """Enables the tracks's background"""
    trackWidth : float = 10
    """The width of the track's (diameter)"""

    showFilling : bool = True
    """Defines if the filling should be displayed"""
    fillingWidth : float = 5
    """The width of the filling above the track (diameter)"""

    showBackground : bool = True
    """ Defines wether the background of the widget should be shown or not. Defaults to False """

    trackColor = [0,0,0,0]
    """The current track color. The track is underneath the filling. """
    fillingColor = [0,0,0,0]
    """The current filling color. The filling is shown above the track and represents the displayed value"""
    backgroundColor = [0,0,0,0]
    """The widget's background color defined by it's boundaries. Defaults to [0,0,0,0]"""

    pos = (0,0)
    """ The widgets position property. Do not use the widget's actual position as it sets itself when inside of layouts
        Defaults to 0,0
    """
    size = (100,100)
    """ The widgets size property. Do not use the widget's actual size as it sets itself when inside of layouts
        Defaults to 100,100
    """
    #endregion
    #region   --------------------------- METHODS
    def TestValue(self, valueToTest) -> float:
        """
            This function allows you to do a quick verification of your
            DrawingProperties. if some members of this class get weird
            data, they'll be automatically capped by this function.

            returns the corrected value
        """
        result = True

        # Check Value
        if(valueToTest > self.max):
            return self.max

        if(valueToTest < self.min):
            return self.min

        return valueToTest
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
    animated : bool = False
    """
        Decides wether smooth animations will be used or if values
        should be set instantaneously to their wanted values.

        True = Use smooth animations
        False = Instantaneously set to wanted values
    """
    _animation_duration = 0.1
    """
        The animation's duration in seconds
    """

    _wanted_BackgroundColor     = [0,0,0,0]
    """
        Private variable used to store the wanted primary color of
        the widget. Defaults to [0,0,0,0].

        Only set this before starting your animation.
    """
    _current_backgroundColor    = [0,0,0,0]
    """
        Private variable used to store the current primary color of
        the widget. Defaults to [0,0,0,0].

        Use this to update the widget's
        real primary color in your Animation binded on_progress function.
    """
    _wanted_TrackColor          = [0,0,0,0]
    """
        Private variable used to store the wanted color of the widget's
        Track. Defaults to [0,0,0,0].

        Only set this before starting your animation.
    """
    _current_trackColor         = [0,0,0,0]
    """
        Private variable used to store the current color of the widget's
        Track. Defaults to [0,0,0,0].

        Use this to update the widget's
        real Track color in your Animation binded on_progress function.
    """
    _wanted_FillingColor        = [0,0,0,0]
    """
        Private variable used to store the wanted color of the widget's
        Filling. Defaults to [0,0,0,0].

        Only set this before starting your animation.
    """
    _current_fillingColor       = [0,0,0,0]
    """
        Private variable used to store the current color of the widget's
        Filling. Defaults to [0,0,0,0].

        Use this to update the widget's
        real filling color in your Animation binded on_progress function.
    """
    _wanted_Value               = 0
    """
        Used to Animate the transition between your widget's current
        value and a new value.

        Only set this before starting your animation.
    """
    _current_value              = 0
    """
        Represents the current value of your widget.

        Use this to set your Widget's real Value variable when
        the Animation's on_progress is called
    """
    _current_pos                = (0,0)
    """
        Represents your widget's current position
        (x,y).
        Defaults to (0,0)

        Use this to update the widget's
        real position in your Animation binded on_progress function.
    """
    _wanted_Pos                 = (0,0)
    """
        Represents the wanted new position of your widget.
        Defaults to (0,0)

        Only set this before starting your animation.
    """
    _current_size               = (0,0)
    """
        Private variable representing your widget's current
        size. (width, height).
        Defaults to (0,0)

        Use this to update the widget's
        real size in your Animation binded on_progress function.
    """
    _wanted_Size                = (0,0)
    """
        Private variable which represents the
        new size to animate towards. (width, height)
        Defaults to (0,0)

        Only set this before starting your animation.
    """
    _current_radius             = 0
    """
        Private variable which represents your widget's real
        radius. Defaults to 0.

        Use this to update the widget's
        real radius in your Animation binded on_progress function.
    """
    _wanted_Radius              = 0
    """
        Private variable representing the new radius needed for your
        widget. Defaults to 0.

        Only set this before starting your animation.
    """
    _current_startAngle         = 0
    """
        Private variable representing your widget's starting angle
        in degrees. Defaults to 0.

        Use this to update the widget's
        real startAngle in your Animation binded on_progress function.
    """
    _wanted_StartAngle          = 0
    """
        Private variable representing your widget's new startAngle.
        Defaults to 0.

        Only set this before starting your animation.
    """
    _current_endAngle           = 0
    """
        Private variable representing your widget's end angle in
        degrees. Defaults to 0.

        Use this to update the widget's
        real endAngle in your Animation binded on_progress function.
    """
    _wanted_EndAngle            = 0
    """
        Private variable representing your widget's new startAngle.
        Defaults to 0.

        Only set this before starting your animation.
    """
    _current_fillingWidth       = 0
    """
        Private variable specifying the current width of the
        widget's filling. Defaults to 0.

        Set this before calling the Animation starter.
    """
    _wanted_FillingWidth        = 0
    """
        Private variable representing your widget's new Filling width.
        Defaults to 0

        Only set this before starting your animation.
    """
    _current_trackWidth         = 0
    """
        Private variable specifying the current width of the
        widget's track. Defaults to 0.

        Set this before calling the Animation starter.
    """
    _wanted_TrackWidth          = 0
    """
        Private variable representing your widget's new Track width.
        Defaults to 0

        Only set this before starting your animation.
    """
    _current_pos_hint           = (0,0)
    """
        Represents your widget's current position
        (x,y).
        Defaults to (0,0)

        Use this to update the widget's
        real position in your Animation binded on_progress function.
    """
    _wanted_Pos_hint            = (0,0)
    """
        Represents the wanted new position of your widget.
        Defaults to (0,0)

        Only set this before starting your animation.
    """
    _wanted_Size_hint           = (0,0)
    """
        Private variable which represents the
        new size to animate towards. (width, height)
        Defaults to (0,0)

        Only set this before starting your animation.
    """
    #endregion
    #region   --------------------------- METHODS
    def _StartShapeAnimation(self, duration:float=0.1, transition:str="in_out_cubic"):
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
        Debug.Log("Building original arguments for Animation")
        arguments = {
                        "_current_value"         : self._wanted_Value,
                        "_current_pos"           : self._wanted_Pos,
                        "_current_size"          : self._wanted_Size,
                        "_current_pos_hint"      : self._wanted_Pos_hint,
                        "_current_size_hint"     : self._wanted_Size_hint,
                        "_current_radius"        : self._wanted_Radius,
                        "_current_endAngle"      : self._wanted_EndAngle,
                        "_current_startAngle"    : self._wanted_StartAngle,
                        "_current_fillingWidth"  : self._wanted_FillingWidth,
                        "_current_trackWidth"    : self._wanted_TrackWidth
                    }

        comparator = {
                        "_current_value"         : self._current_value,
                        "_current_pos"           : self._current_pos,
                        "_current_size"          : self._current_size,
                        "_current_pos_hint"      : self._current_pos_hint,
                        "_current_size_hint"     : self._current_size_hint,
                        "_current_radius"        : self._current_radius,
                        "_current_endAngle"      : self._current_endAngle,
                        "_current_startAngle"    : self._current_startAngle,
                        "_current_fillingWidth"  : self._current_fillingWidth,
                        "_current_trackWidth"    : self._current_trackWidth
                    }

        Debug.Log("Arguments before pop: {}".format(arguments))
        Debug.Log("comparator before pop: {}".format(comparator))
        # endregion
        # region --- [Step 1]: Pop arguments equal to themselves
        Debug.Log("Removing unused arguments from argument list...")
        keys_to_remove = []

        for current, wanted in arguments.items():
            if arguments[current] == comparator[current]:
                keys_to_remove.append(current)

        for key in keys_to_remove:
            arguments.pop(key)

        if(len(arguments) == 0):
            Debug.Warn("No animations were made due to no attributes needing change")
            return
        # Add duration and transition
        arguments["d"] = duration
        arguments["t"] = transition
        Debug.Log(str(arguments))
        Debug.Log("Success")
        # endregion
        # region --- [Step 2]: Build and return the Animation to execute
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
                        "_current_backgroundColor"   : self._wanted_BackgroundColor,
                        "_current_trackColor"        : self._wanted_TrackColor,
                        "_current_fillingColor"      : self._wanted_FillingColor,
                    }

        comparator= {
                        "_current_backgroundColor"   : self._current_backgroundColor,
                        "_current_trackColor"        : self._current_trackColor,
                        "_current_fillingColor"      : self._current_fillingColor,
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

        if(len(arguments) == 0):
            Debug.Warn("No animations were made due to no attributes needing change")
            return

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
        Debug.Start("_InstantAnimation")
        self._current_backgroundColor = self._wanted_BackgroundColor
        self._current_fillingColor = self._wanted_FillingColor
        self._current_trackColor = self._wanted_TrackColor

        self._current_size = (self._wanted_Size[0], self._wanted_Size[1])
        self._current_pos  = (self._wanted_Pos[0], self._wanted_Pos[1])
        self._current_size_hint    = (self._wanted_Size_hint[0], self._wanted_Size_hint[1])
        self._current_pos_hint     = (self._wanted_Pos_hint[0], self._wanted_Pos_hint[1])
        self._current_radius = self._wanted_Radius
        self._current_value = self._wanted_Value

        self._current_endAngle = self._wanted_EndAngle
        self._current_startAngle = self._wanted_StartAngle

        self._current_trackWidth = self._wanted_TrackWidth
        self._current_fillingWidth = self._wanted_FillingWidth
        Debug.End()
    def _current_Get(self, type:str, fromTheseProperties:DrawingProperties=None):
        """
            Transfer specified currently stored value of your class's
            DrawingProperties into the Animated class for you if inherited.

            theseProperties = DrawingProperties to copy from.

            copy = from theseProperty, copy ("None","All","Colors","Shapes")
        """
        Debug.Start("_current_Get")
        def Check(thisProperty):
            return (thisProperty != None)

        # [Step 0]: Checking if we are using that drawing property or our own.
        if(fromTheseProperties != None):

            # [Step 1]: Copying Current colors
            if(type == "All" or type == "Colors"):
                if(Check(self.backgroundColor)):
                    self._current_backgroundColor = self.backgroundColor
                self._current_fillingColor = fromTheseProperties.fillingColor
                self._current_trackColor   = fromTheseProperties.trackColor

            # [Step 2]: Copying Current Shapes
            if(type == "All" or type == "Shapes"):
                self._current_endAngle     = fromTheseProperties.endAngle
                self._current_startAngle   = fromTheseProperties.startAngle
                self._current_fillingWidth = fromTheseProperties.fillingWidth
                self._current_trackWidth   = fromTheseProperties.trackWidth
                self._current_value        = fromTheseProperties.value

                if(Check(self.pos)):
                    Debug.Log("Gotten pos: {}".format(self.pos))
                    # self._current_pos = (self.pos[0], self.pos[1])

                if(Check(self.size)):
                    Debug.Log("Gotten size: {}".format(self.size))
                    # self._current_size = (self.size[0], self.size[1])
        Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------
class BRS_ValueWidgetAttributes(Animated):
    #region   --------------------------- DOCSTRING
    '''
        Inherited object containing standard get set
        and functions used in any BRS widgets to avoid
        useless calls.

        Your widgets should inherit this event if not all
        of it is used
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _state : int = States.Disabled
    """
        Internal reference of the widget's state.
        Do not change this value by hand, use the Get
        Set method instead (State).

        Refer to Utilities.States for a list of available
        States that this widget can be set to.
    """
    Properties = DrawingProperties()
    #endregion
    #region   --------------------------- GET SETS
    #region   -- State
    @property
    def State(self) -> int:
        """[GET]
            Returns the State in which the widget is in.
            Refer to Utilities.States for a list of all
            available states
        """
        return self._state

    @State.setter
    def State(self, newState:States) -> None:
        """[SET]:
            Set the State of the widget to ones from the States class.
            This will handle color changing and animations based of the
            new state. Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newState (States): Utilities.States
        """
        #Save new state in private variable
        if(newState != self._state):
            self._state = newState
            self._UpdateColors(None,None)
    #endregion
    #region   -- Value
    @property
    def Value(self) -> int:
        """[GET]:
            Returns the shown value of the widget
        """
        return self.Properties.value

    @Value.setter
    def Value(self, newValue:float) -> None:
        """[SET:]
            Sets the value of the widget. It will automatically
            adjusts itself to be within the Propertie's range.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new value (from min to max).
        """

        # [Step 1]: Update the shape based on the new value
        if(newValue != self.Properties.value):
            self._current_value        = self.Properties.value
            self._wanted_Value  = self.Properties.TestValue(newValue)
            self._UpdateShape()
    #endregion
    #region   -- FillingWidth
    @property
    def FillingWidth(self) -> int:
        """ [GET]:
            Returns the current width of the filling aspect
        """
        return self.Properties.fillingWidth

    @FillingWidth.setter
    def FillingWidth(self, newValue:int) -> None:
        """ [SET]:
            Sets the filling width of the PieChartDial.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new width of the PieChartDial's filling
        """
        Debug.Start("FillingWidth")
        # [Step 1]: Update the shape based on the new value
        if(newValue != self.Properties.fillingWidth):
            self._current_fillingWidth        = self.Properties.fillingWidth
            self._wanted_FillingWidth  = newValue
            self._UpdateShape()
        Debug.End()
    #endregion
    #region   -- TrackWidth
    @property
    def TrackWidth(self) -> int:
        """ [GET]:
            Returns the current width of the track aspect
        """
        return self.Properties.trackWidth

    @TrackWidth.setter
    def TrackWidth(self, newValue:int) -> None:
        """ [SET]:
            Sets the Track width of the widget.
            The track is drawn below the Filling.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new width of the widget's track
        """
        Debug.Start("TrackWidth")
        # [Step 1]: Update the shape based on the new value
        if(newValue != self.Properties.trackWidth):
            self._wanted_TrackWidth  = newValue
            self._UpdateShape()
        Debug.End()
    #endregion
    #region   -- Size
    @property
    def Size(self) -> list:
        """ [GET]:
            Returns the current Size of the widget
        """
        return self.size

    @Size.setter
    def Size(self, newValue:list) -> None:
        """ [SET]:
            Sets the Size of the widget.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new size of the widget
        """
        Debug.Start("Size")
        # [Step 0]: Save newValue
        self._wanted_Size = (newValue[0], newValue[1])

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape()
        Debug.End()
    #endregion
    #region   -- Pos
    @property
    def Pos(self) -> list:
        """ [GET]:
        Returns the current position of the widget (x,y)
        """
        return self.pos

    @Pos.setter
    def Pos(self, newValue:list) -> None:
        """ [SET]:
            Sets the position of the widget.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new position of the widget (x,y)
        """
        Debug.Start("Pos")
        # [Step 0]: Save newValue
        self._wanted_Pos = (newValue[0], newValue[1])

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape()
        Debug.End()
    #endregion
    #region   -- ShowTrack
    @property
    def ShowTrack(self) -> bool:
        """ [GET]:
            Returns wether the track is shown or not 
        """
        return self.Properties.showTrack

    @ShowTrack.setter
    def ShowTrack(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the track is shown or not.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (bool): the new showing or not
        """
        Debug.Start("ShowTrack")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self.Properties.showTrack):
            self.Properties.showTrack = newValue
            self._UpdateColors(None,None)
        Debug.End()
    #endregion
    #region   -- ShowFilling
    @property
    def ShowFilling(self) -> bool:
        """ [GET]:
        Returns wether the filling is shown or not
        """
        return self.Properties.showFilling

    @ShowFilling.setter
    def ShowFilling(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the filling is shown or not
        Args:
            newValue (bool): the new showing or not
        """
        Debug.Start("ShowFilling")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self.Properties.showFilling):
            self.Properties.showFilling = newValue
            self._UpdateColors(None,None)
        Debug.End()
    #endregion
    #region   -- ShowBackground
    @property
    def ShowBackground(self) -> bool:
        """ [GET]:
        Returns wether the background is shown or not
        """
        return self.Properties.showBackground

    @ShowBackground.setter
    def ShowBackground(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the background is shown or not
        Args:
            newValue (bool): the new showing or not
        """
        Debug.Start("ShowBackground")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self.Properties.showBackground):
            self.Properties.showBackground = newValue
            self._UpdateColors(None,None)
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def SetAttributes(self,
                        TrackWidth = None,
                        FillingWidth = None,
                        position = None,
                        size = None,
                        endAngle = None,
                        startAngle = None,
                        value = None,
                        showTrack = None,
                        showBackground = None,
                        showFilling = None):
        """
            Allows you to set multiple properties at once instead of creating an animation for each one you change.
            This will only call UpdateShapes Once.
        """

        # [Step 0]: Set wanted animation goals
        self._wanted_FillingWidth = self._current_fillingWidth if (FillingWidth == None)   else FillingWidth
        self._wanted_TrackWidth   = self._current_trackWidth   if (TrackWidth == None)     else TrackWidth
        self._wanted_StartAngle   = self._current_startAngle   if (startAngle == None)     else startAngle
        self._wanted_EndAngle     = self._current_endAngle     if (endAngle == None)       else endAngle
        self._wanted_Value        = self._current_value        if (value == None)          else self.Properties.TestValue(value)
        self._wanted_Pos          = (self._wanted_Pos[0],self._wanted_Pos[1]) if (position == None) else (position[0],position[1])
        self._wanted_Size         = (self._wanted_Size[0],self._wanted_Size[1]) if (size == None) else (size[0],size[1])

        self.Properties.showFilling     = self.Properties.showFilling       if (showFilling == None)    else showFilling
        self.Properties.showTrack       = self.Properties.showTrack         if (showTrack == None)      else showTrack
        self.Properties.showBackground  = self.Properties.showBackground    if (showBackground == None) else showBackground

        self._UpdateShape()
    # ------------------------------------------------------
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        self._wanted_FillingColor    = StatesColors.Default.GetColorFrom(self._state) if self.Properties.showFilling    else (0,0,0,0)
        self._wanted_TrackColor      = StatesColors.Pressed.GetColorFrom(self._state) if self.Properties.showTrack      else (0,0,0,0)
        self._wanted_BackgroundColor = StatesColors.Text.GetColorFrom(self._state)    if self.Properties.showBackground else (0,0,0,0)

        # [Step 2]: Start animation
        # Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        Debug.End()
        Debug.End()
    # ------------------------------------------------------
    def _UpdatePos(self, *args):
        """
            Called when the pos property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (x,y)]
        """
        Debug.Start("[PieChartDial]: _UpdatePos")
        self._wanted_Pos = (args[1][0], args[1][1])
        self._UpdateShape()
        Debug.End()
    # ------------------------------------------------------
    def _UpdateSize(self, *args):
        """
            Called when the size property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (width,height)]
        """
        Debug.Start("[PieChartDial]: _UpdateSize")
        self._wanted_Size = (args[1][0], args[1][1])
        self._UpdateShape()
        Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self):
        """
            Function called to setup the Animations and variables
            needed to update the widget's shape.

            Do not call this function outside of this widget
        """
        Debug.Start("_UpdateShape")
        # [Step 0]: Getting valus from widget properties
        self._current_Get("Shapes", fromTheseProperties = self.Properties)

        # [Step 1]: Checking if widget should have animations or not
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass