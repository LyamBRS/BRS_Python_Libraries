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
from BRS.GUI.Utilities.drawings import BRS_ValueWidgetAttributes

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
class PieChartDial(BRS_ValueWidgetAttributes, Widget):
    #region   --------------------------- DOCSTRING
    '''
        This class allows you to create a PieChartDial like widget which represents
        a float value in between a starting angle and an ending angle.
        Use .Property to set the PieChartDial's properties such as end and start angle.
        Do not use Radians.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _use_hint = False
    #endregion
    #region   --------------------------- GET SET
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def GetFillingAngle(self):
        """
            This function returns the end angle of the PieChartDial's filling in degrees
        """
        # [Step 0]: Get properties into local variables
        _max = self.Properties.max
        _min = self.Properties.min
        _value = self.Properties.value

        # [Step 1]: Get filling ratio
        ratio = (_value - _min) / (_max - _min)

        # [Step 2]: Return corresponding angle.
        return (ratio * (_max - _min)) + _min
    # -------------------------------------------
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _AnimatingShapes(self, animation, value, theOtherOne):
        """
            Called when Animations are executed.
            Call which shapes need to be set to new values here.

            See PieChartDial for an example.
        """
        Debug.Start("_AnimatingShapes")

        # [Step 0]: Save private values as actual Widget properties
        self.Properties.value         = self._current_value
        self.Properties.endAngle      = self._current_endAngle
        self.Properties.startAngle    = self._current_startAngle
        self.Properties.fillingWidth  = self._current_fillingWidth
        self.Properties.trackWidth    = self._current_trackWidth
        self.Properties.pos           = (self._current_pos[0], self._current_pos[1])
        self.Properties.size          = (self._current_size[0], self._current_size[1])

        # [Step 1]: Update drawings based on new values
        UpdateEllipse(self.Properties, self, "Track", self.Track)
        UpdateEllipse(self.Properties, self, "Filling", self.Filling)

        # [Step 2]: Update background's positions
        self.rect.pos   = (self._current_pos[0], self._current_pos[1])
        self.rect.size  = (self._current_size[0], self._current_size[1])
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        self.trackColor.rgba   = self._current_trackColor
        self.fillingColor.rgba = self._current_fillingColor
        self.backgroundColor.rgba = self._current_backgroundColor
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 initialState = States.Disabled,
                 trackWidth = 20,
                 fillingWidth = 0,
                 min = 0,
                 max = 100,
                 startAngle = 0,
                 endAngle = 360,
                 **kwargs):
        super(PieChartDial, self).__init__(**kwargs)
        Debug.Start("PieChartDial")
        #region --------------------------- Initial check ups
        self.Properties.size = (self.size[0], self.size[1])
        self.Properties.pos  = (self.pos[0], self.pos[1])
        #endregion
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

        Debug.Log("the maximum is: {}".format(self.Properties.max))
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for PieChartDial widget's background")
            self.backgroundColor = Color(rgba = (StatesColors.Text.GetColorFrom(self._state) if self.Properties.showBackground else (0,0,0,0)))
            self.rect = RoundedRectangle(size=(self.size[0], self.size[1]), pos=(self.pos[0], self.pos[1]))

            Debug.Log("Creating PieChartDial's track")
            self.trackColor = Color(rgba = (StatesColors.Pressed.GetColorFrom(self._state) if self.Properties.showTrack else (0,0,0,0)))
            self.Track = GetEllipse(self.Properties, self, "Track")

            Debug.Log("Creating PieChartDial's filling")
            self.fillingColor = Color(rgba = (StatesColors.Default.GetColorFrom(self._state) if self.Properties.showFilling else (0,0,0,0)))
            self.Filling = GetEllipse(self.Properties, self, "Filling")

            Debug.Log("Binding events to PieChartDial")
            self.bind(pos = self._UpdatePos, size = self._UpdateSize)

        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting PieChartDial's color animation properties")
        # self._current_backgroundColor      = self.Properties.backgroundColor.rgba
        # self._wanted_BackgroundColor= self.Properties.backgroundColor.rgba
        # self._current_fillingColor         = self.Properties.fillingColor.rgba
        # self._wanted_FillingColor   = self.Properties.fillingColor.rgba
        # self._current_trackColor           = self.Properties.trackColor.rgba
        # self._wanted_TrackColor     = self.Properties.trackColor.rgba

        self._current_backgroundColor       = self.backgroundColor.rgba
        self._wanted_BackgroundColor = self.backgroundColor.rgba
        self._current_fillingColor          = self.fillingColor.rgba
        self._wanted_FillingColor    = self.fillingColor.rgba
        self._current_trackColor            = self.trackColor.rgba
        self._wanted_TrackColor      = self.trackColor.rgba

        Debug.Log("Setting PieChartDial's shape animation properties")
        self._current_pos                 = (self.pos[0], self.pos[1])
        self._wanted_Pos           = (self.pos[0], self.pos[1])

        self._current_size                 = (self.size[0], self.size[1])
        self._wanted_Size           = (self.size[0], self.size[1])

        self._current_pos_hint             = (self.pos[0], self.pos[1])
        self._wanted_Pos_hint       = (self.pos[0], self.pos[1])

        self._current_size_hint            = (self.size[0], self.size[1])
        self._wanted_Size_hint      = (self.size[0], self.size[1])

        self._current_value                = self.Properties.value
        self._wanted_Value          = self.Properties.value
        self._current_endAngle             = self.Properties.endAngle
        self._wanted_EndAngle       = self.Properties.endAngle
        self._current_startAngle           = self.Properties.startAngle
        self._wanted_StartAngle     = self.Properties.startAngle
        self._current_fillingWidth         = self.Properties.fillingWidth
        self._current_trackWidth           = self.Properties.trackWidth
        self._wanted_FillingWidth   = self.Properties.fillingWidth
        self._wanted_TrackWidth     = self.Properties.trackWidth


        #endregion
        Debug.End()
    #endregion
    pass