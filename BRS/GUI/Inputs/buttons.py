#====================================================================#
# File Information
#====================================================================#
import os
import sys

print("buttons.py")
#====================================================================#
# Imports
#====================================================================#
from ...Utilities.states import States,StatesColors
from ...GUI.Utilities.attributes import BRS_CardLayoutAttributes, BRS_ButtonWidgetAttributes
from ...GUI.Utilities.font import Font
from ...GUI.Utilities.references import Shadow, Rounding
from ...Debug.consoleLog import Debug
from ...GUI.Utilities.colors import GUIColors

from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import RoundedRectangle
from kivy.graphics import Color
from kivy.event import EventDispatcher

from kivy.properties import (
    NumericProperty,
    ObjectProperty,
)

from kivymd.uix.button import MDRaisedButton, BaseButton
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class TextButton(ButtonBehavior, Widget):
    # region   --------------------------- DOCSTRING
    """
    This class generates a button widget with rounded edges which
    contains a text string defined by via .Text
    Args:
        ButtonBehavior (Kivy): See Kivy's documentation
        Widget (Kivy): See Kivy's documentation
    """
    #endregion
    # region   --------------------------- MEMBERS
    _state : States = States.Disabled
    """ Private variable representing the state of the widget without passing through the get/set """
    _font : Font = Font()
    """ Private font specific to this widget. Use the TextFont getset variable. Do not use this. """
    _label : Label = Label()
    """ Child label widget. Do not change the properties of this variable as the widget won't update. """
    _text : str = ""
    """ represents the text shown on the widget. Kinda useless """
    _currentColor = [0,0,0,0]
    """ current color used for Animations. This is automatically handled by the State get set """
    _wantedColor = [0,0,0,0]
    """ wanted color used for Animations. This is automatically handled by the State get set """
    heightPadding = 30
    """ How many pixels should seperate the text from the top and bottom of the button. Defaults to 30 """
    animation = Animation()
    """Represents the TextButton's animation object"""
    #endregion
    # region   --------------------------- GET SET
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
    # ------------------------------------------------------
    @property
    def Text(self) -> str:
        """ Gets you the current shown text above the widget """
        return self._text

    @Text.setter
    def Text(self, newText:str) -> None:
        """ Sets the TextButton's shown text """
        self._text = newText
        self._label.text = self._text
    # ------------------------------------------------------
    @property
    def TextFont(self) -> Font:
        """ Returns the button's Font class """
        return self._font

    @TextFont.setter
    def TextFont(self, newFont:Font) -> None:
        """ Copies a font into the widget's label and saves it in the widget for references and drawings """
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
    # region   --------------------------- METHODS
    def _UpdateColors(self, instance, value):
        """
            Updates the color of the TextButton based on Kivy's state values 
            (down or up). Do not call this function, it calls itself when
            you set the widget's state or it is pressed.
        """
        Debug.Start()
        if self.state == "down":  # if the button is being pressed
            wantedColor       = StatesColors.Pressed.GetColorFrom(self.State)
            self._label.color = StatesColors.Text.GetColorFrom(self.State)
            duration = 0
        else:
            wantedColor = StatesColors.Default.GetColorFrom(self.State)
            self._label.color = StatesColors.Text.GetColorFrom(self.State)
            duration = 0.3

        self._wantedColor = wantedColor
        self._currentColor = self.color.rgba

        self.animation.stop_all(self)
        self.animation = Animation(_currentColor = self._wantedColor, duration = duration)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)
        Debug.End()
    # ------------------------------------------------------
    def _Animating(self, animation, value, theOtherOne):
        """ Called when Animations are executed """
        self.color.rgba = self._currentColor
    # ------------------------------------------------------
    def _UpdateShape(self, *args):
        """_summary_
            Updates the shape of the widget whenever it's
            attributes are changed. (pos/size)
        """
        Debug.Start("TextButton: _UpdateShape")
        
        Debug.Log("pos: {}".format(self.pos))
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.radius, self.radius, self.radius, self.radius]
        self._label.size = self.size
        self._label.pos = self.pos
        Debug.End()
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
#====================================================================#
def Get_RaisedButton(text:str=""):
    """
        Attempting to uniformize KivyMD buttons when building the application
        rather than manually setting all the button's values individually each time.
    """

    # Create the button to return
    button = MDRaisedButton(text=text)
    button.size_hint_min_y = 0
    button.size_hint_min_x = 0
    button.size_hint_max_y = 1
    button.size_hint_max_x = 1
    button.shadow_color =  GUIColors.CardShadow

    # button.size_hint_max = (1,1)
    # button.size_hint_min = (0,0)
    # button.size_hint = (None,None)

    return button























