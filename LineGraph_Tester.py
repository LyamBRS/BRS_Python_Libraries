#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.graphics import Line, Ellipse, Color

from kivymd.app import MDApp

import random
from BRS.GUI.Utilities.font import Font
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from BRS.GUI.Status.Indicators import SVGDisplay
from BRS.Utilities.states import StatesColors,States
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Containers.cards import WidgetCard
#====================================================================#
# Configuration
#====================================================================#
# region -- Font
ButtonFont = Font()
ButtonFont.isBold = True
ButtonFont.size = "32sp"
# endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class ButtonLayout(BoxLayout):
    #region   --------------------------- DOCSTRING
    ''' Layout inside of which buttons for dial testing are located
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    def showTrack(self):
        """ Called when the Show track button is pressed """

        # Increase the valueSlider's value here

    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("ButtonLayout")
            super(ButtonLayout, self).__init__(**kwargs)

            self.orientation = "vertical"
            self.padding = 10
            self.spacing = 25

            self.card = WidgetCard()
            self.card.Orientation = "vertical"

            self.card.showTrack          = TextButton(initialFont = ButtonFont, wantedText = "Hide Track")
            self.card.showFilling        = TextButton(initialFont = ButtonFont, wantedText = "Hide Filling")
            self.card.showBackground     = TextButton(initialFont = ButtonFont, wantedText = "Hide Background")
            self.card.switchState        = TextButton(initialFont = ButtonFont, wantedText = "Switch State")
            self.card.switchOrientation  = TextButton(initialFont = ButtonFont, wantedText = "Orientation")
            self.card.startingPoint      = TextButton(initialFont = ButtonFont, wantedText = "Edges")

            self.card.Add_Widget(self.card.showTrack)
            self.card.Add_Widget(self.card.showFilling)
            self.card.Add_Widget(self.card.showBackground)
            self.card.Add_Widget(self.card.switchState)
            self.card.Add_Widget(self.card.switchOrientation)
            self.card.Add_Widget(self.card.startingPoint)

            self.card.showTrack.State = States.Active
            self.card.showFilling.State = States.Active
            self.card.showBackground.State = States.Active
            self.card.switchState.State = States.Active
            self.card.switchOrientation.State = States.Active
            self.card.startingPoint.State = States.Active
            
            self.add_widget(self.card)

            Debug.End()
    #endregion

class SliderLayout(BoxLayout):
    #region   --------------------------- DOCSTRING
    ''' Layout inside of which sliders for dial testing are located
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("SliderLayout")
            super(SliderLayout, self).__init__(**kwargs)

            self.padding = 10
            self.spacing = 25
            
            self.card = WidgetCard()

            self.card.valueSlider    = Slider(min = 0, max = 100)
            self.card.fillingWidth   = Slider(min = 0, max = 100)
            self.card.trackWidth     = Slider(min = 0, max = 100)
            # self.startAngle     = Slider(min = -360, max = 360)
            # self.endAngle       = Slider(min = -360, max = 360)

            self.card.valueSlider.orientation = "vertical"
            self.card.fillingWidth.orientation = "vertical"
            self.card.trackWidth.orientation = "vertical"
            # self.startAngle.orientation = "vertical"
            # self.endAngle.orientation = "vertical"

            self.card.valueSlider.value_track = True
            self.card.fillingWidth.value_track = True
            self.card.trackWidth.value_track = True
            # self.startAngle.value_track = True
            # self.endAngle.value_track = True

            self.card.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.card.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.card.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            # self.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            # self.endAngle.value_track_color  = StatesColors.Pressed.GetColorFrom(States.Active)

            self.card.Add_Widget(self.card.valueSlider )
            self.card.Add_Widget(self.card.fillingWidth)
            self.card.Add_Widget(self.card.trackWidth  )
            # self.add_widget(self.startAngle  )
            # self.add_widget(self.endAngle    )

            self.add_widget(self.card)
            Debug.End()
    #endregion

