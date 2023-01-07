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
class PieChartDial(Animated, Widget):
    #region   --------------------------- DOCSTRING
    '''
        This class allows you to create a PieChartDial like widget which represents
        a float value in between a starting angle and an ending angle.
        Use .Property to set the PieChartDial's properties such as end and start angle.
        Do not use Radians.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _state = States.Disabled
    animated : bool = False
    Properties = DrawingProperties()
    _use_hint = False
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
            Sets the value of the PieChartDial. It will automatically
            adjusts itself to be within the Propertie's range
        Args:
            newValue (float): the new value (from min to max)
        """

        # [Step 0]: Save newValue
        self._animated_value        = self.Properties.value
        self._animated_wantedValue  = self.Properties.TestValue(newValue)

        # [Step 1]: Update the shape based on the new value
        if(newValue != self._animated_value):
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
            Sets the filling width of the PieChartDial.
        Args:
            newValue (float): the new width of the PieChartDial's filling
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
        """ Returns the current width of the track aspect """
        return self.Properties.trackWidth

    @TrackWidth.setter
    def TrackWidth(self, newValue:int) -> None:
        """_summary_
            Sets the Track width of the PieChartDial.
        Args:
            newValue (float): the new width of the PieChartDial's track
        """
        Debug.Start("TrackWidth")
        # [Step 0]: Save newValue
        self._animated_wantedTrackWidth  = newValue

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape(None)
        Debug.End()
    #endregion
    #region   -- Size
    @property
    def Size(self) -> int:
        """ Returns the current Size of the widget """
        return self.size

    @Size.setter
    def Size(self, newValue:int) -> None:
        """_summary_
            Sets the Size of the PieChartDial.
        Args:
            newValue (float): the new size of the widget
        """
        Debug.Start("Size")
        # [Step 0]: Save newValue
        self._animated_wantedSize = newValue

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape(None)
        Debug.End()
    #endregion
    #region   -- Pos
    @property
    def Pos(self) -> int:
        """ Returns the current position of the widget (x,y)"""
        return self.pos

    @Pos.setter
    def Pos(self, newValue:int) -> None:
        """_summary_
            Sets the position of the PieChartDial.
        Args:
            newValue (float): the new position of the PieChartDial (x,y)
        """
        Debug.Start("Pos")
        # [Step 0]: Save newValue
        self._animated_wantedPos = newValue

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape(None)
        Debug.End()
    #endregion
    #region   -- ShowTrack
    @property
    def ShowTrack(self) -> bool:
        """ Returns wether the track is shown or not """
        return self.Properties.showTrack

    @ShowTrack.setter
    def ShowTrack(self, newValue:bool) -> None:
        """_summary_
            Sets wether the track is shown or not
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
        """ Returns wether the fillinf is shown or not """
        return self.Properties.showFilling

    @ShowFilling.setter
    def ShowFilling(self, newValue:bool) -> None:
        """_summary_
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
        """ Returns wether the background is shown or not """
        return self.Properties.showBackground

    @ShowBackground.setter
    def ShowBackground(self, newValue:bool) -> None:
        """_summary_
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
    def SetAttributes(self, TrackWidth=Properties.trackWidth, FillingWidth=Properties.fillingWidth, position=None, size=None, endAngle=Properties.endAngle, startAngle=Properties.startAngle, value=Properties.value, showTrack=Properties.showTrack, showBackground=Properties.showBackground, showFilling=Properties.showFilling):
        """
            Allows you to set multiple properties at once instead of creating an animation for each one you change.
        """
        if(position == None):
            pos = self.pos
        if(size == None):
            size = self.size

        self._animated_wantedFillingWidth = FillingWidth
        self._animated_wantedTrackWidth   = TrackWidth
        self._animated_wantedPos          = position
        self._animated_wantedSize         = size
        self._animated_wantedStartAngle   = startAngle
        self._animated_wantedEndAngle     = endAngle
        self._animated_wantedValue        = self.Properties.TestValue(value)

        self.Properties.showFilling = showFilling
        self.Properties.showTrack = showTrack
        self.Properties.showBackground = showBackground

        self._UpdateShape(None)
    # -------------------------------------------
    def SetAttributesFromParent(self):
        """
            This is called after the widget is added to the layout.
            It is impossible for the code to know that sort of shit in the __init__
            so this will make your widget relative in the parents layout area.
        """
        Debug.Start("SetAttributesFromParent")
        Debug.Log("Automatically positioning widget based off parent's informations")

        # - Step 0 - Pos and sizes
        Debug.Log("Size of Parent: {}".format(self.parent.size))
        Debug.Log("Pos of Parent: {}".format(self.parent.pos))
        Debug.Log("size_hint_max of Parent: {}".format(self.parent.size_hint_max))
        Debug.Log("size_hint_min of Parent: {}".format(self.parent.size_hint_min))
        Debug.Log("pos_hint of Parent: {}".format(self.parent.pos_hint))
        Debug.Log("size_hint_x of Parent: {}".format(self.parent.size_hint_x))
        Debug.Log("size_hint_y of Parent: {}".format(self.parent.size_hint_y))
        Debug.Log("size_hint_max_x of Parent: {}".format(self.parent.size_hint_max_x))
        Debug.Log("size_hint_max_y of Parent: {}".format(self.parent.size_hint_max_y))
        Debug.Log("size_hint_min_x of Parent: {}".format(self.parent.size_hint_min_x))
        Debug.Log("size_hint_min_y of Parent: {}".format(self.parent.size_hint_min_y))
        # self._animated_wantedPos = self.to_parent(self.pos)
        # self._animated_wantedSize = self.to_parent(self.size)

        # - Instant animation to put the widget back to where it should've been by default.
        self._InstantAnimation()
        self._UpdateShape()
        Debug.End()
    #endregion
    #region   -- Private
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        # Debug.Log("[Step 0]:")
        self._animated_wantedFillingColor   = StatesColors.Default.GetColorFrom(self._state) if self.Properties.showFilling else (0,0,0,0)
        self._animated_wantedTrackColor     = StatesColors.Pressed.GetColorFrom(self._state) if self.Properties.showTrack else (0,0,0,0)
        self._animated_wantedBackgroundColor= StatesColors.Text.GetColorFrom(self._state) if self.Properties.showBackground else (0,0,0,0)

        # [Step 1]: Set animation's current values
        # Debug.Log("[Step 1]:")
        self._animated_fillingColor     = self.Properties.fillingColor.rgba
        self._animated_trackColor       = self.Properties.trackColor.rgba
        self._animated_backgroundColor  = self.Properties.backgroundColor.rgba

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
        # Debug.Log("Updating the shape of the PieChartDial")

        # Debug.Log("Setting animation parameters")
        self._Animated_Get("Shapes", fromTheseProperties = self.Properties)

        self._animated_pos = self.rect.pos
        self._animated_size = self.rect.size

        # Debug.Log("Set wanteds")

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
        self.pos = self._animated_pos
        self.size = self._animated_size

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
        self.Properties.backgroundColor.rgba = self._animated_backgroundColor
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, initialState=_state, trackWidth=Properties.trackWidth, fillingWidth=Properties.fillingWidth, min=Properties.min, max=Properties.max, startAngle=Properties.startAngle, endAngle=Properties.endAngle,  **kwargs):
        super(PieChartDial, self).__init__(**kwargs)
        Debug.Start("PieChartDial")
        #region --------------------------- Initial check ups
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

        self._value = self.Properties.value
        self._wantedValue = self.Properties.value

        Debug.Log("the maximum is: {}".format(self.Properties.max))
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Creating drawings for PieChartDial widget's background")
            self.Properties.backgroundColor = Color(rgba = (StatesColors.Text.GetColorFrom(self._state) if self.Properties.showBackground else (0,0,0,0)))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)

            Debug.Log("Creating PieChartDial's track")
            self.Properties.trackColor = Color(rgba = (StatesColors.Pressed.GetColorFrom(self._state) if self.Properties.showTrack else (0,0,0,0)))
            self.Track = GetEllipse(self.Properties, self, "Track")

            Debug.Log("Creating PieChartDial's filling")
            self.Properties.fillingColor = Color(rgba = (StatesColors.Default.GetColorFrom(self._state) if self.Properties.showFilling else (0,0,0,0)))
            self.Filling = GetEllipse(self.Properties, self, "Filling")

            # Debug.Log("Binding events to PieChartDial")
            #self.bind(Properties.showTrack = self._UpdateShape, size = self._UpdateShape)

        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting PieChartDial's color animation properties")
        self._animated_backgroundColor      = self.Properties.backgroundColor.rgba
        self._animated_wantedBackgroundColor= self.Properties.backgroundColor.rgba
        self._animated_fillingColor         = self.Properties.fillingColor.rgba
        self._animated_wantedFillingColor   = self.Properties.fillingColor.rgba
        self._animated_trackColor           = self.Properties.trackColor.rgba
        self._animated_wantedTrackColor     = self.Properties.trackColor.rgba

        Debug.Log("Setting PieChartDial's shape animation properties")
        self._animated_pos                  = self.pos
        self._animated_pos                  = self.pos
        self._animated_size                 = self.size
        self._animated_wantedSize           = self.size
        self._animated_value                = self.Properties.value
        self._animated_wantedValue          = self.Properties.value
        self._animated_endAngle             = self.Properties.endAngle
        self._animated_wantedEndAngle       = self.Properties.endAngle
        self._animated_startAngle           = self.Properties.startAngle
        self._animated_wantedStartAngle     = self.Properties.startAngle
        self._animated_fillingWidth         = self.Properties.fillingWidth
        self._animated_trackWidth           = self.Properties.trackWidth
        self._animated_wantedFillingWidth   = self.Properties.fillingWidth
        self._animated_wantedTrackWidth     = self.Properties.trackWidth

        #endregion
        Debug.End()
    #endregion
    pass