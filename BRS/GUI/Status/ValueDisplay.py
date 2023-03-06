#====================================================================#
# File Information
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("ValueDisplay.py")
#====================================================================#
# Imports
#====================================================================#
import time
from ...Utilities.states import States,StatesColors
from ...GUI.Utilities.font import Font
from ...Debug.consoleLog import Debug
from ...GUI.Utilities.attributes import GetEllipse,GetLine
from ...GUI.Utilities.attributes import UpdateEllipse,UpdateLine
from ...GUI.Utilities.attributes import BRS_ValueWidgetAttributes, BRS_BarGraphWidgetAttributes

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
# PieChartDial
#====================================================================#
class PieChartDial(BRS_ValueWidgetAttributes, Widget):
    #region   --------------------------- DOCSTRING
    '''
        This class allows you to create a PieChartDial like widget which represents
        a float value in between a starting angle and an ending angle.
        Use SetAttributes to set the PieChartDial's properties such as end and start angle.
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
        _max = self._current_max
        _min = self._current_min
        _value = self._current_value

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
        UpdateEllipse(self, "Track", self.Track)
        UpdateEllipse(self, "Filling", self.Filling)

        # [Step 2]: Update background's positions
        self.rect.pos   = (self._current_pos[0], self._current_pos[1])
        self.rect.size  = (self._current_size[0], self._current_size[1])
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        Debug.Log("Color = {}".format(self._current_trackColor))
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
        self.InitAnimations()
        x = self.pos[0]
        y = self.pos[1]
        # self.Properties.size = (self.size[0], self.size[1])
        # self.Properties.pos  = (self.pos[0], self.pos[1])
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

        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for PieChartDial widget's background")
            self.backgroundColor = Color(rgba = (StatesColors.Text.GetColorFrom(self._state) if self._showBackground else (0,0,0,0)))
            self.rect = RoundedRectangle(size=(self.size[0], self.size[1]), pos=(x, y))

            Debug.Log("Creating PieChartDial's track")
            self.trackColor = Color(rgba = (StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack else (0,0,0,0)))
            self.Track = GetEllipse(self, "Track")

            Debug.Log("Creating PieChartDial's filling")
            self.fillingColor = Color(rgba = (StatesColors.Default.GetColorFrom(self._state) if self._showFilling else (0,0,0,0)))
            self.Filling = GetEllipse(self, "Filling")

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
        self._wanted_BackgroundColor        = self.backgroundColor.rgba
        self._current_fillingColor          = self.fillingColor.rgba
        self._wanted_FillingColor           = self.fillingColor.rgba
        self._current_trackColor            = self.trackColor.rgba
        self._wanted_TrackColor             = self.trackColor.rgba

        Debug.Log("Setting PieChartDial's shape animation properties")

        self._current_pos           = (x, y)
        self._wanted_Pos            = (x, y)

        self._current_size          = (x, y)
        self._wanted_Size           = (x, y)

        self._current_pos_hint      = (x, y)
        self._wanted_Pos_hint       = (x, y)

        self._current_size_hint     = (x, y)
        self._wanted_Size_hint      = (x, y)

        # self._current_value         = self.Properties.value
        # self._wanted_Value          = self.Properties.value
        self._current_endAngle      = endAngle
        self._wanted_EndAngle       = endAngle
        self._current_startAngle    = startAngle
        self._wanted_StartAngle     = startAngle
        self._current_fillingWidth  = fillingWidth
        self._current_trackWidth    = trackWidth
        self._wanted_FillingWidth   = fillingWidth
        self._wanted_TrackWidth     = trackWidth


        #endregion
        Debug.End()
    #endregion
    pass
#====================================================================#
# OutlineDial
#====================================================================#
class OutlineDial(BRS_ValueWidgetAttributes, Widget):
    #region   --------------------------- DOCSTRING
    '''
        This class allows you to create a OutlineDial like widget which represents
        a float value in between a starting angle and an ending angle.
        Use SetAttributes to set the OutlineDial's properties such as end and start angle.
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
        _max = self._current_max
        _min = self._current_min
        _value = self._current_value

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
        # Debug.Start("_AnimatingShapes")
        # [Step 0]: Save private values as actual Widget properties

        # [Step 1]: Update drawings based on new values
        UpdateLine(self, "Track", self.Track)
        UpdateLine(self, "Filling", self.Filling)
        UpdateEllipse(self, "Background", self.background)

        # Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        # Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        self.trackColor.rgba        = self._current_trackColor
        self.fillingColor.rgba      = self._current_fillingColor
        self.backgroundColor.rgba   = self._current_backgroundColor
        # Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 initialState = States.Disabled,
                 trackWidth = 20,
                 fillingWidth = 10,
                 min = 0,
                 max = 100,
                 startAngle = 0,
                 endAngle = 360,
                 **kwargs):
        super(OutlineDial, self).__init__(**kwargs)
        Debug.Start("OutlineDial")
        #region --------------------------- Initial check ups
        self.InitAnimations()
        x = self.pos[0]
        y = self.pos[1]
        w = self.size[0]
        h = self.size[1]
        #endregion
        #region --------------------------- Set Variables
        Debug.Log("Setting internal variables to new specified values")
        self._state = initialState

        self.Properties.fillingWidth    = fillingWidth
        self.Properties.trackWidth      = trackWidth
        self.Properties.max             = max
        self.Properties.min             = min
        self.Properties.value           = self._current_value
        self.Properties.endAngle        = endAngle
        self.Properties.startAngle      = startAngle

        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for OutlineDial widget's background")
            self.backgroundColor = Color(rgba = (StatesColors.Text.GetColorFrom(self._state) if self._showBackground else (0,0,0,0)))
            self.background = GetEllipse(self, "Background")

            Debug.Log("Creating OutlineDial's track")
            self.trackColor = Color(rgba = (StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack else (0,0,0,0)))
            self.Track = GetLine(self, "Track")

            Debug.Log("Creating OutlineDial's filling")
            self.fillingColor = Color(rgba = (StatesColors.Default.GetColorFrom(self._state) if self._showFilling else (0,0,0,0)))
            self.Filling = GetLine(self, "Filling")

            Debug.Log("Binding events to OutlineDial")
            self.bind(pos = self._UpdatePos, size = self._UpdateSize)

        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting PieChartDial's color animation properties")

        self._current_backgroundColor       = self.backgroundColor.rgba
        self._wanted_BackgroundColor        = self.backgroundColor.rgba
        self._current_fillingColor          = self.fillingColor.rgba
        self._wanted_FillingColor           = self.fillingColor.rgba
        self._current_trackColor            = self.trackColor.rgba
        self._wanted_TrackColor             = self.trackColor.rgba

        Debug.Log("Setting PieChartDial's shape animation properties")

        self._current_pos           = (x, y)
        self._wanted_Pos            = (x, y)

        self._current_size          = (w, h)
        self._wanted_Size           = (w, h)

        self._current_pos_hint      = (x, y)
        self._wanted_Pos_hint       = (x, y)

        self._current_size_hint     = (w, h)
        self._wanted_Size_hint      = (w, h)

        self._current_endAngle      = endAngle
        self._wanted_EndAngle       = endAngle
        self._current_startAngle    = startAngle
        self._wanted_StartAngle     = startAngle
        self._current_fillingWidth  = fillingWidth
        self._current_trackWidth    = trackWidth
        self._wanted_FillingWidth   = fillingWidth
        self._wanted_TrackWidth     = trackWidth


        #endregion
        Debug.End()
    #endregion
    pass
