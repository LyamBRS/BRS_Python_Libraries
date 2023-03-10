#====================================================================#
# File Information
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("attributes.py")
#====================================================================#
# Imports
#====================================================================#
import time
from ...Debug.consoleLog import Debug
from ...Utilities.states import States,StatesColors
from ...GUI.Utilities.colors import GUIColors
from ...GUI.Utilities.references import Shadow
from kivy.clock import Clock
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.animation import Animation
from kivy.graphics import svg

from kivymd.uix.card import MDCard

from ...GUI.Utilities.font import Font

#====================================================================#
# Functions
#====================================================================#
def UpdateEllipse(widget, type:str, ellipse):
    ##Debug.Start("UpdateEllipse")
    """Updates an already existing Ellipse from DrawingProperties"""

    if(type == "Track"):
        # ##Debug.Log("\nGetting Track ellipse")
        ellipse.pos  = (widget._current_pos[0] + widget._current_trackWidth/2,
                        widget._current_pos[1] + widget._current_trackWidth/2)
        ellipse.size = (widget._current_size[0] - widget._current_trackWidth,
                        widget._current_size[1] - widget._current_trackWidth)
        ellipse.angle_start = widget._current_startAngle
        ellipse.angle_end   = widget._current_endAngle

    elif(type == "Filling"):
        ellipse.pos  = (
                        widget._current_pos[0] + widget._current_fillingWidth/2,
                        widget._current_pos[1] + widget._current_fillingWidth/2
                        )
        ellipse.size = (
                        widget._current_size[0] - widget._current_fillingWidth,
                        widget._current_size[1] - widget._current_fillingWidth
                        )

        ratio      = _GetRatio(widget)
        startAngle = _GetStartAngle(widget)
        endAngle   = _GetEndAngle(widget, startAngle, ratio)
        ellipse.angle_start = startAngle
        ellipse.angle_end =  endAngle

    elif(type == "Background"):
        ellipse.pos = (widget._current_pos[0] + widget._current_trackWidth, widget._current_pos[1] + widget._current_trackWidth)
        ellipse.size = (widget._current_size[0] - widget._current_trackWidth*2, widget._current_size[1] - widget._current_trackWidth*2)

    ##Debug.End()
#---------------------------------------------------------------------
def GetEllipse(widget, type:str):
    # ##Debug.Start()
    """Draws an ellipse from given values"""

    if(type == "Track"):
        ellipseWidth = widget._current_trackWidth
        startAngle = widget._current_startAngle
        endAngle = widget._current_endAngle
        width   = widget.size[0] - (widget._current_fillingWidth * 2)
        height  = widget.size[1] - (widget._current_trackWidth * 2)

    elif(type == "Filling"):
        ellipseWidth    = widget._current_fillingWidth
        ratio           = _GetRatio(widget)
        startAngle      = _GetStartAngle(widget)
        endAngle        = _GetEndAngle(widget, startAngle, ratio)
        width   = widget.size[0] - (widget._current_fillingWidth * 2)
        height  = widget.size[1] - (widget._current_trackWidth * 2)

    elif(type == "Background"):
        ellipseWidth = 0
        startAngle = 0
        endAngle = 360
        width = widget.size[0] - (widget._current_trackWidth * 2)
        height = widget.size[1] - (widget._current_trackWidth * 2)

    position = (widget.pos[0] + ellipseWidth, widget.pos[1] + ellipseWidth)

    # ##Debug.End()
    return Ellipse(pos=position, size=(width,height), angle_start=startAngle, angle_end=endAngle, line=(2, (1, 0, 0, 1)))
#---------------------------------------------------------------------
def UpdateLine(widget, type:str, line):
    ##Debug.Start("UpdateLine")
    """
        Updates an already existing Border from a widget's
        attributes.

        Your widget needs to have the following attributes:
        - Attribute_Track
        - Attribute_Filling
        - Attribute_Value

        Optional attributes are:
        - Attribute_Angles
    """
    # [Step 0]: Get the largest of both tracks
    width = _GetLargestTrack(widget)

    # [Step 1]: Check if the widget has end and start attributes
    if(hasattr(widget, "_current_endAngle")):
        if(type == "Track"):
            line.ellipse = (
                            widget._current_pos[0] + width,
                            widget._current_pos[1] + width,
                            widget._current_size[0] - width*2,
                            widget._current_size[1] - width*2,
                            widget._current_startAngle,
                            widget._current_endAngle
                            )
            line.width = widget._current_trackWidth
        else:

            # Get width if equal to minimum
            fillingwidth = _GetFillingWidth(widget, 10000)
            line.width = fillingwidth

            # Get result values for the filling track
            ratio      = _GetRatio(widget)
            startAngle = _GetStartAngle(widget)
            endAngle   = _GetEndAngle(widget, startAngle, ratio)

            # Update the ellipse's properties
            line.ellipse = (
                            widget._current_pos[0] + width,
                            widget._current_pos[1] + width,
                            widget._current_size[0] - width*2,
                            widget._current_size[1] - width*2,
                            startAngle,
                            endAngle
                            )
    else:
        # [Step 2]: Creating the 2 coordinates needed to create the line
        if(widget._orientation == "Top" or widget._orientation == "Bottom"):
            maxWidth = widget._current_size[0]/2
            x1 = widget._current_pos[0] + widget._current_size[0]/2 # For centering
            x2 = widget._current_pos[0] + widget._current_size[0]/2 # For centering
            y1 = widget._current_pos[1]
            y2 = widget._current_pos[1] + widget._current_size[1]
        else:
            maxWidth = widget._current_size[1]/2
            x1 = widget._current_pos[0]
            x2 = widget._current_pos[0] + widget._current_size[0]
            y1 = widget._current_pos[1] + widget._current_size[1]/2 # For centering
            y2 = widget._current_pos[1] + widget._current_size[1]/2 # For centering

        if(type == "Track"):
            # Width check so we don't overflow onto other neighboring widgets
            width = widget._current_trackWidth
            if(width > maxWidth):
                width = maxWidth

            if(width <= 0):
                width = 1

            line.points = (x1, y1, x2, y2)
            line.width = width

        elif(type == "Filling"):
            # Width check so we don't overflow onto other neighboring widgets
            width = _GetFillingWidth(widget, maxWidth)

            # Create variables depending on if we start from the middle or not
            if(widget._startFromMiddle):
                ratio = ((widget._current_value - widget._current_min) / (widget._current_max - widget._current_min))-0.5
                offsetHeight = (widget._current_size[1] * 0.5)
                offsetWidth = (widget._current_size[0] * 0.5)
            else:
                ratio = (widget._current_value - widget._current_min) / (widget._current_max - widget._current_min)
                offsetHeight = 0
                offsetWidth = 0

            # Find the starting coordinates and the ending coordinates depending on the wanted orientation.
            if(widget._orientation == "Top"):
                distance = (widget._current_size[1]) * ratio
                startX = x2
                startY = y2 - offsetHeight
                endX   = x1
                endY   = y2 - (distance + offsetHeight)
                ##Debug.Log("startY : {}, endY : {}".format(startY, endY))

            elif(widget._orientation == "Right"):
                distance = (widget._current_size[0]) * ratio
                startX = x2 - offsetWidth
                startY = y2
                endX   = x2 - (distance + offsetWidth)
                endY   = y1
            elif(widget._orientation == "Bottom"):
                distance = (widget._current_size[1]) * ratio
                startX = x1
                startY = y1 + offsetHeight
                endX   = x2
                endY   = y1 + (distance + offsetHeight)
            elif(widget._orientation == "Left"):
                distance = (widget._current_size[0]) * ratio
                startX = x1 + offsetWidth
                startY = y1
                endX   = x1 + (distance + offsetWidth)
                endY   = y2

            line.points = (startX, startY, endX, endY)
            line.width = width

        elif(type == "Background"):
            if(maxWidth <= 0):
                maxWidth = 1
            line.points = (x1, y1, x2, y2)
            line.width = maxWidth

    ##Debug.End()
