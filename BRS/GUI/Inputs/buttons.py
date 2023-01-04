#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from BRS.Utilities.states import States,StatesColors
from BRS.GUI.Utilities.font import Font


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
class RoundedButton(ButtonBehavior, Widget):
    #region   --------------------------- DOCSTRING
    #endregion
    #region   --------------------------- MEMBERS
    State : States = States.Disabled
    font : Font = Font()
    label : Label = Label()
    Text : str = ""
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, radius = 10, initialState = States.Disabled, initialFont = Font(), wantedText="", **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        #region --------------------------------------# Set Variables
        self.radius = radius
        self.font = initialFont
        self.State = initialState
        self.label = Label(pos = self.pos)
        #endregion
        #region --------------------------------------# Set Classes
        self.set_Font(self.font)
        self.set_Label(wantedText)
        #endregion
        #region --------------------------------------# Set Canvas
        with self.canvas:
            self.color = Color(rgba = StatesColors.Default.GetColorFrom(self.State))  # set the initial color to green
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.radius, self.radius, self.radius, self.radius])
            self.bind(pos=self.update_rect, size=self.update_rect)
            self.bind(state=self.update_color)  # bind the state property to the update_color method
        #endregion
        #region --------------------------------------# Set Widgets
        self.label.color = StatesColors.Text.GetColorFrom(thatState=self.State)
        self.add_widget(self.label)
        #endregion
    #endregion

    #region ------------------------------------------# UPDATES
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.radius, self.radius, self.radius, self.radius]
        self.label.pos = self.pos

    def update_color(self, instance, value):
        if self.state == "down":  # if the button is being pressed
            self.color.rgba = StatesColors.Pressed.GetColorFrom(self.State)
            self.label.color = StatesColors.Text.GetColorFrom(self.State)
        else:
            self.color.rgba = StatesColors.Default.GetColorFrom(self.State)
            self.label.color = StatesColors.Text.GetColorFrom(self.State)
    #endregion

    #region #------------------------------------------# BUILDING
    def set_Font(self, font:Font):
        self.font = font
        self.label.font_blended = font.blended
        self.label.font_context = font.context
        self.label.font_family = font.family
        self.label.font_hinting = font.hinting
        self.label.font_size = font.size
        self.label.font_kerning = font.kerning
        self.label.font_name = font.name
        self.label.bold = font.isBold
        self.label.italic = font.isItalic
        self.label.strikethrough = font.isStrikethrough
        self.label.underline = font.isUnderline

    def set_State(self, wantedState:States):
        self.State = wantedState
        self.label.color = StatesColors.Text.GetColorFrom(self.State)
        self.rect.rgba =   StatesColors.Default.GetColorFrom(self.State)

    def set_Label(self, wantedText=""):
        self.label.text = wantedText
    #endregion
    pass