'''
class FloatingTextButton(BRS_ButtonWidgetAttributes, Widget):
    #region   --------------------------- DOCSTRING
    """ 
        This class builds a simple, Material design floating button.
        It has BRS_ButtonWidgetAttributes.

        You can directly access the MD button through self.button in order to 
        set bindings for on_press, on_release for example.

        This class sole purpose is to interface custom BRS attributes easily
        without needing to redefine 1000 things about the button manually.

        However, these button should not be used inside of cards, but rather outside of them.
    """
    #endregion
    #region   --------------------------- MEMBERS
    _default_md_bg_color = None
    _default_md_bg_color_disabled = None
    _default_theme_text_color = "Custom"
    _default_text_color = "PrimaryHue"
    #endregion
    #region   --------------------------- METHODS
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
        Debug.Log("Setting widget to current values")
        self.button.elevation = self._current_elevation
        self.button.shadow_softness = self._current_ShadowSoftness
        self.button.radius = self._current_radius

        # [Step 2]: Update background's positions
        self.pos   = self.button.pos#(self._current_pos[0], self._current_pos[1])
        self.size  = self.button.size#(self._current_size[0], self._current_size[1])

        Debug.Warn(f"Elevation is now: {self.button.elevation}")
        Debug.Warn(f"Radius: {self.button.radius}")
        Debug.Warn(f"Shadow_softness: {self.button.shadow_softness}")
        Debug.Log("shadow_color = {}".format(self.buttonshadow_color))
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        # self.md_bg_color = self._current_backgroundColor
        self.button.shadow_color = self._current_ShadowColor
        Debug.Log("shadow_color = {}".format(self.button.shadow_color))
        Debug.End()
    # ------------------------------------------------------
    def _HandlePressing(self, *args):
        """
            Called when on_press is called
        """
        Debug.Start("_HandlePressing")

        if(self.state == "normal"):
            Debug.Log("Setting elevation to pressed")
            self.Elevation = Shadow.Elevation.pressed
        else:
            Debug.Log("Setting elevation to default")
            self.Elevation = Shadow.Elevation.default

        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 initialState = States.Disabled,
                 text = "",
                 **kwargs):
        super(FloatingTextButton, self).__init__(**kwargs)
        Debug.Start("FloatingTextButton")
        #region --------------------------- Initial Check ups
        self.InitAnimations()
        x = self.pos[0]
        y = self.pos[1]
        w = self.size[0]
        h = self.size[1]

        self.size_hint_min = (0,0)
        self.size_hint_max = (1,1)
        #endregion
        #region --------------------------- Set Variables
        Debug.Log("Setting internal variables to new specified values")
        self._state = initialState
        #endregion
        #region --------------------------- Create MD Button
        self.button = MDRaisedButton(text = text)

        self.button.shadow_softness = Shadow.Smoothness.default
        self.button.radius = Rounding.Buttons.default
        self.button.elevation = self._current_elevation

        self.button.size_hint_max = (1,1)
        self.button.size_hint_min = (1,1)
        #endregion
        #region --------------------------- Set Binds
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Binding events to FloatingTextButton")
            self.bind(pos = self._UpdatePos, size = self._UpdateSize)#,state = self._HandlePressing)

        #endregion
        #region --------------------------- Set Animation Properties
        # Debug.Log("Setting FloatingTextButton's color animation properties")

        #self._current_backgroundColor       = self.md_bg_color
        #self._wanted_BackgroundColor        = self.md_bg_color

        Debug.Log("Setting FloatingTextButton's shape animation properties")

        self._current_pos           = (x, y)
        self._wanted_Pos            = (x, y)

        self._current_size          = (w, h)
        self._wanted_Size           = (w, h)

        self._current_pos_hint      = (x, y)
        self._wanted_Pos_hint       = (x, y)

        self._current_size_hint     = (w, h)
        self._wanted_Size_hint      = (w, h)

        self.add_widget(self.button)

        #endregion
        Debug.End()
    #endregion
    pass
'''