#---------------------------------------------------------------------
def GetLine(widget, type:str):
    ##Debug.Start("GetLine")
    """
        Draws a border from given values.
        if your widget has end and start angles attributes,
        it will draw an ellipse.

        Your widget needs to have the following attributes:
        - Attribute_Track
        - Attribute_Filling
        - Attribute_Value

        Optional attributes are:
        - Attribute_Angles
    """

    # [Step 0]: Get the largest of both tracks
    ellipseWidth = _GetLargestTrack(widget)

    # [Step 1]: Check if the widget has end and start attributes
    if(hasattr(widget, "_current_endAngle")):
        if(type == "Track"):
            startAngle      = widget._current_startAngle
            endAngle        = widget._current_endAngle
            width           = widget.size[0] - (ellipseWidth * 2)
            height          = widget.size[1] - (ellipseWidth * 2)

        elif(type == "Filling"):
            ratio           = _GetRatio(widget)
            startAngle      = _GetStartAngle(widget)
            endAngle        = _GetEndAngle(widget, startAngle, ratio)
            width           = widget.size[0] - (ellipseWidth * 2)
            height          = widget.size[1] - (ellipseWidth * 2)

        # [Step 2]: Get the ellipse's position
        position = (widget.pos[0] + ellipseWidth, widget.pos[1] + ellipseWidth)

        # [Step 3]: Return the line resulting from the previous settings
        ##Debug.End()
        return Line(ellipse=(position[0], position[1], width, height, startAngle, endAngle), width=ellipseWidth)

    else:
        # [Step 2]: Creating the 2 coordinates needed to create the line
        if(widget._orientation == "Top" or widget._orientation == "Bottom"):
            maxWidth = widget._current_size[0]/2
            x1 = widget._current_pos[0] + widget._current_size[0]/2 # For centering
            x2 = widget._current_pos[0] + widget._current_size[0]/2 # For centering
            y1 = widget._current_pos[1]
            y2 = widget._current_pos[1] + widget._current_size[1]
        else:
            maxWidth = widget._current_size[1]/2
            x1 = widget._current_pos[0]
            x2 = widget._current_pos[0] + widget._current_size[0]
            y1 = widget._current_pos[1] + widget._current_size[1]/2 # For centering
            y2 = widget._current_pos[1] + widget._current_size[1]/2 # For centering

        if(type == "Track"):
            # Width check so we don't overflow onto other neighboring widgets
            width = widget._current_trackWidth
            if(width > maxWidth):
                width = maxWidth

            if(width <= 0):
                width = 1

            ##Debug.End()
            return Line(points=(x1, y1, x2, y2), width=width)

        elif(type == "Filling"):
            # Width check so we don't overflow onto other neighboring widgets
            width = _GetFillingWidth(widget, maxWidth)

            # Create variables depending on if we start from the middle or not
            if(widget._startFromMiddle):
                ratio = ((widget._current_value - widget._current_min) / (widget._current_max - widget._current_min))-0.5
                offsetHeight = (widget._current_size[1] * 0.5)
                offsetWidth = (widget._current_size[0] * 0.5)
            else:
                ratio = (widget._current_value - widget._current_min) / (widget._current_max - widget._current_min)
                offsetHeight = 0
                offsetWidth = 0

            # Find the starting coordinates and the ending coordinates depending on the wanted orientation.
            if(widget._orientation == "Top"):
                distance = (widget._current_size[1]) * ratio
                startX = x2
                startY = y2 - offsetHeight
                endX   = x1
                endY   = y2 - (distance + offsetHeight)
                ##Debug.Log("startY : {}, endY : {}".format(startY, endY))

            elif(widget._orientation == "Right"):
                distance = (widget._current_size[0]) * ratio
                startX = x2 - offsetWidth
                startY = y2
                endX   = x2 - (distance + offsetWidth)
                endY   = y1
            elif(widget._orientation == "Bottom"):
                distance = (widget._current_size[1]) * ratio
                startX = x1
                startY = y1 + offsetHeight
                endX   = x2
                endY   = y1 + (distance + offsetHeight)
            elif(widget._orientation == "Left"):
                distance = (widget._current_size[0]) * ratio
                startX = x1 + offsetWidth
                startY = y1
                endX   = x1 + (distance + offsetWidth)
                endY   = y2

            ##Debug.End()
            return Line(points=(startX, startY, endX, endY), width=width)

        elif(type == "Background"):
            if(maxWidth <= 0):
                maxWidth = 1

            ##Debug.End()
            return Line(points=(x1, y1, x2, y2), width=maxWidth)


#--------------------------------------------------------------------
def _GetFillingWidth(widget, maximumWidth) -> int:

    # Width check so we don't overflow onto other neighboring widgets
    width = widget._current_fillingWidth
    if(width > maximumWidth):
        width = maximumWidth

    # Check if equal to 0. If yes, equals to 1 to avoid errors.
    if(width <= 0):
        width = 1

    if(widget._startFromMiddle):
        # Check if value is equal to half the ratio
        if((((widget._current_value - widget._current_min) / (widget._current_max - widget._current_min))-0.5) == 0):
            width = 1
        return width
    else:
        # Check if value is equal to minimum
        if(widget._current_value == widget._current_min):
            width = 1
        return width
#--------------------------------------------------------------------
def _GetRatio(widget) -> int:
    """
        Gets a ratio from 0 to 1 or -0.5 to 0.5 depending on
        the widget's value, minimum and maximum.

        if startfromMiddle is True, 0.5 will be used as a ratio.
        Otherwise, 0 to 1 will be the returned ratio.
    """
    #[Step 0]: Get the values
    _min = widget._current_min
    _max = widget._current_max
    _value = widget._current_value

    #[Step 1]: Check if we want to start from the middle or not
    if(widget._startFromMiddle):
        return ((_value - _min) / (_max - _min)) - 0.5
    else:
        return ((_value - _min) / (_max - _min))
#--------------------------------------------------------------------
def _GetLargestTrack(widget) -> int:
    """
        Returns either the Filling track's width
        or the Track's width. Also won't return 0.
    """
    # [Step 0]: Get global variables as local variables.
    _filling = widget._current_fillingWidth
    _track   = widget._current_trackWidth

    # [Step 1]: Check which is larger
    if(_filling > _track):
        width = _filling
    else:
        width = _track

    # [Step 2]: Make sure it is not equal to 0
    if(width <= 0):
        width = 1
    
    # [Step 3]: Return the resulted value
    return width
#---------------------------------------------------------------------
def _GetStartAngle(widget) -> int:
    """
        Returns the widget's starting angle in degrees
    """
    # [Step 0]: Get local variables
    _start = widget._current_startAngle
    _end   = widget._current_endAngle

    # [Step 1]: Check if we are starting from the middle
    if(widget._startFromMiddle):

        # [Step 2]: Calculate the offset between the Start and End
        offset = (_end - _start)/2

        # [Step 3]: Return the adjusted starting angle:
        return _start + offset

    else:
        # [Step 2]: Return start angle
        return _start
#---------------------------------------------------------------------
def _GetEndAngle(widget, startAngle, ratio) -> int:
    """
        Calculates the end angle of a widget depending on a given
        ratio.
    """
    #[Step 0]: Get global variables as local variables
    _end   = widget._current_endAngle

    #[Step 1]: Check if we are starting from the middle
    if(widget._startFromMiddle):
        #[Step 2]: Get angle distance between start and end angle
        length = (_end - startAngle)*2

        #[Step 3]: Calculate the ratio on that length and add the start angle's offset
        return (length * ratio) + startAngle

    else:
        #[Step 2]: Get the distance between start and end
        length = (_end - startAngle)

        #[Step 3]: Calculate the ratio on that length and add the start angle's offset
        return (length * ratio) + startAngle
