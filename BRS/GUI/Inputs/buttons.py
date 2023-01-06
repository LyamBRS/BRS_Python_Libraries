#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from BRS.Utilities.states import States,StatesColors
from BRS.GUI.Utilities.font import Font
from BRS.Debug.consoleLog import Debug

from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import RoundedRectangle
from kivy.graphics import Color
from kivy.event import EventDispatcher
from kivy.uix.label import Label
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class TextButton(ButtonBehavior, Widget):
    #region   --------------------------- DOCSTRING
    """
    This class generates a button widget with rounded edges which
    contains a text string defined by via Text
    Args:
        ButtonBehavior (Kivy): See Kivy's documentation
        Widget (Kivy): See Kivy's documentation
    """
    #endregion
    #region   --------------------------- MEMBERS
    _state : States = States.Disabled
    _font : Font = Font()
    _label : Label = Label()
    _text : str = ""
    _currentColor = [0,0,0,0]
    _wantedColor = [0,0,0,0]
    heightPadding = 30
    #endregion
    #region   --------------------------- GET SET
    @property
    def State(self) -> int:
        return self._state

    @State.setter
    def State(self, newState:States) -> None:
        #Save new state in private variable
        self._state = newState
        self._UpdateColors(None,None)
    # ------------------------------------------------------
    @property
    def Text(self) -> str:
        return self._text

    @Text.setter
    def Text(self, newText:str) -> None:
        self._text = newText
        self._label.text = self._text
    # ------------------------------------------------------
    @property
    def TextFont(self) -> Font:
        return self._font

    @TextFont.setter
    def TextFont(self, newFont:Font) -> None:
        self._font.GetFrom(thatFont = newFont)
        self._label.font_blended    = self._font.blended
        self._label.font_context    = self._font.context
        self._label.font_family     = self._font.family
        self._label.font_hinting    = self._font.hinting
        self._label.font_size       = self._font.size
        self._label.font_kerning    = self._font.kerning
        self._label.font_name       = self._font.name
        self._label.bold            = self._font.isBold
        self._label.italic          = self._font.isItalic
        self._label.strikethrough   = self._font.isStrikethrough
        self._label.underline       = self._font.isUnderline
        #Visually update the text with the new font
        self._label.text            = self._text
        self.height = self._font.size
        self.size = (self.width, self.height + self.heightPadding)
    #endregion
    #region   --------------------------- METHODS
    def _UpdateColors(self, instance, value):
        Debug.Start()
        if self.state == "down":  # if the button is being pressed
            Debug.Warn("{} is pressed".format(self._label.text))
            wantedColor = StatesColors.Pressed.GetColorFrom(self.State)
            self._label.color = StatesColors.Text.GetColorFrom(self.State)
        else:
            Debug.Warn("{} is released".format(self._label.text))
            wantedColor = StatesColors.Default.GetColorFrom(self.State)
            self._label.color = StatesColors.Text.GetColorFrom(self.State)

        self._wantedColor = wantedColor
        self._currentColor = self.color.rgba

        self.animation = Animation(_currentColor = self._wantedColor, duration = 0.1)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)
        Debug.End()
    # ------------------------------------------------------
    def _Animating(self, animation, value, theOtherOne):
        self.color.rgba = self._currentColor
        print(self._currentColor)
    # ------------------------------------------------------
    def _UpdateShape(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.radius, self.radius, self.radius, self.radius]
        self._label.size = self.size
        self._label.pos = self.pos
    # ------------------------------------------------------
    #endregion
    # region   --------------------------- CONSTRUCTOR
    def __init__(self, radius = 10, initialState = States.Disabled, initialFont = Font(), wantedText="", **kwargs):
        super(TextButton, self).__init__(**kwargs)
        Debug.Start()
        #region --------------------------- Set Variables
        Debug.Log("Setting Textbutton's variables...")
        self.size = (self.width, self._font.size)
        self.height = self.height + self.heightPadding
        self._label = Label(pos = self.pos)
        self.radius = radius
        #endregion
        #region --------------------------- Set Classes
        Debug.Log("Setting Textbutton's Classes...")
        #self.TextFont(self.font)
        #self.set_Label(wantedText)
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Setting Textbutton's Canvas...")
        with self.canvas:
            # Color setups and variables
            self.color = Color(rgba = StatesColors.Default.GetColorFrom(self._state))
            self._currentColor = self.color.rgba
            self._wantedColor = self.color.rgba

            # Rectangle making
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.radius, self.radius, self.radius, self.radius])

            # Binding events 
            self.bind(pos=self._UpdateShape, size=self._UpdateShape)
            self.bind(state=self._UpdateColors)
        #endregion
        #region --------------------------- Set Widgets
        Debug.Log("Setting Textbutton's children widgets...")
        self._label.color = StatesColors.Text.GetColorFrom(thatState=self.State)
        self.add_widget(self._label)
        Debug.Log("Success")
        #endregion
        #region --------------------------- Set GetSets
        Debug.Log("Setting Textbutton's GetSets variables")
        self.TextFont = initialFont
        self.Text = wantedText
        self.State = initialState
        Debug.Warn("TextButton successfully created")
        #endregion
        Debug.End()
    #endregion
    pass