#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from BRS.Utilities.states import States,StatesColors
from BRS.GUI.Utilities.font import Font
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Utilities.drawings import DrawingProperties
from BRS.GUI.Utilities.drawings import GetEllipse
from BRS.GUI.Utilities.drawings import UpdateEllipse
from BRS.GUI.Utilities.drawings import Animated

from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import RoundedRectangle
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.graphics import Ellipse
from kivy.event import EventDispatcher
from kivy.uix.label import Label
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Dial(Animated, Widget):
    #region   --------------------------- DOCSTRING
    '''
        This class allows you to create a Dial like widget which represents
        a float value in between a starting angle and an ending angle.
        Use .Property to set the dial's properties such as end and start angle.
        Do not use Radians.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _state = States.Disabled
    animated : bool = False
    Properties = DrawingProperties()
    #endregion
    #region   --------------------------- GET SET
    #region   -- State
    @property
    def State(self) -> int:
        """ Returns the State in which the widget is in """
        return self._state

    @State.setter
    def State(self, newState:States) -> None:
        """_summary_
            Set the State of the widget to ones from the States class.
            This will handle color changing and animations based of the new state
        Args:
            newState (States): _description_
        """
        #Save new state in private variable
        self._state = newState
        self._UpdateColors(None,None)
    #endregion
    #region   -- Value
    @property
    def Value(self) -> int:
        """ Returns the State in which the widget is in """
        return self.Properties.value

    @Value.setter
    def Value(self, newValue:float) -> None:
        """_summary_
            Sets the value of the Dial. It will automatically
            adjusts itself to be within the Propertie's range
        Args:
            newValue (float): the new value (from min to max)
        """

        # [Step 0]: Save newValue
        self._animated_value        = self.Properties.value
        self._animated_wantedValue  = newValue

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape(None)
    #endregion
    #region   -- FillingWidth
    @property
    def FillingWidth(self) -> int:
        """ Returns the current width of the filling aspect """
        return self.Properties.fillingWidth

    @FillingWidth.setter
    def FillingWidth(self, newValue:int) -> None:
        """_summary_
            Sets the filling width of the dial.
        Args:
            newValue (float): the new width of the dial's filling
        """
        Debug.Start("FillingWidth")
        # [Step 0]: Save newValue
        self._animated_fillingWidth        = self.Properties.fillingWidth
        self._animated_wantedFillingWidth  = newValue

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape(None)
        Debug.End()
    #endregion
    #region   -- TrackWidth
    @property
    def TrackWidth(self) -> int:
        """ Returns the current width of the filling aspect """
        return self.Properties.fillingWidth

    @TrackWidth.setter
    def TrackWidth(self, newValue:int) -> None:
        """_summary_
            Sets the Track width of the dial.
        Args:
            newValue (float): the new width of the dial's track
        """
        Debug.Start("TrackWidth")
        # [Step 0]: Save newValue
        self._animated_wantedTrackWidth  = newValue

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape(None)
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def GetFillingAngle(self):
        """
            This function returns the end angle of the dial's filling in degrees
        """
        # [Step 0]: Get properties into local variables
        _max = self.Properties.max
        _min = self.Properties.min
        _value = self.Properties.value

        # [Step 1]: Get filling ratio
        ratio = (_value - _min) / (_max - _min)

        # [Step 2]: Return corresponding angle.
        return (ratio * (_max - _min)) + _min

    #endregion
    #region   -- Private
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        # Debug.Log("[Step 0]:")
        self._animated_wantedFillingColor   = StatesColors.Default.GetColorFrom(self._state)
        self._animated_wantedTrackColor     = StatesColors.Pressed.GetColorFrom(self._state)
        self._animated_wantedBackgroundColor= StatesColors.Text.GetColorFrom(self._state)

        # [Step 1]: Set animation's current values
        # Debug.Log("[Step 1]:")
        self._animated_fillingColor     = self.Properties.fillingColor.rgba
        self._animated_trackColor       = self.Properties.trackColor.rgba
        self._animated_backgroundColor  = self.backgroundColor.rgba

        # [Step 2]: Start animation
        # Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self, *args):
        """
            Updates the general shape of the widget.
        """
        Debug.Start("_UpdateShape")
        # Debug.Log("Updating the shape of the Dial")

        # Debug.Log("Setting animation parameters")
        self._Animated_Get("Shapes", fromTheseProperties = self.Properties)

        self._animated_pos = self.rect.pos
        self._animated_size = self.rect.size

        # Debug.Log("Set wanteds")
        self._animated_wantedPos = self.pos
        self._animated_wantedSize = self.size

        # Debug.Log("Launching shape animator")
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingShapes(self, animation, value, theOtherOne):
        """ Called when Animations are executed """
        Debug.Start("_AnimatingShapes")
        # [Step 0]: Save private values as actual values
        # Debug.Log("Value : {}".format(self.Animating.value))
        self.Properties.value         = self._animated_value
        self.Properties.endAngle      = self._animated_endAngle
        self.Properties.startAngle    = self._animated_startAngle
        self.Properties.fillingWidth  = self._animated_fillingWidth
        self.Properties.trackWidth    = self._animated_trackWidth

        # [Step 1]: Update drawings based on new values
        # Debug.Log("[Step 1]")
        UpdateEllipse(self.Properties, self, "Track", self.Track)
        UpdateEllipse(self.Properties, self, "Filling", self.Filling)

        # [Step 2]: Update background's positions
        # Debug.Log("[Step 2]")
        self.rect.pos   = self._animated_pos
        self.rect.size  = self._animated_size
        Debug.End()

    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")
        # [Step 0]: Save private values as actual values
        self.Properties.trackColor.rgba   = self._animated_trackColor
        self.Properties.fillingColor.rgba = self._animated_fillingColor
        self.backgroundColor.rgba         = self._animated_backgroundColor
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, initialState=_state, trackWidth=Properties.trackWidth, fillingWidth=Properties.fillingWidth, min=Properties.min, max=Properties.max, startAngle=Properties.startAngle, endAngle=Properties.endAngle,  **kwargs):
        super(Dial, self).__init__(**kwargs)
        Debug.Start("Dial")
        #region --------------------------- Set Variables
        Debug.Log("Setting internal variables to new specified values")
        self._state = initialState

        self.Properties.fillingWidth    = fillingWidth
        self.Properties.trackWidth      = trackWidth
        self.Properties.max             = max
        self.Properties.min             = min
        self.Properties.value           = 50
        self.Properties.endAngle        = endAngle
        self.Properties.startAngle      = startAngle

        self._value = self.Properties.value
        self._wantedValue = self.Properties.value

        Debug.Log("the maximum is: {}".format(self.Properties.max))
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for dial widget's background")
            self.backgroundColor = Color(rgba = (1,1,1,1))#Color(rgba = StatesColors.Text.GetColorFrom(self._state))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)

            Debug.Log("Creating dial's track")
            if(self.Properties.showTrack == True):
                self.Properties.trackColor = Color(rgba = StatesColors.Pressed.GetColorFrom(self._state))
                # self.Track = Line(pos=self.pos, ellipse=(self.x, self.y, self.width - self.Properties.trackWidth, self.height - self.Properties.trackWidth), width = self.Properties.trackWidth, angle_end = self.Properties.endAngle, angle_start = self.Properties.startAngle)
                self.Track = GetEllipse(self.Properties, self, "Track")

            Debug.Log("Creating dial's filling")
            if(self.Properties.showFilling == True):
                self.Properties.fillingColor = Color(rgba = StatesColors.Default.GetColorFrom(self._state))
                # self.Filling = Line(pos=self.pos, ellipse=(self.x, self.y, self.width - self.Properties.fillingWidth, self.height - self.Properties.fillingWidth), width = self.Properties.fillingWidth, angle_end = self.Properties.endAngle/2, angle_start = self.Properties.startAngle)
                self.Filling = GetEllipse(self.Properties, self, "Filling")

            Debug.Log("Binding events to dial")
            self.bind(pos = self._UpdateShape, size = self._UpdateShape)
            # self.bind(_state = self._UpdateColors)  # bind the state property to the update_color method
        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting dial's color animation properties")
        self._animated_backgroundColor      = self.backgroundColor.rgba
        self._animated_wantedBackgroundColor= self.backgroundColor.rgba
        self._animated_fillingColor         = self.Properties.fillingColor.rgba
        self._animated_wantedFillingColor   = self.Properties.fillingColor.rgba
        self._animated_trackColor           = self.Properties.trackColor.rgba
        self._animated_wantedTrackColor     = self.Properties.trackColor.rgba

        Debug.Log("Setting dial's shape animation properties")
        self._animated_pos              = self.pos
        self._animated_pos              = self.pos
        self._animated_size             = self.size
        self._animated_wantedSize       = self.size
        self._animated_value            = self.Properties.value
        self._animated_wantedValue      = self.Properties.value
        self._animated_endAngle         = self.Properties.endAngle
        self._animated_wantedEndAngle   = self.Properties.endAngle
        self._animated_startAngle       = self.Properties.startAngle
        self._animated_wantedStartAngle = self.Properties.startAngle
        self._animated_fillingWidth         = self.Properties.fillingWidth
        self._animated_trackWidth           = self.Properties.trackWidth
        self._animated_wantedFillingWidth   = self.Properties.fillingWidth
        self._animated_wantedTrackWidth     = self.Properties.trackWidth

        #endregion
        Debug.End()
    #endregion
    pass