#---------------------------------------------------------------------
#====================================================================#
# Lists
#====================================================================#
#====================================================================#
# Inherited Attributes
#====================================================================#
class Attribute_Foundation:
    #region   --------------------------- DOCSTRING
    '''
        Inherited class containing all the very basic attributes that 
        a BRS widget should have no matter its type or purpose in life.

        Do not build this class

        - State
        - Size
        - Pos
        - Size_hint
        - Pos_hint
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
    _forceAnimation             = False
    """
        This is used by other attributes.
        Do not manually use this.

        An example of attributes using this would be orientation changes for example.
        Since there is no ways to tell all that must be changed, that one is instant.
    """
    #endregion
    #region   --------------------------- GET SET
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
    #region   -- Size
    @property
    def Size(self) -> list:
        """ [GET]:
            Returns the current Size of the widget.
            This returns a new array and not an address
        """
        ##Debug.Start("GET Size")
        ##Debug.End()
        return (self.size[0], self.size[1])

    @Size.setter
    def Size(self, newValue:list) -> None:
        """ [SET]:
            Sets the Size of the widget.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new size of the widget
        """
        ##Debug.Start("SET Size")
        # [Step 0]: Save newValue
        self._wanted_Size = (newValue[0], newValue[1])
        # [Step 1]: Update the shape based on the new value
        self._UpdateShape()
        ##Debug.End()
    #endregion
    #region   -- Pos
    @property
    def Pos(self) -> list:
        """ [GET]:
        Returns the current position of the widget (x,y)
        This returns a new array, not an address
        """
        ##Debug.Start("Pos: Get")
        ##Debug.End()
        return (self.pos[0], self.pos[1])

    @Pos.setter
    def Pos(self, newValue:list) -> None:
        """ [SET]:
            Sets the position of the widget.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new position of the widget (x,y)
        """
        #Debug.Start("SET Pos")
        # [Step 0]: Save newValue
        self._wanted_Pos = (newValue[0], newValue[1])

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape()
        #Debug.End()
    #endregion
    #region   -- Size_hint
    @property
    def Size_hint(self) -> list:
        """ [GET]:
            Returns the current Size_hint of the widget.
            This returns a new array and not an address
        """
        return (self.size_hint[0], self.size_hint[1])

    @Size_hint.setter
    def Size_hint(self, newValue:list) -> None:
        """ [SET]:
            Sets the size_hint of the widget.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new size_hint of the widget
        """
        #Debug.Start("Size_hint")
        # [Step 0]: Save newValue
        self._wanted_Size_hint = (newValue[0], newValue[1])

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape()
        #Debug.End()
    #endregion
    #region   -- Pos_hint
    @property
    def Pos_hint(self) -> list:
        """ [GET]:
        Returns the current position of the widget (x,y)
        This returns a new array, not an address
        """
        return (self.pos_hint[0], self.pos_hint[1])

    @Pos_hint.setter
    def Pos_hint(self, newValue:list) -> None:
        """ [SET]:
            Sets the Pos_hint of the widget.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new Pos_hint of the widget (x,y)
        """
        #Debug.Start("Pos_hint")
        # [Step 0]: Save newValue
        self._wanted_Pos_hint = (newValue[0], newValue[1])

        # [Step 1]: Update the shape based on the new value
        self._UpdateShape()
        #Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Foundation_SetToWanted(self):
        #Debug.Start("_Attribute_Foundation_SetToWanted")
        self._current_pos = (self._wanted_Pos[0], self._wanted_Pos[1])
        self._current_pos_hint = (self._wanted_Pos_hint[0], self._wanted_Pos_hint[1])
        self._current_size = (self._wanted_Size[0], self._wanted_Size[1])
        self._current_size_hint = (self._wanted_Size_hint[0], self._wanted_Size_hint[1])
        #Debug.End()

    def _Attribute_Foundation_GetShapeComparator(self):
        #Debug.Start("_Attribute_Foundation_GetShapeComparator")
        comparator = {
                        "_current_pos"  : self._current_pos,
                        "_current_size" : self._current_size,
                        "_current_pos_hint" : self._current_pos_hint,
                        "_current_size_hint" : self._current_size_hint
                     }
        #Debug.End()
        return comparator
    def _Attribute_Foundation_GetShapeArguments(self):
        #Debug.Start("_Attribute_Foundation_GetShapeComparator")
        attributes = {
                        "_current_pos"  : self._wanted_Pos,
                        "_current_size" : self._wanted_Size,
                        "_current_pos_hint"  : self._wanted_Pos_hint,
                        "_current_size_hint" : self._wanted_Size_hint
                     }
        #Debug.End()
        return attributes

    def _Attribute_Foundation_SetAttributes(self, state=None, pos=None, size=None, radius=None, posHint=None, sizeHint=None):
        """
            Sets all the foundation attributes of the widget to something.
            This is private, use your widgets's SetAttribute function instead.
        """
        self._wanted_Pos = self._wanted_Pos if (pos == None) else (pos[0], pos[1])
        self._wanted_Size = self._wanted_Size if (size == None) else (size[0], size[1])

        self._wanted_Pos_hint = self._wanted_Pos_hint if (posHint == None) else (posHint[0], posHint[1])
        self._wanted_Size_hint = self._wanted_Size_hint if (sizeHint == None) else (sizeHint[0], sizeHint[1])

        self._wanted_Radius = self._wanted_Radius if(radius == None) else radius
    #endregion
    pass

class Attribute_Track:
    #region   --------------------------- DOCSTRING
    '''
        Inherited class containing all needed members and methods
        in order to add a track to your widget.

        A track is what it is. It's a track which a "filling" follows.
        A filling is drawn above the track and represents a value.
        Tracks usually goes from a minimum to a maximum associated with
        a value
    '''
    #endregion
    #region   --------------------------- MEMBERS
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
    _current_trackWidth         = 0
    """
        Private variable specifying the current padding of the
        widget's track. Defaults to 0.

        Set this before calling the Animation starter.
    """
    _wanted_TrackWidth          = 0
    """
        Private variable representing your widget's new Track padding.
        Defaults to 0

        Only set this before starting your animation.
    """
    _showTrack : bool = True
    """Enables the tracks's drawing"""
    _useCustomTrackColor:list = None
    #endregion
    #region   --------------------------- GET SET
    #region   -- UseCustomTrackColor
    @property
    def UseCustomTrackColor(self) -> list:
        """ [GET]:
        Returns wether the track is a custom color or not
        """
        return self._useCustomTrackColor

    @UseCustomTrackColor.setter
    def UseCustomTrackColor(self, newValue:list) -> None:
        """ [SET]:
            Sets wether the track is a custom color or not.
            If `None`, then no custom colors will be used anymore
        Args:
            newValue (list): the new color
        """
        #Debug.Start("ShowBackground")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self._useCustomTrackColor):
            self._useCustomTrackColor = newValue
            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #region   -- TrackWidth
    @property
    def TrackWidth(self) -> int:
        """ [GET]:
            Returns the current width of the track aspect
        """
        return self._wanted_TrackWidth

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
        #Debug.Start("TrackWidth")

        if(newValue == 0):
            #Debug.Warn("Attempted to set width at 0. Automatically set back to 1")
            newValue = 1

        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_TrackWidth):
            # self._wanted_TrackWidth  = newValue
            self._UpdateShape()
        #Debug.End()
    #endregion
    #region   -- ShowTrack
    @property
    def ShowTrack(self) -> bool:
        """ [GET]:
            Returns wether the track is shown or not 
        """
        return self._showTrack

    @ShowTrack.setter
    def ShowTrack(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the track is shown or not.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (bool): the new showing or not
        """
        #Debug.Start("ShowTrack")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self._showTrack):
            self._showTrack = newValue
            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Track_SetToWanted(self):
        self._current_trackColor = (
                                    self._wanted_TrackColor[0],
                                    self._wanted_TrackColor[1],
                                    self._wanted_TrackColor[2],
                                    self._wanted_TrackColor[3],
                                    )
        self._current_trackWidth = self._wanted_TrackWidth
    def _Attribute_Track_GetColorsComparator(self):
        comparator = {
                        "_current_trackColor"      : self._current_trackColor,
                     }
        return comparator
    def _Attribute_Track_GetColorsArguments(self):
        attributes = {
                      "_current_trackColor"      : self._wanted_TrackColor,
                     }
        return attributes
    def _Attribute_Track_GetShapeComparator(self):
        comparator = {
                        "_current_trackWidth"      : self._current_trackWidth,
                     }
        return comparator
    def _Attribute_Track_GetShapeArguments(self):
        attributes = {
                      "_current_trackWidth"      : self._wanted_TrackWidth,
                     }
        return attributes
    #endregion
    pass
class Attribute_Filling:
    #region   --------------------------- DOCSTRING
    '''
        Inherited class containing all needed members and methods
        in order to add a filling to your widget.

        A track is what it is. It's a track which a "filling" follows.
        A filling is drawn above the track and represents a value.
        Tracks usually goes from a minimum to a maximum associated with
        a value
        Fillings go from min to value
    '''
    #endregion
    #region   --------------------------- MEMBERS
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
    _showFilling : bool = True
    """Defines if the filling should be displayed"""
    _useCustomFillingColor:list = None
    #endregion
    #region   --------------------------- GET SET
    #region   -- UseCustomFillingColor
    @property
    def UseCustomFillingColor(self) -> list:
        """ [GET]:
        Returns wether the filling is a custom color or not
        `None`: not a custom color
        """
        return self._useCustomFillingColor

    @UseCustomFillingColor.setter
    def UseCustomFillingColor(self, newValue:list) -> None:
        """ [SET]:
            Sets wether the filling is a custom color or not.
            if `None`, no custom colors will be used
        Args:
            newValue (list): the new color
        """
        #Debug.Start("ShowBackground")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self._useCustomFillingColor):
            self._useCustomFillingColor = newValue
            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #region   -- FillingWidth
    @property
    def FillingWidth(self) -> int:
        """ [GET]:
            Returns the current width of the filling aspect
        """
        return self._wanted_FillingWidth

    @FillingWidth.setter
    def FillingWidth(self, newValue:int) -> None:
        """ [SET]:
            Sets the filling width of the PieChartDial.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new width of the PieChartDial's filling
        """
        #Debug.Start("FillingWidth")

        if(newValue == 0):
            #Debug.Warn("Attempted to set width at 0. Automatically set back to 1")
            newValue = 1

        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_FillingWidth):
            self._wanted_FillingWidth  = newValue
            self._UpdateShape()
        #Debug.End()
    #endregion
    #region   -- ShowFilling
    @property
    def ShowFilling(self) -> bool:
        """ [GET]:
            Returns wether the track is shown or not 
        """
        return self._showFilling

    @ShowFilling.setter
    def ShowFilling(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the track is shown or not.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (bool): the new showing or not
        """
        #Debug.Start("ShowFilling")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self._showFilling):
            self._showFilling = newValue
            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Filling_SetToWanted(self):
        self._current_fillingColor = (
                                    self._wanted_FillingColor[0],
                                    self._wanted_FillingColor[1],
                                    self._wanted_FillingColor[2],
                                    self._wanted_FillingColor[3],
                                    )
        self._current_fillingWidth = self._wanted_FillingWidth
    def _Attribute_Filling_GetColorsComparator(self):
        comparator = {
                        "_current_fillingColor"      : self._current_fillingColor,
                     }
        return comparator
    def _Attribute_Filling_GetColorsArguments(self):
        attributes = {
                      "_current_fillingColor"      : self._wanted_FillingColor,
                     }
        return attributes
    def _Attribute_Filling_GetShapeComparator(self):
        comparator = {
                        "_current_fillingWidth"      : self._current_fillingWidth,
                     }
        return comparator
    def _Attribute_Filling_GetShapeArguments(self):
        attributes = {
                      "_current_fillingWidth"      : self._wanted_FillingWidth,
                     }
        return attributes
    #endregion
    pass
class Attribute_Background:
    #region   --------------------------- DOCSTRING
    '''
        Inherited class containing all needed members and methods
        in order to add a background to your widget.

        The background takes the entire widget's size.

        - BackgroundColor
        - ShowBackground
    '''
    #endregion
    #region   --------------------------- MEMBERS
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
    _wanted_BackgroundShadowColor     = [0,0,0,0]
    """
        Private variable used to store the wanted shadow color of
        the widget. Defaults to [0,0,0,0].
    """
    _current_backgroundShadowColor    = [0,0,0,0]
    """
        Private variable used to store the current shadow color of
        the widget. Defaults to [0,0,0,0].

        Use this to update the widget's
        real primary color in your Animation binded on_progress function.
    """
    _showBackground : bool = True
    """ Defines wether the background of the widget should be shown or not. Defaults to True """
    _showShadow : bool = False
    """ Defines wether the background of the widget or layout should have a shadow or not. Defaults to False"""
    _useCustomBackgroundColor:list = None
    #endregion
    #region   --------------------------- GET SET
    #region   -- UseCustomBackgroundColor
    @property
    def UseCustomBackgroundColor(self) -> list:
        """ [GET]:
        Returns wether the background is a custom color or not
        if `None`, then no custom color is used
        """
        return self._useCustomBackgroundColor

    @UseCustomBackgroundColor.setter
    def UseCustomBackgroundColor(self, newValue:list) -> None:
        """ [SET]:
            Sets wether the background is a custom color or not.
            if `None`, no custom colors will be used
        Args:
            newValue (list): the new showing or not
        """
        #Debug.Start("ShowBackground")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self._useCustomBackgroundColor):
            self._useCustomBackgroundColor = newValue
            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #region   -- ShowBackground
    @property
    def ShowBackground(self) -> bool:
        """ [GET]:
        Returns wether the background is shown or not
        """
        return self._showBackground

    @ShowBackground.setter
    def ShowBackground(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the background is shown or not
        Args:
            newValue (bool): the new showing or not
        """
        #Debug.Start("ShowBackground")

        # [Step 1]: Update the shape based on the new value if its a new value
        if(newValue != self._showBackground):
            self._showBackground = newValue

            if(self._showShadow and not self._showBackground):
                self._showShadow = False

            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #region   -- ShowShadow
    @property
    def ShowShadow(self) -> bool:
        """ [GET]:
        Returns wether the background's shadow is shown or not
        """
        return self._showShadow

    @ShowShadow.setter
    def ShowShadow(self, newValue:bool) -> None:
        """ [SET]:
            Sets wether the background's shadow is shown or not
        Args:
            newValue (bool): the new showing or not
        """
        #Debug.Start("ShowShadow")

        # [Step 1]: Update the shape based on the new value if its a new value
        if((newValue != self._showShadow) and self._showBackground):
            self._showShadow = newValue
            self._UpdateColors(None,None)
        #Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Background_SetToWanted(self):
        self._current_backgroundColor = (
                                        self._wanted_BackgroundColor[0],
                                        self._wanted_BackgroundColor[1],
                                        self._wanted_BackgroundColor[2],
                                        self._wanted_BackgroundColor[3],
                                        )
        self._current_backgroundShadowColor = (
                                        self._wanted_BackgroundShadowColor[0],
                                        self._wanted_BackgroundShadowColor[1],
                                        self._wanted_BackgroundShadowColor[2],
                                        self._wanted_BackgroundShadowColor[3],
                                        )
    def _Attribute_Background_GetColorsComparator(self):
        comparator = {
                        "_current_backgroundColor"      : self._current_backgroundColor,
                        "_current_backgroundShadowColor"      : self._current_backgroundShadowColor,
                     }
        return comparator

    def _Attribute_Background_GetColorsArguments(self):
        attributes = {
                      "_current_backgroundColor"      : self._wanted_BackgroundColor,
                      "_current_backgroundShadowColor"      : self._wanted_BackgroundShadowColor,
                     }
        return attributes
    #endregion
    pass

class Attribute_SVG:
    #region   --------------------------- DOCSTRING
    """
        Inherited class which contains all Animated
        properties specific to widgets that shows an
        SVG file

        Contains:
        - path : path to the wanted SVG
    """
    #endregion
    #region   --------------------------- MEMBERS
    _svg_path:str = None
    """
    Private variable which contains the path to the wanted
    SVG file to display
    """
    _svg_instructions = None
    """ Kivy's canvas instructions which draws the SVG """
    #endregion
    #region   --------------------------- GET SET
    #region   -- SVGFile
    @property
    def SVGFile(self) -> str:
        """[GET]:
            Returns the path to the currently shown SVG
        """
        return self._svg_path

    @SVGFile.setter
    def SVGFile(self, newValue:str) -> None:
        """[SET:]
            Sets a new path to use to get the SVG file to show
            on the widget
        Args:
            newValue (str): path to the SVG
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._svg_path):
            self._svg_path  = newValue
            self._UpdateShape()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_SVG_SetToWanted(self):
        self._current_max = self._wanted_max
        self._current_min = self._wanted_min
        self._current_value = self._wanted_Value

    def _Attribute_SVG_GetShapeComparator(self):
        comparator = {
                        "_current_max"      : self._current_max,
                        "_current_min"      : self._current_min,
                        "_current_value"      : self._current_value,
                     }
        return comparator

    def _Attribute_SVG_GetShapeArguments(self):
        # attributes = {
                        # "_current_max"      : self._wanted_max,
                        # "_current_min"      : self._wanted_min,
                        # "_current_value"      : self._wanted_Value,
                    #  }
        # return attributes
        pass
    
    def _CreateSVG(self):
        """
            Private function which creates the drawing instructions
            needed to draw the SVG in the canvas.
        """
        with self.canvas:
            self._svg_instructions = svg.svg_to_instruction_group(self._svg_path)
    #endregion
    pass

class Attribute_Shadow:
    #region   --------------------------- DOCSTRING
    """
        Inherited class which contains all Animated
        properties specific to widgets that have a shadow.
        Do not build this class, it's useless.

        Contains:
        - Elevation : Shadow elevation
        - Softness : Shadow softness
    """
    #endregion
    #region   --------------------------- MEMBERS
    _wanted_Elevation               = Shadow.Elevation.default
    """
        Private variable representing the wanted elevation value.
        Defaults to Shadow.Elevation.default
    """
    _current_elevation              = Shadow.Elevation.default
    """
        Private variable representing the current elevation value.
        Defaults to Shadow.Elevation.default
    """
    _wanted_ShadowSoftness          = Shadow.Smoothness.default
    """
        Private variable representing the wanted softness of the shadow
    """
    _current_ShadowSoftness         = Shadow.Smoothness.default
    """
        Private variable representing the current softness of the shadow
    """
    _wanted_ShadowColor     = GUIColors.CardShadow
    """
        Private variable used to store the wanted shadow color of
        the widget. Defaults to GUIColors.CardShadow.
    """
    _current_ShadowColor    = GUIColors.CardShadow
    """
        Private variable used to store the current shadow color of
        the widget. Defaults to GUIColors.CardShadow.

        Use this to update the widget's
        real primary color in your Animation binded on_progress function.
    """
    _previousShadowColor    = GUIColors.CardShadow
    """
        When the widget's showShadow is set to false, this stores what wantedColor previously was
        for when you decide to show the shadow again.
    """
    _showShadow:bool        = True
    """
        Private variable which stores if the shadow should be shown or not.
    """
    #endregion
    #region   --------------------------- GET SET
    #region   -- Elevation
    @property
    def Elevation(self) -> float:
        """[GET]:
            Returns the shown elevation of the widget
        """
        return self._wanted_Elevation

    @Elevation.setter
    def Elevation(self, newValue:float) -> None:
        """[SET:]
            Sets the wanted elevation and calls the updater.
        Args:
            newValue (float): the new elevation.
        """

        # [Step 1]: Update the shape based on the new value
        #Debug.Start("Elevation.setter")
        if(newValue != self._wanted_Elevation):
            #Debug.Log("New value saved in wanted.")
            self._wanted_Elevation  = newValue
            self._UpdateShape()
        #Debug.End()
    #endregion
    #region   -- Softness
    @property
    def ShadowSoftness(self) -> float:
        """[GET]:
            Returns the shadow softness of the widget
        """
        return self._wanted_ShadowSoftness

    @ShadowSoftness.setter
    def ShadowSoftness(self, newValue:float) -> None:
        """[SET:]
            Sets the wanted shadow softness and calls the updater.
        Args:
            newValue (float): the new elevation.
        """

        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_ShadowSoftness):
            self._wanted_ShadowSoftness  = newValue
            self._UpdateShape()
    #endregion
    #region   -- Color
    @property
    def ShadowColor(self) -> tuple:
        """[GET]:
            Returns the shadow color of the widget
        """
        # Build a temporary tuple to return to avoid pointer returns

        return (
                self._wanted_ShadowColor[0],
                self._wanted_ShadowColor[1],
                self._wanted_ShadowColor[2],
                self._wanted_ShadowColor[3],
                )

    @ShadowColor.setter
    def ShadowColor(self, newValue:tuple) -> None:
        """[SET:]
            Sets the wanted shadow color and calls the updater.
        Args:
            newValue (tuple): the new color.
        """
        # [Step 0]: Rebuild the array to avoid pointer passing
        color = (
            newValue[0],newValue[1],newValue[2],newValue[3]
        )
        # [Step 1]: Update the shape based on the new value
        if(color != self._wanted_ShadowColor):
            self._wanted_ShadowSoftness  = color
            self._UpdateShape()
    #endregion
    #region   -- Show
    @property
    def ShowShadow(self) -> bool:
        """[GET]:
            Returns if the shadow is shown or not.
            True: The widget shows a shadow
            False: The widget does not show a shadow
        """
        # Build a temporary tuple to return to avoid pointer returns
        return self._showShadow

    @ShadowColor.setter
    def ShadowColor(self, newValue:bool) -> None:
        """[SET:]
            Sets if a shadow should be shown or not.
            Will automatically change wanted_color of the shadow
            to transparent. If you change shadow color, it will
            also update this if set to transparent.
        Args:
            newValue (bool): Show shadow or not.
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._showShadow):
            if(newValue):
                self._wanted_ShadowColor = (self._previousShadowColor[0], self._previousShadowColor[1], self._previousShadowColor[2], self._previousShadowColor[3])
            else:
                self._previousShadowColor = (self._wanted_ShadowColor[0], self._wanted_ShadowColor[1], self._wanted_ShadowColor[2], self._wanted_ShadowColor[3])
                self._wanted_ShadowColor = (0,0,0,0)
            self._UpdateColors()
    #endregion
    
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Shadow_SetToWanted(self):
        self._current_elevation = self._wanted_Elevation
        self._current_ShadowSoftness = self._wanted_ShadowSoftness
        self._current_ShadowColor = self._wanted_ShadowColor

    def _Attribute_Shadow_GetShapeComparator(self):
        comparator = {
                        "_current_elevation"      : self._current_elevation,
                        "_current_ShadowSoftness" : self._current_ShadowSoftness,
                     }
        return comparator

    def _Attribute_Shadow_GetShapeArguments(self):
        attributes = {
                        "_current_elevation"      : self._wanted_Elevation,
                        "_current_ShadowSoftness" : self._wanted_ShadowSoftness,
                     }
        return attributes

    def _Attribute_Shadow_GetColorComparator(self):
        comparator = {
                        "_current_ShadowColor"      : self._current_ShadowColor,
                     }
        return comparator

    def _Attribute_Shadow_GetColorArguments(self):
        attributes = {
                        "_current_ShadowColor"      : self._wanted_ShadowColor,
                     }
        return attributes
    
    def _Attribute_Shadow_SetAttributes(self, shadowColor=None, elevation=None, softness=None, showShadow=None):
        """
            Sets all the shadow attributes of the widget to something.
            This is private, use your widgets's SetAttribute function instead.
        """
        self._wanted_ShadowColor = self._wanted_ShadowColor if (shadowColor == None) else (shadowColor[0], shadowColor[1], shadowColor[2],shadowColor[3])
        self._wanted_Elevation = self._wanted_Elevation if (elevation == None) else elevation
        self._wanted_ShadowSoftness = self._wanted_ShadowSoftness if(softness == None) else softness
        self._showShadow = self._showShadow if(showShadow==None) else showShadow
    #endregion
    pass


class Attribute_Card:
    #region   --------------------------- DOCSTRING
    """
        Inherited class which contains all Animated
        properties specific to layouts

        Contains:
        - Padding: Sets how far away from other layouts this layout is.
        - Spacing: Distance separating the widgets from each other.
        - Orientation: Orientation of the widgets within the layout. "vertical" or "horizontal"
    """
    #endregion
    #region   --------------------------- MEMBERS
    _wanted_padding: float = 25
    """ Private variable that sets how far away from other layouts this layout is. 
        Defaults to 25.
    """
    _wanted_spacing: float = 25
    """
        Private variable that sets how far away widgets contained in the layouts are from each other.
        Defaults to 25.
    """
    _current_padding: float = 25
    """
        Private variable that sets how far away from other layouts this layout is.
        Defaults to 25.
    """
    _current_spacing: float = 25
    """
        Private variable that sets how far away widgets contained in the layouts are from each other
        currently. Defaults to 25.
    """
    #endregion
    #region   --------------------------- GET SET
    #region   -- Padding
    @property
    def Padding(self) -> str:
        """[GET]:
            Returns the current padding of the layout
        """
        return self._wanted_padding

    @Padding.setter
    def Padding(self, newValue:float) -> None:
        """[SET:]
            Sets the wanted padding of the layout.
            Then calls the shape animator of the layout.
        Args:
            newValue (str): amount of padding.
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_padding):
            self._wanted_padding  = newValue
            self._UpdateShape()
    #endregion
    #region   -- Spacing
    @property
    def Spacing(self) -> str:
        """[GET]:
            Returns the current spacing of the layout
        """
        return self._wanted_spacing

    @Spacing.setter
    def Spacing(self, newValue:float) -> None:
        """[SET:]
            Sets the wanted spacing of the layout.
            Then calls the shape animator of the layout.
        Args:
            newValue (str): amount of spacing.
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_spacing):
            self._wanted_spacing  = newValue
            self._UpdateShape()
    #endregion
    #region   -- Orientation
    @property
    def Orientation(self) -> str:
        """[GET]:
            Returns the current spacing of the layout
        """
        return self._MDCard.orientation

    @Orientation.setter
    def Orientation(self, newValue:str) -> None:
        """[SET:]
            Sets the wanted spacing of the layout.
            Then calls the shape animator of the layout.
        Args:
            newValue (str): amount of spacing.
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._MDCard.orientation):
            self._MDCard.orientation  = newValue
            self._UpdateShape()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Card_SetToWanted(self):
        self._current_padding = self._wanted_padding
        self._current_spacing = self._wanted_spacing

    def _Attribute_Card_GetShapeComparator(self):
        comparator = {
                        "_current_padding"      : self._current_padding,
                        "_current_spacing"      : self._current_spacing,
                     }
        return comparator

    def _Attribute_Card_GetShapeArguments(self):
        attributes = {
                        "_current_padding"      : self._wanted_padding,
                        "_current_spacing"      : self._wanted_spacing,
                     }
        return attributes
    
    def Add_Widget(self, widgetToAdd):
        """_summary_
            Adds a widget to the card. You must build the card in the widgets attribute handler's Init Animations
        """
        self._MDCard.add_widget(widgetToAdd)
    #endregion
    pass

# UNFINISHED
class Attribute_Text:
    #region   --------------------------- DOCSTRING
    """
        Inherited class which contains all Animated
        properties specific to a widget which text
        is it's main purpose.

        Contains:
        - Text: Sets the text displayed by the widget through self.text
        - Font: Font applied to the label.
    """
    #endregion
    #region   --------------------------- MEMBERS
    _font:Font = Font()
    """Private variable storing the BRS font of the widget."""
    #endregion
    #region   --------------------------- GET SET
    #region   -- Text
    @property
    def Text(self) -> str:
        """[GET]:
            Returns the shown text of the widget.
        """
        return self.text

    @Text.setter
    def Text(self, newValue:str) -> None:
        """[SET:]
            Sets the text that the widget should
            display.
        Args:
            newValue (str): new text.
        """
        # [Step 1]: Test the new text with the old text to avoid useless program executions
        if(newValue != self.text):
            self.text  = newValue
    #endregion
    #region   -- Font
    @property
    def Font(self) -> Font:
        """[GET]:
            Returns the private font class representing
            the font used by the widget's text.
        """
        return self._font

    @Font.setter
    def Font(self, newValue:Font) -> None:
        """[SET:]
            Sets the wanted spacing of the layout.
            Then calls the shape animator of the layout.
        Args:
            newValue (str): amount of spacing.
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_spacing):
            self._wanted_spacing  = newValue
            self._UpdateShape()
    #endregion
    #region   -- Orientation
    @property
    def Orientation(self) -> str:
        """[GET]:
            Returns the current spacing of the layout
        """
        return self._MDCard.orientation

    @Orientation.setter
    def Orientation(self, newValue:str) -> None:
        """[SET:]
            Sets the wanted spacing of the layout.
            Then calls the shape animator of the layout.
        Args:
            newValue (str): amount of spacing.
        """
        # [Step 1]: Update the shape based on the new value
        if(newValue != self._MDCard.orientation):
            self._MDCard.orientation  = newValue
            self._UpdateShape()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Card_SetToWanted(self):
        self._current_padding = self._wanted_padding
        self._current_spacing = self._wanted_spacing

    def _Attribute_Card_GetShapeComparator(self):
        comparator = {
                        "_current_padding"      : self._current_padding,
                        "_current_spacing"      : self._current_spacing,
                     }
        return comparator

    def _Attribute_Card_GetShapeArguments(self):
        attributes = {
                        "_current_padding"      : self._wanted_padding,
                        "_current_spacing"      : self._wanted_spacing,
                     }
        return attributes
    
    def Add_Widget(self, widgetToAdd):
        """_summary_
            Adds a widget to the card. You must build the card in the widgets attribute handler's Init Animations
        """
        self._MDCard.add_widget(widgetToAdd)
    #endregion
    pass


class Attribute_Value:
    #region   --------------------------- DOCSTRING
    """
        Inherited class which contains all Animated
        properties specific to widgets that shows 1 value.
        Do not build this class, it's useless.

        Contains:
        - value : widget's represented value
        - max : maximum the value can reach
        - min : minimum the value can reach
    """
    #endregion
    #region   --------------------------- MEMBERS
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
    _current_max                = 100
    """ Represents the maximum the Value can reach. """
    _wanted_max                 = 100
    """ The wanted maximum of the widget"""
    _current_min                = 0
    """ Represents the minimum the Value can reach. """
    _wanted_min                 = 0
    """ The wanted minimum of the widget"""
    _startFromMiddle            = False
    """ If set to True, the middle point of the widget will be the starting point for the Filling's drawing"""
    #endregion
    #region   --------------------------- GET SET
    #region   -- Value
    @property
    def Value(self) -> int:
        """[GET]:
            Returns the shown value of the widget
        """
        return self._wanted_Value

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
        # [Step 0]: Correct the given value
        if(newValue > self._wanted_max):
            newValue = self._wanted_max
        if(newValue < self._wanted_min):
            newValue = self._wanted_max

        # [Step 1]: Update the shape based on the new value
        if(newValue != self._wanted_Value):
            self._wanted_Value  = newValue
            self._UpdateShape()
    #endregion
    #region   -- Max
    @property
    def Max(self) -> int:
        """[GET]:
            Returns the widget value's maximum.
        """
        return self._wanted_max

    @Max.setter
    def Max(self, newValue:float) -> None:
        """[SET:]
            Sets the maximum the widget's value can reach. It will automatically
            adjusts the stored values to be within the Propertie's range.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new reacheable maximum
        """

        # [Step 1]: Update the shape based on the new maximum
        if(newValue != self._wanted_max):
            self._wanted_max  = newValue

            if(self._wanted_Value > newValue):
                self._wanted_Value = newValue

            self._UpdateShape()
    #endregion
    #region   -- Min
    @property
    def Min(self) -> int:
        """[GET]:
            Returns the widget value's minimum.
        """
        return self._wanted_min

    @Min.setter
    def Min(self, newValue:float) -> None:
        """[SET:]
            Sets the minimum the widget's value can reach. It will automatically
            adjusts the stored values to be within the Propertie's range.
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes.
        Args:
            newValue (float): the new reacheable minimum
        """

        # [Step 1]: Update the shape based on the new maximum
        if(newValue != self._wanted_min):
            self._wanted_min  = newValue

            if(self._wanted_Value < newValue):
                self._wanted_Value = newValue

            self._UpdateShape()
    #endregion
    #region   -- StartFromMiddle
    @property
    def StartFromMiddle(self) -> bool:
        """[GET]:
            Returns True if the widget is drawing it's Filling starting from the middle of itself.
        """
        return self._startFromMiddle

    @StartFromMiddle.setter
    def StartFromMiddle(self, newValue:bool) -> None:
        """[SET:]
            Sets wether the Filling of the widget is drawn from an edge or from
            the middle point between the Minimum and the Maximum.
            This will force animations.
        Args:
            newValue (bool): the new drawing starting point
        """

        # [Step 1]: Update the shape based on the new starting drawing attribute
        if(newValue != self._startFromMiddle):
            self._startFromMiddle  = newValue
            self._forceAnimation = True
            self._UpdateShape()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Value_SetToWanted(self):
        self._current_max = self._wanted_max
        self._current_min = self._wanted_min
        self._current_value = self._wanted_Value

    def _Attribute_Value_GetShapeComparator(self):
        comparator = {
                        "_current_max"      : self._current_max,
                        "_current_min"      : self._current_min,
                        "_current_value"      : self._current_value,
                     }
        return comparator

    def _Attribute_Value_GetShapeArguments(self):
        attributes = {
                        "_current_max"      : self._wanted_max,
                        "_current_min"      : self._wanted_min,
                        "_current_value"      : self._wanted_Value,
                     }
        return attributes

    def TestValue(self, valueToTest) -> float:
        """
            This function allows you to do a quick verification of your
            DrawingProperties. if some members of this class get weird
            data, they'll be automatically capped by this function.

            returns the corrected value
        """
        result = True

        # Check Value
        if(valueToTest > self._wanted_max):
            return self._wanted_max

        if(valueToTest < self._wanted_min):
            return self._wanted_min

        return valueToTest
    #endregion
    pass

class Attribute_Angles:
    #region   --------------------------- DOCSTRING
    '''
        Inherited class containing all needed members and methods
        in order to add basic angles to your widget.

        Do not build this class, it's useless

        - startAngle
        - endAngle
    '''
    #endregion
    #region   --------------------------- MEMBERS
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
    _current_endAngle           = 360
    """
        Private variable representing your widget's end angle in
        degrees. Defaults to 360.

        Use this to update the widget's
        real endAngle in your Animation binded on_progress function.
    """
    _wanted_EndAngle            = 360
    """
        Private variable representing your widget's new startAngle.
        Defaults to 360.

        Only set this before starting your animation.
    """
    #endregion
    #region   --------------------------- GET SET
    #region   -- StartAngle
    @property
    def StartAngle(self) -> int:
        """[GET]:
            Returns the widget value's StartAngle.
        """
        return self._wanted_StartAngle

    @StartAngle.setter
    def StartAngle(self, newValue:float) -> None:
        """[SET:]
            Sets the Start Angle the widget's value can reach. 
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes to optimize
            your run time
        Args:
            newValue (float): the new Start Angle in degrees
        """

        # [Step 1]: Update the shape based on the new start angle
        if(newValue != self._wanted_StartAngle):
            self._wanted_StartAngle  = newValue
            self._UpdateShape()
    #endregion
    #region   -- EndAngle
    @property
    def EndAngle(self) -> int:
        """[GET]:
            Returns the widget value's EndAngle.
        """
        return self._wanted_EndAngle

    @EndAngle.setter
    def EndAngle(self, newValue:float) -> None:
        """[SET:]
            Sets the End Angle the widget's value can reach. 
            Instead of setting bunch of widget attributes one
            above the other, please use SetAttributes to optimize
            your run time
        Args:
            newValue (float): the new End Angle in degrees
        """

        # [Step 1]: Update the shape based on the new end angle
        if(newValue != self._wanted_EndAngle):
            self._wanted_EndAngle  = newValue
            self._UpdateShape()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    def _Attribute_Angles_SetToWanted(self):
        self._current_endAngle = self._wanted_EndAngle
        self._current_startAngle = self._wanted_StartAngle

    def _Attribute_Angles_GetShapeComparator(self):
        comparator = {
                        "_current_endAngle"      : self._current_endAngle,
                        "_current_startAngle"    : self._current_startAngle,
                     }
        return comparator

    def _Attribute_Angles_GetShapeArguments(self):
        attributes = {
                        "_current_endAngle"      : self._wanted_EndAngle,
                        "_current_startAngle"    : self._wanted_StartAngle,
                     }
        return attributes
    #endregion
    pass

class Attribute_Orientation:
    #region   --------------------------- DOCSTRING
    '''
        Inherited class containing all needed members and methods
        in order to add basic orientation to a widget.
        Orientation can be "Top,Bottom,Left,Right".

        Do not build this class, it's useless

        - orientation
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _orientation:str         = "Top"
    """
        Private variable representing your widget's orientation
        Note that this is not using current and wanted prefixes
        because this cannot be animated.

        Use the Get Set representative to set the orientation.
        Defaults to "Top"
    """
    #endregion
    #region   --------------------------- GET SET
    #region   -- Orientation
    @property
    def Orientation(self) -> str:
        """[GET]:
            Returns the widget orientation
            "Top,Bottom,Left,Right"
        """
        return self._orientation

    @Orientation.setter
    def Orientation(self, newValue:str) -> None:
        """[SET:]
            Sets your widget's orientation and calls the
            update shape function. It also disregards callings
            if the new value is equal to the current orientation.
        Args:
            newValue (str): the new orientation
        """
        #Debug.Start("Orientation")
        # [Step 1]: Update the shape based on the new start angle
        if(newValue != self._orientation):
            self._orientation  = newValue
            #Debug.Log("Forcing animation")
            self._forceAnimation = True
            self._UpdateShape()
        #Debug.End()
    #endregion
    #endregion
    #region   --------------------------- METHODS
    #endregion
    pass