class DialLayout(BoxLayout):
    #region   --------------------------- DOCSTRING
    ''' Layout inside of which show cased dials are located
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("DialLayout")
            super(DialLayout, self).__init__(**kwargs)

            self.padding = 10
            self.spacing = 25
            self.orientation = "vertical"

            self.card = WidgetCard()
            self.card.Orientation = "vertical"

            self.card.OutlineDial = LineGraph(min=0, max=100)
            self.card.OutlineDial.animated = True

            self.card.Information = TextButton(initialFont=ButtonFont)
            self.card.Information.Text = "LineGraph"

            # self.SVG = SVGDisplay(file="C:\\Users\\cous5\\Documents\\BRS_Documents\\Librairies\\Icons\\Applications\\Icons_BRS\\Logos\\UniLetters\\BRS_B.svg")

            # self.add_widget(self.SVG)
            self.card.Add_Widget(self.card.Information)
            self.card.Add_Widget(self.card.OutlineDial)

            self.add_widget(self.card)
            Debug.End()
    #endregion

class WindowLayout(BoxLayout):
    #region   --------------------------- DOCSTRING
    ''' Layout inside of which all layouts are located
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    def HideTrack(self):
        if(self.dials.card.OutlineDial.ShowTrack):
            self.dials.card.OutlineDial.ShowTrack = False
            self.buttons.card.showTrack.State = States.Inactive
            self.buttons.card.showTrack.Text  = "Show track"
        else:
            self.dials.card.OutlineDial.ShowTrack = True
            self.buttons.card.showTrack.State = States.Active
            self.buttons.card.showTrack.Text  = "Hide track"

    def HideFilling(self):
        if(self.dials.card.OutlineDial.ShowFilling):
            self.dials.card.OutlineDial.ShowFilling = False
            self.buttons.card.showFilling.State = States.Inactive
            self.buttons.card.showFilling.Text  = "Show Filling"
        else:
            self.dials.card.OutlineDial.ShowFilling = True
            self.buttons.card.showFilling.State = States.Active
            self.buttons.card.showFilling.Text  = "Hide Filling"
    def HideBackground(self):
        if(self.dials.card.OutlineDial.ShowBackground):
            self.dials.card.OutlineDial.ShowBackground = False
            self.buttons.card.showBackground.State = States.Inactive
            self.buttons.card.showBackground.Text  = "Show Background"
        else:
            self.dials.card.OutlineDial.ShowBackground = True
            self.buttons.card.showBackground.State = States.Active
            self.buttons.card.showBackground.Text  = "Hide Background"
    def SwitchState(self):
        state = self.dials.card.OutlineDial.State

        if(state == 7):
            self.dials.card.OutlineDial.State = States.Disabled
            self.dials.card.Information.State = States.Disabled
            self.dials.card.Information.Text = "State: Disabled"
        else:
            state += 1

            if state == States.Active:
                self.dials.card.Information.Text = "State: Active"
            if state == States.Inactive:
                self.dials.card.Information.Text = "State: Inactive"
            if state == States.Warning:
                self.dials.card.Information.Text = "State: Warning"
            if state == States.Warning:
                self.dials.card.Information.Text = "State: Warning"
            if state == States.Error:
                self.dials.card.Information.Text = "State: Error"
            if state == States.Locked:
                self.dials.card.Information.Text = "State: Locked"
            if state == States.Unavailable:
                self.dials.card.Information.Text = "State: Unavailable"
            if state == States.Good:
                self.dials.card.Information.Text = "State: Good"

            self.dials.card.Information.State = state
            self.dials.card.OutlineDial.State = state

        # Changing the states of all the buttons
        self.buttons.card.switchState.State = self.dials.card.OutlineDial.State
        self.buttons.card.showBackground.State = self.dials.card.OutlineDial.State
        self.buttons.card.showFilling.State = self.dials.card.OutlineDial.State
        self.buttons.card.showTrack.State = self.dials.card.OutlineDial.State
        self.buttons.card.switchOrientation.State = self.dials.card.OutlineDial.State
        self.buttons.card.startingPoint.State = self.dials.card.OutlineDial.State

        # Changing the track color of sliders
        self.sliders.card.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        # self.sliders.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        # self.sliders.endAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        self.sliders.card.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        self.sliders.card.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
    def SwitchOrientation(self):
        # Get the current orientation
        orientation = self.dials.card.OutlineDial.Orientation

        if(orientation == "Top"):
            self.dials.card.OutlineDial.Orientation = "Left"
            self.dials.card.Information.Text = "Left"
        elif(orientation == "Left"):
            self.dials.card.OutlineDial.Orientation = "Bottom"
            self.dials.card.Information.Text = "Bottom"
        elif(orientation == "Bottom"):
            self.dials.card.OutlineDial.Orientation = "Right"
            self.dials.card.Information.Text = "Right"
        elif(orientation == "Right"):
            self.dials.card.OutlineDial.Orientation = "Top"
            self.dials.card.Information.Text = "Top"
    def SwitchEdges(self):
        # Inverse the current value
        self.dials.card.OutlineDial.StartFromMiddle = not self.dials.card.OutlineDial.StartFromMiddle

        # Change the text
        if(self.dials.card.OutlineDial.StartFromMiddle):
            self.buttons.card.startingPoint.Text = "Middle"
        else:
            self.buttons.card.startingPoint.Text = "Edges"

    def SetValue(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.OutlineDial.Value = self.sliders.card.valueSlider.value
        self.dials.card.Information.Text = "Value: {}".format(int(self.sliders.card.valueSlider.value))
        self.dials.card.OutlineDial.animated = True

    # def SetEnd(self, *args):
    #     self.dials.card.OutlineDial.animated = False
    #     self.dials.card.OutlineDial.SetAttributes(endAngle = self.sliders.endAngle.value, startAngle= self.sliders.startAngle.value)
    #     self.dials.card.Information.Text = "End angle: {}".format(int(self.sliders.endAngle.value))
    #     self.dials.card.OutlineDial.animated = True

    # def SetStart(self, *args):
    #     self.dials.card.OutlineDial.animated = False
    #     self.dials.card.OutlineDial.SetAttributes(startAngle= self.sliders.startAngle.value, endAngle=self.sliders.endAngle.value)
    #     self.dials.card.Information.Text = "Start angle: {}".format(int(self.sliders.startAngle.value))
    #     self.dials.card.OutlineDial.animated = True

    def SetTrackWidth(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.OutlineDial.SetAttributes(TrackWidth=self.sliders.card.trackWidth.value)
        self.dials.card.Information.Text = "Track: {}".format(int(self.sliders.card.trackWidth.value))
        self.dials.card.OutlineDial.animated = True

    def SetFillingWidth(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.OutlineDial.SetAttributes(FillingWidth=self.sliders.card.fillingWidth.value)
        self.dials.card.Information.Text = "Filling: {}".format(int(self.sliders.card.fillingWidth.value))
        self.dials.card.OutlineDial.animated = True
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("WindowLayout")
            super(WindowLayout, self).__init__(**kwargs)

            self.buttons = ButtonLayout()
            self.dials   = DialLayout()
            self.sliders = SliderLayout()

            self.add_widget(self.buttons)
            self.add_widget(self.dials)
            self.add_widget(self.sliders)

            self.buttons.card.switchState.on_press = self.SwitchState
            self.buttons.card.showTrack.on_press = self.HideTrack
            self.buttons.card.showFilling.on_press = self.HideFilling
            self.buttons.card.showBackground.on_press = self.HideBackground
            self.buttons.card.switchOrientation.on_press = self.SwitchOrientation
            self.buttons.card.startingPoint.on_press = self.SwitchEdges

            self.sliders.card.valueSlider.bind(value = self.SetValue)
            self.sliders.card.trackWidth.bind(value = self.SetTrackWidth)
            self.sliders.card.fillingWidth.bind(value = self.SetFillingWidth)

            self.sliders.card.valueSlider.value  = self.dials.card.OutlineDial.Value
            self.sliders.card.trackWidth.value   = self.dials.card.OutlineDial.TrackWidth
            self.sliders.card.fillingWidth.value = self.dials.card.OutlineDial.FillingWidth

            Debug.End()
    #endregion

#################################################################### WIDGETS
class MainWidget(Widget):
    pass
#====================================================================#
# Application Building
#====================================================================#
# class KivyUIApp(MDApp):
#     def build(self):
#         Debug.Start()
#         Debug.Log("Building application's parameters...")
#         #---------------------------------------------------------# Title
#         Debug.Log("Setting Name...")
#         self.title = "BRS Dial Tester"
#         #---------------------------------------------------------# Window properties
#         Debug.Log("Setting Window configurations...")

#         Window.borderless = False
#         Window.resizable = True
#         # Window.left = -1024
#         # Window.top = 600
#         Window.fullscreen = 'auto'
#         Window.clearcolor = (1,1,1,1)
#         #---------------------------------------------------------#
#         Debug.Log("Building layouts")

#         self.windowLayout = WindowLayout()
#         Debug.End()
#         return self.windowLayout

#     def run(self):
#         Debug.Start()
#         Debug.Warn("Kivy application called the run function")
#         Debug.End()
#         return super().run()

#     def on_start(self):
#         Debug.Start("on_start")
#         Debug.End()
# #====================================================================#
# # Application Running
# #====================================================================#
# Debug.enableConsole = True
# Debug.Warn(logged = "Launching KivyUIApp through .run")
# KivyUIApp().run()
# Debug.Warn(logged = "============================END OF SCRIPT============================")

