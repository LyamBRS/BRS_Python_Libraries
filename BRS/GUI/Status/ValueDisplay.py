#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
import math

from BRS.Utilities.states import States,StatesColors
from BRS.GUI.Utilities.font import Font
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Utilities.drawings import DrawingProperties
from BRS.GUI.Utilities.drawings import GetEllipse
from BRS.GUI.Utilities.drawings import UpdateEllipse

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
class Dial(Widget):
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
    _wantedValue = 0
    _value = 0

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
        # return self.Properties.value

    @Value.setter
    def Value(self, newValue:float) -> None:
        """_summary_
            Sets the value of the Dial. It will automatically
            adjusts itself to be within the Propertie's range
        Args:
            newValue (float): the new value (from min to max)
        """
        # [Step 0]: Save newValue
        self._wantedValue = newValue

        self.animation = Animation(_value = self._wantedValue, duration = 1, t='out_back')
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)

        UpdateEllipse(self.Properties, self, "Track", self.Track)
        UpdateEllipse(self.Properties, self, "Filling", self.Filling)

        # self._UpdateColors(None,None)
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
        """Updates the color based on the widget's State"""
        self.Properties.trackColor.rgba = StatesColors.Pressed.GetColorFrom(self._state)
        self.Properties.fillingColor.rgba = StatesColors.Default.GetColorFrom(self._state)

    def _UpdateShape(self, *args):
        """
            Updates the general shape of the widget.
        """
        Debug.Start()
        Debug.Log("Updating the shape of the Dial")
        #Update the widget's sizes and positions
        self.rect.pos = self.pos
        self.rect.size = self.size

        Debug.Log("Setting angles for tracks and filling")
        UpdateEllipse(self.Properties, self, "Track", self.Track)
        UpdateEllipse(self.Properties, self, "Filling", self.Filling)

        Debug.End()
        Debug.Log("Success")

    def _Animating(self, animation, value, theOtherOne):
        """ Called when Animations are executed """

        self.Properties.value = self._value

        UpdateEllipse(self.Properties, self, "Track", self.Track)
        UpdateEllipse(self.Properties, self, "Filling", self.Filling)
        self.Properties.trackColor.rgba = StatesColors.Pressed.GetColorFrom(self._state)
        self.Properties.fillingColor.rgba = StatesColors.Default.GetColorFrom(self._state)
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, initialState=_state, trackWidth=Properties.trackWidth, fillingWidth=Properties.fillingWidth, min=Properties.min, max=Properties.max, startAngle=Properties.startAngle, endAngle=Properties.endAngle,  **kwargs):
        super(Dial, self).__init__(**kwargs)
        Debug.Start()
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
        Debug.End()
        Debug.Log("Success")
    #endregion
    pass