#====================================================================#
# Sub Classes
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
    _animation_transition = "in_out_cubic"

    _animation_ShapeArguments_functions = {}
    _animation_ShapeComparator_functions = {}

    _animation_ColoArguments_functions = {}
    _animation_ColorComparator_functions = {}

    _animation_InstantAnimation_functions = {}
    """ List of attribute's functions that sets their current to wanted """
    #endregion
    #region   --------------------------- METHODS
    def _StartShapeAnimation(self, duration:float=0.5, transition:str="in_out_cubic"):
        #Debug.Start("StartShapeAnimation")
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
        arguments = {"_" : 0}
        comparator = {"_" : 0}

        for function in self._animation_ShapeArguments_functions:
            arguments.update(function())

        for function in self._animation_ShapeComparator_functions:
            comparator.update(function())

        #Debug.Log("Arguments before pop: {}".format(arguments))
        #Debug.Log("comparator before pop: {}".format(comparator))
        # endregion
        # region --- [Step 1]: Pop arguments equal to themselves
        #Debug.Log("Removing unused arguments from argument list...")
        keys_to_remove = []

        for current, wanted in arguments.items():
            if arguments[current] == comparator[current]:
                keys_to_remove.append(current)

        for key in keys_to_remove:
            arguments.pop(key)

        if(len(arguments) == 0):
            if(not self._forceAnimation):
                #Debug.Warn("No animations were made due to no attributes needing change")
                return
            else:
                self._forceAnimation = False

        # Add duration and transition
        arguments["d"] = duration
        arguments["t"] = transition
        #Debug.Log(str(arguments))
        #Debug.Log("Success")
        # endregion
        # region --- [Step 2]: Build and return the Animation to execute
        #Debug.Error("Arguments : {}".format(arguments))
        animation = Animation(**arguments)
        animation.bind(on_progress = self._AnimatingShapes)
        animation.start(self)
        # endregion
        #Debug.End()
        pass
    def _StartColorAnimation(self, duration:float=0.5, transition:str="in_out_cubic"):
        #Debug.Start("StartColorAnimation")
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
        #Debug.Log("Building original arguments for Animation")
        arguments = {"_" : 0}
        comparator = {"_" : 0}

        for function in self._animation_ColoArguments_functions:
            arguments.update(function())

        for function in self._animation_ColorComparator_functions:
            comparator.update(function())
        # endregion
        # region --- [Step 1]: Pop arguments equal to themselves
        #Debug.Log("Removing unused arguments from argument list...")
        keys_to_remove = []

        for current, wanted in arguments.items():
            if arguments[current] == comparator[current]:
                keys_to_remove.append(current)

        for key in keys_to_remove:
            arguments.pop(key)

        if(len(arguments) == 0):
            #Debug.Warn("No animations were made due to no attributes needing change")
            return
        else:
            #Debug.Log("Arguments : {}".format(arguments))
            pass

        # Add duration and transition
        arguments["d"] = duration
        arguments["t"] = transition
        #Debug.Log("Success")
        # endregion
        # region --- [Step 2]: Build and return the Animation to execute
        #Debug.Log("Generating and launching Animation()")
        #Debug.Error("Arguments : {}".format(arguments))
        animation = Animation(**arguments)
        animation.bind(on_progress = self._AnimatingColors)
        animation.start(self)
        #Debug.Log("End of function")
        # endregion
        #Debug.End()
        pass
    def _InstantAnimation(self):
        """ Will make all values equal to their wanted equivalent """
        #Debug.Start("_InstantAnimation")

        for function in self._animation_InstantAnimation_functions:
            function()

        #Debug.End()
    def _Animated_Get(self, type:str, fromTheseProperties:DrawingProperties=None):
        """
            Transfer specified currently stored value of your class's
            DrawingProperties into the Animated class for you if inherited.

            theseProperties = DrawingProperties to copy from.

            copy = from theseProperty, copy ("None","All","Colors","Shapes")
        """
        #Debug.Start("_current_Get")
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

                # if(Check(self.pos)):
                    # #Debug.Log("Gotten pos: {}".format(self.pos))
                    # self._current_pos = (self.pos[0], self.pos[1])

                # if(Check(self.size)):
                    # #Debug.Log("Gotten size: {}".format(self.size))
                    # self._current_size = (self.size[0], self.size[1])
        #Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