#====================================================================#
# Bar Graph
#====================================================================#
class LineGraph(BRS_BarGraphWidgetAttributes, Widget):
    #region   --------------------------- DOCSTRING
    '''
        This class allows you to create a line graph with graph
        specific attributes such as orientation for example.

        Attributes are:
        - Orientation: "Top,Bottom,Left,Right"
        - Value
        - Min,Max
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _use_hint = False
    #endregion
    #region   --------------------------- GET SET
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
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

        # [Step 1]: Update drawings based on new values
        UpdateLine(self, "Track", self.Track)
        UpdateLine(self, "Filling", self.Filling)

        # [Step 2]: Update background's positions
        self.background.pos   = (self._current_pos[0], self._current_pos[1])
        self.background.size  = (self._current_size[0], self._current_size[1])

        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        Debug.Log("Color = {}".format(self._current_trackColor))
        self.trackColor.rgba        = self._current_trackColor
        self.fillingColor.rgba      = self._current_fillingColor
        self.backgroundColor.rgba   = self._current_backgroundColor
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 initialState = States.Disabled,
                 trackWidth = 20,
                 fillingWidth = 10,
                 min = 0,
                 max = 100,
                 orientation = "Top",
                 **kwargs):
        super(LineGraph, self).__init__(**kwargs)
        Debug.Start("LineGraph")
        #region --------------------------- Initial check ups
        self.InitAnimations()
        x = self.pos[0]
        y = self.pos[1]
        w = self.size[0]
        h = self.size[1]
        #endregion
        #region --------------------------- Set Variables
        Debug.Log("Setting internal variables to new specified values")
        self._state = initialState

        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for LineGraph widget's background")
            self.backgroundColor = Color(rgba = (StatesColors.Text.GetColorFrom(self._state) if self._showBackground else (0,0,0,0)))
            self.background = RoundedRectangle(size=(self.size[0], self.size[1]), pos=(x, y))

            Debug.Log("Creating LineGraph's track")
            self.trackColor = Color(rgba = (StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack else (0,0,0,0)))
            self.Track = GetLine(self, "Track")

            Debug.Log("Creating LineGraph's filling")
            self.fillingColor = Color(rgba = (StatesColors.Default.GetColorFrom(self._state) if self._showFilling else (0,0,0,0)))
            self.Filling = GetLine(self, "Filling")

            Debug.Log("Binding events to LineGraph")
            self.bind(pos = self._UpdatePos, size = self._UpdateSize)

        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting LineGraph's color animation properties")

        self._current_backgroundColor       = self.backgroundColor.rgba
        self._wanted_BackgroundColor        = self.backgroundColor.rgba
        self._current_fillingColor          = self.fillingColor.rgba
        self._wanted_FillingColor           = self.fillingColor.rgba
        self._current_trackColor            = self.trackColor.rgba
        self._wanted_TrackColor             = self.trackColor.rgba

        Debug.Log("Setting LineGraph's shape animation properties")

        self._current_pos           = (x, y)
        self._wanted_Pos            = (x, y)

        self._current_size          = (w, h)
        self._wanted_Size           = (w, h)

        self._current_pos_hint      = (x, y)
        self._wanted_Pos_hint       = (x, y)

        self._current_size_hint     = (w, h)
        self._wanted_Size_hint      = (w, h)

        self._orientation           = orientation
        self._current_fillingWidth  = fillingWidth
        self._current_trackWidth    = trackWidth
        self._wanted_FillingWidth   = fillingWidth
        self._wanted_TrackWidth     = trackWidth


        #endregion
        Debug.End()
    #endregion
    pass
#====================================================================#
LoadingLog.End("ValueDisplay.py")