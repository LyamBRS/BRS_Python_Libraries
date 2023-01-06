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

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
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

    Properties = DrawingProperties()
    #endregion
    #region   --------------------------- GET SET
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def GetFillingAngle(self):
        """This function returns the end angle of the dial's filling in degrees"""
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
        self.Track.color.rgba = StatesColors.Text.GetColorFrom(self._state)
        self.Filling.color.rgba = StatesColors.Default.GetColorFrom(self._state)

    def _UpdateShape(self, *args):
        """Updates the general shape of the widget."""

        #Update the widget's sizes and positions
        self.rect.pos = self.pos
        self.rect.size = self.size

        self.Track.angle_end = self.Properties.endAngle
        self.Track.angle_start = self.Properties.startAngle

        self.Filling.angle_end = self.Properties.endAngle
        self.Filling.angle_start = self.Properties.startAngle

        #Update the track's size and position.
        if(self.Properties.showTrack):
            self.Track.size = self.size
            self.Track.pos = self.pos
            self.Track.ellipse = (self.x, self.y, self.width - self.Properties.trackWidth, self.height - self.Properties.trackWidth)
            self.Track.width = self.Properties.trackWidth

        if(self.Properties.showFilling):
            self.Track.size = self.size
            self.Track.pos = self.pos
            self.Track.ellipse = (self.x, self.y, self.width - self.Properties.trackWidth, self.height - self.Properties.trackWidth)
            self.Track.width = self.Properties.trackWidth
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
        self.Properties.value           = min
        self.Properties.endAngle        = endAngle
        self.Properties.startAngle      = startAngle
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for dial widget's background")
            self.color = Color(rgba = StatesColors.Pressed.GetColorFrom(self._state))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)

            Debug.Log("Creating dial's track")
            if(self.Properties.showTrack == True):
                self.Track = Line(size=self.size, pos=self.pos, ellipse=(self.x, self.y, self.width - self.Properties.trackWidth, self.height - self.Properties.trackWidth), width = self.Properties.trackWidth, angle_end = self.Properties.endAngle, angle_start = self.Properties.startAngle, color = Color(rgba=(StatesColors.Text.GetColorFrom(self._state))))

            Debug.Log("Creating dial's filling")
            if(self.Properties.showFilling == True):
                self.Filling = Line(size=self.size, pos=self.pos, ellipse=(self.x, self.y, self.width - self.Properties.fillingWidth, self.height - self.Properties.fillingWidth), width = self.Properties.fillingWidth, angle_end = self.Properties.endAngle, angle_start = self.Properties.startAngle, color = Color(rgba=(StatesColors.Default.GetColorFrom(self._state))))

            Debug.Log("Binding events to dial")
            self.bind(pos = self._UpdateShape, size = self._UpdateShape)
            self.bind(state = self._UpdateColors)  # bind the state property to the update_color method
        Debug.Log("Success")
        #endregion
        Debug.End()
    #endregion
    pass