# Widget Builders
#====================================================================#
class BRS_ValueWidgetAttributes(
                                Attribute_Foundation,
                                Attribute_Background,
                                Attribute_Filling,
                                Attribute_Track,
                                Attribute_Value,
                                Attribute_Angles,
                                Animated
                                ):
    #region   --------------------------- DOCSTRING
    '''
        Inherited object containing standard get set
        and functions used in any BRS widgets to avoid
        useless calls.

        Your widgets should inherit this event if not all
        of it is used
    '''
    #endregion
    #region   =========================== ANIMATION CONSTRUCTOR
    def InitAnimations(self):
        """Call this at the start of your widget's __init__"""

        self._animation_ShapeArguments_functions = {
                                                    self._Attribute_Angles_GetShapeArguments,
                                                    self._Attribute_Track_GetShapeArguments,
                                                    self._Attribute_Value_GetShapeArguments,
                                                    self._Attribute_Filling_GetShapeArguments,
                                                    self._Attribute_Foundation_GetShapeArguments
                                                    }

        self._animation_ShapeComparator_functions = {
                                                    self._Attribute_Angles_GetShapeComparator,
                                                    self._Attribute_Track_GetShapeComparator,
                                                    self._Attribute_Value_GetShapeComparator,
                                                    self._Attribute_Filling_GetShapeComparator,
                                                    self._Attribute_Foundation_GetShapeComparator
                                                    }

        self._animation_ColoArguments_functions = {
                                                    self._Attribute_Filling_GetColorsArguments,
                                                    self._Attribute_Track_GetColorsArguments,
                                                    self._Attribute_Background_GetColorsArguments
                                                    }

        self._animation_ColorComparator_functions = {
                                                    self._Attribute_Filling_GetColorsComparator,
                                                    self._Attribute_Track_GetColorsComparator,
                                                    self._Attribute_Background_GetColorsComparator
                                                    }

        self._animation_InstantAnimation_functions = {
                                                    self._Attribute_Angles_SetToWanted,
                                                    self._Attribute_Track_SetToWanted,
                                                    self._Attribute_Value_SetToWanted,
                                                    self._Attribute_Filling_SetToWanted,
                                                    self._Attribute_Foundation_SetToWanted,
                                                    self._Attribute_Background_SetToWanted
                                                    }
    #endregion
    #region   --------------------------- MEMBERS
    Properties = DrawingProperties()
    #endregion
    #region   --------------------------- GET SETS
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
        #Debug.Start("[BRS_ValueWidgetAttributes]: SetAttributes")
        # [Step 0]: Set wanted animation goals
        self._wanted_FillingWidth = self._current_fillingWidth if (FillingWidth == None)   else FillingWidth
        if(self._wanted_FillingWidth <= 0):
            self._wanted_FillingWidth = 1

        self._wanted_TrackWidth   = self._current_trackWidth   if (TrackWidth == None)     else TrackWidth
        if(self._wanted_TrackWidth <= 0):
            self._wanted_TrackWidth = 1

        self._wanted_StartAngle   = self._current_startAngle   if (startAngle == None)     else startAngle
        self._wanted_EndAngle     = self._current_endAngle     if (endAngle == None)       else endAngle
        self._wanted_Value        = self._current_value        if (value == None)          else self.Properties.TestValue(value)
        self._wanted_Pos          = (self._wanted_Pos[0],self._wanted_Pos[1]) if (position == None) else (position[0],position[1])
        self._wanted_Size         = (self._wanted_Size[0],self._wanted_Size[1]) if (size == None) else (size[0],size[1])

        self.Properties.showFilling     = self.Properties.showFilling       if (showFilling == None)    else showFilling
        self.Properties.showTrack       = self.Properties.showTrack         if (showTrack == None)      else showTrack
        self.Properties.showBackground  = self.Properties.showBackground    if (showBackground == None) else showBackground

        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        #Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        if(self._useCustomFillingColor != None):
            self._wanted_FillingColor = self._useCustomFillingColor if self._showFilling else (0,0,0,0)
        else:
            self._wanted_FillingColor = StatesColors.Default.GetColorFrom(self._state) if self._showFilling else (0,0,0,0)

        if(self._useCustomTrackColor != None):
            self._wanted_TrackColor = self._useCustomTrackColor if self._showTrack else (0,0,0,0)
        else:
            self._wanted_TrackColor = StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack else (0,0,0,0)

        if(self._useCustomBackgroundColor != None):
            self._wanted_BackgroundColor = self._useCustomBackgroundColor if self._showBackground else (0,0,0,0)
        else:
            self._wanted_BackgroundColor = StatesColors.Text.GetColorFrom(self._state) if self._showBackground else (0,0,0,0)


        # [Step 2]: Start animation
        # #Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        #Debug.End()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdatePos(self, *args):
        """
            Called when the pos property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (x,y)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdatePos")
        self._wanted_Pos = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateSize(self, *args):
        """
            Called when the size property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (width,height)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdateSize")
        self._wanted_Size = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self):
        """
            Function called to setup the Animations and variables
            needed to update the widget's shape.

            Do not call this function outside of this widget
        """
        #Debug.Start("_UpdateShape")
        # [Step 0]: Getting valus from widget properties
        # self._Animated_Get("Shapes", fromTheseProperties = self.Properties)

        # [Step 1]: Checking if widget should have animations or not
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        #Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------
class BRS_BarGraphWidgetAttributes(
                                Attribute_Foundation,
                                Attribute_Background,
                                Attribute_Filling,
                                Attribute_Track,
                                Attribute_Value,
                                Attribute_Orientation,
                                Animated
                                ):
    #region   --------------------------- DOCSTRING
    '''
        Inherited object containing standard get set
        and functions used in any BRS widgets to avoid
        useless calls.

        Your widgets should inherit this event if not all
        of it is used
    '''
    #endregion
    #region   =========================== ANIMATION CONSTRUCTOR
    def InitAnimations(self):
        """Call this at the start of your widget's __init__"""

        self._animation_ShapeArguments_functions = {
                                                    self._Attribute_Track_GetShapeArguments,
                                                    self._Attribute_Value_GetShapeArguments,
                                                    self._Attribute_Filling_GetShapeArguments,
                                                    self._Attribute_Foundation_GetShapeArguments
                                                    }

        self._animation_ShapeComparator_functions = {
                                                    self._Attribute_Track_GetShapeComparator,
                                                    self._Attribute_Value_GetShapeComparator,
                                                    self._Attribute_Filling_GetShapeComparator,
                                                    self._Attribute_Foundation_GetShapeComparator
                                                    }

        self._animation_ColoArguments_functions = {
                                                    self._Attribute_Filling_GetColorsArguments,
                                                    self._Attribute_Track_GetColorsArguments,
                                                    self._Attribute_Background_GetColorsArguments
                                                    }

        self._animation_ColorComparator_functions = {
                                                    self._Attribute_Filling_GetColorsComparator,
                                                    self._Attribute_Track_GetColorsComparator,
                                                    self._Attribute_Background_GetColorsComparator
                                                    }

        self._animation_InstantAnimation_functions = {
                                                    self._Attribute_Track_SetToWanted,
                                                    self._Attribute_Value_SetToWanted,
                                                    self._Attribute_Filling_SetToWanted,
                                                    self._Attribute_Foundation_SetToWanted,
                                                    self._Attribute_Background_SetToWanted
                                                    }
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- GET SETS
    #endregion
    #region   --------------------------- METHODS
    def SetAttributes(self,
                        TrackWidth = None,
                        FillingWidth = None,
                        position = None,
                        size = None,
                        value = None,
                        showTrack = None,
                        orientation = None,
                        showBackground = None,
                        showFilling = None):
        """
            Allows you to set multiple properties at once instead of creating an animation for each one you change.
            This will only call UpdateShapes Once.
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: SetAttributes")
        # [Step 0]: Set wanted animation goals
        self._wanted_FillingWidth = self._current_fillingWidth if (FillingWidth == None)   else FillingWidth
        if(self._wanted_FillingWidth <= 0):
            self._wanted_FillingWidth = 1

        self._wanted_TrackWidth   = self._current_trackWidth   if (TrackWidth == None)     else TrackWidth
        if(self._wanted_TrackWidth <= 0):
            self._wanted_TrackWidth = 1

        self._wanted_Value        = self._current_value        if (value == None)          else self.Properties.TestValue(value)
        self._wanted_Pos          = (self._wanted_Pos[0],self._wanted_Pos[1]) if (position == None) else (position[0],position[1])
        self._wanted_Size         = (self._wanted_Size[0],self._wanted_Size[1]) if (size == None) else (size[0],size[1])

        self._showTrack = self._showTrack if(showTrack == None) else showTrack
        self._showTrack = self._showFilling if(showFilling == None) else showFilling
        self._showTrack = self._showBackground if(showBackground == None) else showBackground

        self._orientation = self._orientation if(orientation == None) else orientation

        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        #Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        self._wanted_FillingColor    = StatesColors.Default.GetColorFrom(self._state) if self._showFilling    else (0,0,0,0)
        self._wanted_TrackColor      = StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack      else (0,0,0,0)
        self._wanted_BackgroundColor = StatesColors.Text.GetColorFrom(self._state)    if self._showBackground else (0,0,0,0)

        # [Step 2]: Start animation
        # #Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        #Debug.End()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdatePos(self, *args):
        """
            Called when the pos property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (x,y)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdatePos")
        self._wanted_Pos = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateSize(self, *args):
        """
            Called when the size property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (width,height)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdateSize")
        self._wanted_Size = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self):
        """
            Function called to setup the Animations and variables
            needed to update the widget's shape.

            Do not call this function outside of this widget
        """
        #Debug.Start("_UpdateShape")
        # [Step 0]: Getting values from widget properties
        # self._Animated_Get("Shapes", fromTheseProperties = self.Properties)

        # [Step 1]: Checking if widget should have animations or not
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        #Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------
class BRS_SVGWidgetAttributes(
                                Attribute_Foundation,
                                Attribute_Background,
                                Attribute_SVG,
                                Animated
                                ):
    #region   --------------------------- DOCSTRING
    '''
        Inherited object containing standard get set
        and functions used in any BRS widgets to avoid
        useless calls.

        Your widgets should inherit this event if not all
        of it is used
    '''
    #endregion
    #region   =========================== ANIMATION CONSTRUCTOR
    def InitAnimations(self):
        """Call this at the start of your widget's __init__"""

        self._animation_ShapeArguments_functions = {
                                                    self._Attribute_Foundation_GetShapeArguments
                                                    }

        self._animation_ShapeComparator_functions = {
                                                    self._Attribute_Foundation_GetShapeComparator
                                                    }

        self._animation_ColoArguments_functions = {
                                                    self._Attribute_Background_GetColorsArguments
                                                    }

        self._animation_ColorComparator_functions = {
                                                    self._Attribute_Background_GetColorsComparator
                                                    }

        self._animation_InstantAnimation_functions = {
                                                    self._Attribute_Foundation_SetToWanted,
                                                    self._Attribute_Background_SetToWanted
                                                    }
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- GET SETS
    #endregion
    #region   --------------------------- METHODS
    def SetAttributes(self,
                        position = None,
                        size = None,
                        showBackground = None):
        """
            Allows you to set multiple properties at once instead of creating an animation for each one you change.
            This will only call UpdateShapes Once.
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: SetAttributes")
        # [Step 0]: Set wanted animation goals
        # self._wanted_FillingWidth = self._current_fillingWidth if (FillingWidth == None)   else FillingWidth
        # if(self._wanted_FillingWidth <= 0):
        #     self._wanted_FillingWidth = 1

        # self._wanted_TrackWidth   = self._current_trackWidth   if (TrackWidth == None)     else TrackWidth
        # if(self._wanted_TrackWidth <= 0):
        #     self._wanted_TrackWidth = 1

        # self._wanted_Value        = self._current_value        if (value == None)          else self.Properties.TestValue(value)
        self._wanted_Pos          = (self._wanted_Pos[0],self._wanted_Pos[1]) if (position == None) else (position[0],position[1])
        self._wanted_Size         = (self._wanted_Size[0],self._wanted_Size[1]) if (size == None) else (size[0],size[1])

        # self._showTrack = self._showTrack if(showTrack == None) else showTrack
        # self._showTrack = self._showFilling if(showFilling == None) else showFilling
        self._showTrack = self._showBackground if(showBackground == None) else showBackground

        # self._orientation = self._orientation if(orientation == None) else orientation

        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        #Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        # self._wanted_FillingColor    = StatesColors.Default.GetColorFrom(self._state) if self._showFilling    else (0,0,0,0)
        # self._wanted_TrackColor      = StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack      else (0,0,0,0)
        self._wanted_BackgroundColor = StatesColors.Text.GetColorFrom(self._state)    if self._showBackground else (0,0,0,0)

        # [Step 2]: Start animation
        # #Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        #Debug.End()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdatePos(self, *args):
        """
            Called when the pos property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (x,y)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdatePos")
        self._wanted_Pos = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateSize(self, *args):
        """
            Called when the size property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (width,height)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdateSize")
        self._wanted_Size = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self, *args):
        """
            Function called to setup the Animations and variables
            needed to update the widget's shape.

            Do not call this function outside of this widget
        """
        #Debug.Start("_UpdateShape")
        # [Step 0]: Getting values from widget properties
        # self._Animated_Get("Shapes", fromTheseProperties = self.Properties)

        # [Step 1]: Checking if widget should have animations or not
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        #Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------
class BRS_CardLayoutAttributes(
                                Attribute_Foundation,
                                Attribute_Card,
                                Attribute_Shadow,
                                Attribute_Background,
                                Animated
                                ):
    #region   --------------------------- DOCSTRING
    '''
        Inherited object containing standard get set
        and functions used in any BRS Card layouts to avoid
        useless calls.

        Your widgets should inherit this event if not all
        of it is used
    '''
    #endregion
    #region   =========================== ANIMATION CONSTRUCTOR
    def InitAnimations(self):
        """Call this at the start of your widget's __init__"""

        self._animation_ShapeArguments_functions = {
                                                    self._Attribute_Foundation_GetShapeArguments,
                                                    self._Attribute_Card_GetShapeArguments,
                                                    self._Attribute_Shadow_GetShapeArguments
                                                    }

        self._animation_ShapeComparator_functions = {
                                                    self._Attribute_Foundation_GetShapeComparator,
                                                    self._Attribute_Card_GetShapeComparator,
                                                    self._Attribute_Shadow_GetShapeComparator
                                                    }

        self._animation_ColoArguments_functions = {
                                                    self._Attribute_Background_GetColorsArguments
                                                    }

        self._animation_ColorComparator_functions = {
                                                    self._Attribute_Background_GetColorsComparator
                                                    }

        self._animation_InstantAnimation_functions = {
                                                        self._Attribute_Foundation_SetToWanted,
                                                        self._Attribute_Background_SetToWanted,
                                                        self._Attribute_Card_SetToWanted,
                                                        self._Attribute_Shadow_SetToWanted
                                                     }

        # Building the card here
        self._MDCard = MDCard()
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- GET SETS
    #endregion
    #region   --------------------------- METHODS
    def SetAttributes(self,
                        position = None,
                        size = None,
                        showBackground = None,
                        showShadow = None,
                        orientation = None,
                        padding = None,
                        spacing = None,
                        state = None,
                        shadowSoftness = None,
                        elevation = None
                        ):
        """
            Allows you to set multiple properties at once instead of creating an animation for each one you change.
            This will only call UpdateShapes Once.
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: SetAttributes")
        # [Step 0]: Set wanted animation goals
        self._Attribute_Foundation_SetAttributes(state=state,pos=position,size=size)
        self._Attribute_Shadow_SetAttributes(elevation=elevation,softness=shadowSoftness,showShadow=showShadow)

        # self._showTrack = self._showTrack if(showTrack == None) else showTrack
        # self._showTrack = self._showFilling if(showFilling == None) else showFilling
        self._showBackground = self._showBackground if(showBackground == None) else showBackground
        self._showShadow = self._showShadow if(showShadow == None) else showShadow

        self._wanted_padding = self._wanted_padding if(padding == None) else padding
        self._wanted_spacing = self._wanted_spacing if(spacing == None) else spacing

        self.Orientation = self.Orientation if(orientation == None) else orientation

        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateColors(self, *args):
        """
            Updates the color based on the widget's State
        """
        #Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        # self._wanted_FillingColor    = StatesColors.Default.GetColorFrom(self._state) if self._showFilling    else (0,0,0,0)
        # self._wanted_TrackColor      = StatesColors.Pressed.GetColorFrom(self._state) if self._showTrack      else (0,0,0,0)
        self._wanted_BackgroundColor = GUIColors.Card if self._showBackground else (0,0,0,0)
        self._wanted_BackgroundShadowColor = GUIColors.CardShadow if self._showShadow else (0,0,0,0)

        # [Step 2]: Start animation
        # #Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        #Debug.End()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdatePos(self, *args):
        """
            Called when the pos property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (x,y)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdatePos")
        self._wanted_Pos = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateSize(self, *args):
        """
            Called when the size property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (width,height)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdateSize")
        self._wanted_Size = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self, *args):
        """
            Function called to setup the Animations and variables
            needed to update the widget's shape.

            Do not call this function outside of this widget
        """
        #Debug.Start("_UpdateShape")
        # [Step 0]: Getting values from widget properties
        # self._Animated_Get("Shapes", fromTheseProperties = self.Properties)

        # [Step 1]: Checking if widget should have animations or not
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        #Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
# --------------------------------------------------
class BRS_ButtonWidgetAttributes(
                                Attribute_Foundation,
                                Attribute_Shadow,
                                Animated
                                ):
    #region   --------------------------- DOCSTRING
    '''
        Inherited object containing standard get set
        and functions used in any BRS MD buttons to avoid
        useless calls.

        Your widgets should inherit this attribute
    '''
    #endregion
    #region   =========================== ANIMATION CONSTRUCTOR
    def InitAnimations(self):
        """Call this at the start of your widget's __init__"""

        self._animation_ShapeArguments_functions =  {
                                                        self._Attribute_Foundation_GetShapeArguments,
                                                        self._Attribute_Shadow_GetShapeArguments
                                                    }

        self._animation_ShapeComparator_functions = {
                                                        self._Attribute_Foundation_GetShapeComparator,
                                                        self._Attribute_Shadow_GetShapeComparator
                                                    }

        self._animation_ColoArguments_functions =   {
                                                        self._Attribute_Shadow_GetColorArguments
                                                    }

        self._animation_ColorComparator_functions = {
                                                        self._Attribute_Shadow_GetColorComparator
                                                    }

        self._animation_InstantAnimation_functions = {
                                                        self._Attribute_Foundation_SetToWanted,
                                                        self._Attribute_Shadow_SetToWanted
                                                     }

    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- GET SETS
    #endregion
    #region   --------------------------- METHODS
    def SetAttributes(self,
                        pos = None,
                        size = None,
                        posHint = None,
                        sizeHint = None,
                        radius = None,
                        state = None,
                        showShadow = None,
                        shadowColor = None,
                        shadowElevation = None,
                        shadowSoftness = None
                        ):
        """
            Allows you to set multiple properties at once instead of creating an animation for each one you change.
            This will only call UpdateShapes Once.
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: SetAttributes")
        # [Step 0]: Set wanted animation goals
        self._Attribute_Foundation_SetAttributes(state=state,pos=pos,size=size,sizeHint=sizeHint,posHint=posHint,radius=radius)
        self._Attribute_Shadow_SetAttributes(shadowColor=shadowColor,elevation=shadowElevation,softness=shadowSoftness,showShadow=showShadow)
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateColors(self, instance, value):
        """
            Updates the color based on the widget's State
        """
        #Debug.Start("_UpdateColors")
        # [Step 0]: Set wanted animation results
        self._wanted = GUIColors.CardShadow if self._showShadow else (0,0,0,0)

        # [Step 2]: Start animation
        # #Debug.Log("[Step 2]:")
        if(self.animated):
            self._StartColorAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingColors(None, None, None)
        #Debug.End()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdatePos(self, *args):
        """
            Called when the pos property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (x,y)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdatePos")
        self._wanted_Pos = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateSize(self, *args):
        """
            Called when the size property is changed. This is called by
            itself, do not call this function yourself.

            *args = [object, (width,height)]
        """
        #Debug.Start("[BRS_ValueWidgetAttributes]: _UpdateSize")
        self._wanted_Size = (args[1][0], args[1][1])
        self._UpdateShape()
        #Debug.End()
    # ------------------------------------------------------
    def _UpdateShape(self, *args):
        """
            Function called to setup the Animations and variables
            needed to update the widget's shape.

            Do not call this function outside of this widget
        """
        #Debug.Start("_UpdateShape")
        # [Step 1]: Checking if widget should have animations or not
        if(self.animated):
            self._StartShapeAnimation()
        else:
            self._InstantAnimation()
            self._AnimatingShapes(None, None, None)
        #Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass

LoadingLog.End("attributes.py")