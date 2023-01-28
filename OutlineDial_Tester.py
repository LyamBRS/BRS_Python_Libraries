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
from kivy.uix.stencilview import StencilView

from kivymd.app import MDApp
from kivymd.uix.slider import MDSlider


import random
from BRS.GUI.Utilities.font import Font
from BRS.Utilities.states import StatesColors
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Status.Progress import Bar
from BRS.Utilities.states import States
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Status.ValueDisplay import OutlineDial, PieChartDial
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

            self.card.showTrack = TextButton(initialFont = ButtonFont, wantedText = "Hide Track")
            self.card.showFilling = TextButton(initialFont = ButtonFont, wantedText = "Hide Filling")
            self.card.showBackground = TextButton(initialFont = ButtonFont, wantedText = "Hide Background")
            self.card.switchState    = TextButton(initialFont = ButtonFont, wantedText = "Switch State")
            self.card.startingPoint      = TextButton(initialFont = ButtonFont, wantedText = "Start: Edges")

            self.card.Add_Widget(self.card.showTrack)
            self.card.Add_Widget(self.card.showFilling)
            self.card.Add_Widget(self.card.showBackground)
            self.card.Add_Widget(self.card.switchState)
            self.card.Add_Widget(self.card.startingPoint)

            self.add_widget(self.card)

            self.card.showTrack.State = States.Active
            self.card.showFilling.State = States.Active
            self.card.showBackground.State = States.Active
            self.card.switchState.State = States.Active
            self.card.startingPoint.State = States.Active

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

            self.card.valueSlider    = MDSlider(min = 0, max = 100)
            self.card.fillingWidth   = MDSlider(min = 0, max = 100)
            self.card.trackWidth     = MDSlider(min = 0, max = 100)
            self.card.startAngle     = MDSlider(min = -360, max = 360)
            self.card.endAngle       = MDSlider(min = -360, max = 360)

            self.card.valueSlider.orientation = "vertical"
            self.card.fillingWidth.orientation = "vertical"
            self.card.trackWidth.orientation = "vertical"
            self.card.startAngle.orientation = "vertical"
            self.card.endAngle.orientation = "vertical"

            self.card.valueSlider.value_track = True
            self.card.fillingWidth.value_track = True
            self.card.trackWidth.value_track = True
            self.card.startAngle.value_track = True
            self.card.endAngle.value_track = True

            self.card.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.card.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.card.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.card.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.card.endAngle.value_track_color  = StatesColors.Pressed.GetColorFrom(States.Active)

            self.card.Add_Widget(self.card.valueSlider )
            self.card.Add_Widget(self.card.fillingWidth)
            self.card.Add_Widget(self.card.trackWidth  )
            self.card.Add_Widget(self.card.startAngle  )
            self.card.Add_Widget(self.card.endAngle    )

            self.add_widget(self.card)

            with self.canvas:
                Color(0, 1, 0, 1)  # red
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

            self.card.OutlineDial = OutlineDial(min=0, max=100, endAngle=360, startAngle=0)
            self.card.OutlineDial.animated = True

            self.card.PieChartDial = PieChartDial(min=0, max=100, endAngle=360, startAngle=0)
            self.card.PieChartDial.animated = True

            self.card.Information = TextButton(initialFont=ButtonFont)
            self.card.Information.Text = "PieChartDial"

            # self.add_widget(self.Information)
            self.card.Add_Widget(self.card.OutlineDial)
            self.card.Add_Widget(self.card.PieChartDial)

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
            self.dials.card.PieChartDial.ShowTrack = False
            self.buttons.card.showTrack.State = States.Inactive
            self.buttons.card.showTrack.Text  = "Show track"
        else:
            self.dials.card.OutlineDial.ShowTrack = True
            self.dials.card.PieChartDial.ShowTrack = True
            self.buttons.card.showTrack.State = States.Active
            self.buttons.card.showTrack.Text  = "Hide track"

    def HideFilling(self):
        if(self.dials.card.OutlineDial.ShowFilling):
            self.dials.card.OutlineDial.ShowFilling = False
            self.dials.card.PieChartDial.ShowFilling = False
            self.buttons.card.showFilling.State = States.Inactive
            self.buttons.card.showFilling.Text  = "Show Filling"
        else:
            self.dials.card.OutlineDial.ShowFilling = True
            self.dials.card.PieChartDial.ShowFilling = True
            self.buttons.card.showFilling.State = States.Active
            self.buttons.card.showFilling.Text  = "Hide Filling"
    def HideBackground(self):
        if(self.dials.card.OutlineDial.ShowBackground):
            self.dials.card.OutlineDial.ShowBackground = False
            self.dials.card.PieChartDial.ShowBackground = False
            self.buttons.card.showBackground.State = States.Inactive
            self.buttons.card.showBackground.Text  = "Show Background"
        else:
            self.dials.card.OutlineDial.ShowBackground = True
            self.dials.card.PieChartDial.ShowBackground = True
            self.buttons.card.showBackground.State = States.Active
            self.buttons.card.showBackground.Text  = "Hide Background"
    def SwitchState(self):
        state = self.dials.card.OutlineDial.State

        if(state == 7):
            self.dials.card.OutlineDial.State = States.Disabled
            self.dials.card.PieChartDial.State = States.Disabled
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
            self.dials.card.PieChartDial.State = state

        # Changing the states of all the buttons
        self.buttons.card.switchState.State = self.dials.card.OutlineDial.State
        self.buttons.card.showBackground.State = self.dials.card.OutlineDial.State
        self.buttons.card.showFilling.State = self.dials.card.OutlineDial.State
        self.buttons.card.showTrack.State = self.dials.card.OutlineDial.State
        self.buttons.card.startingPoint.State = self.dials.card.OutlineDial.State

        # Changing the track color of sliders
        self.sliders.card.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        self.sliders.card.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        self.sliders.card.endAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        self.sliders.card.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
        self.sliders.card.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.card.OutlineDial.State)
    def SwitchEdges(self):
        # Inverse the current value
        self.dials.card.OutlineDial.StartFromMiddle = not self.dials.card.OutlineDial.StartFromMiddle
        self.dials.card.PieChartDial.StartFromMiddle = not self.dials.card.PieChartDial.StartFromMiddle

        # Change the text
        if(self.dials.card.OutlineDial.StartFromMiddle):
            self.buttons.card.startingPoint.Text = "Start: Middle"
        else:
            self.buttons.card.startingPoint.Text = "Start: Edges"

    def SetValue(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.PieChartDial.animated = False
        self.dials.card.OutlineDial.Value = self.sliders.card.valueSlider.value
        self.dials.card.PieChartDial.Value = self.sliders.card.valueSlider.value
        self.dials.card.Information.Text = "Value: {}".format(int(self.sliders.card.valueSlider.value))
        self.dials.card.OutlineDial.animated = True
        self.dials.card.PieChartDial.animated = True

    def SetEnd(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.PieChartDial.animated = False
        self.dials.card.PieChartDial.SetAttributes(endAngle = self.sliders.card.endAngle.value, startAngle= self.sliders.card.startAngle.value)
        self.dials.card.OutlineDial.SetAttributes(endAngle = self.sliders.card.endAngle.value, startAngle= self.sliders.card.startAngle.value)
        self.dials.card.Information.Text = "End angle: {}".format(int(self.sliders.card.endAngle.value))
        self.dials.card.OutlineDial.animated = True
        self.dials.card.PieChartDial.animated = True

    def SetStart(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.PieChartDial.animated = False
        self.dials.card.OutlineDial.SetAttributes(startAngle= self.sliders.card.startAngle.value, endAngle=self.sliders.card.endAngle.value)
        self.dials.card.PieChartDial.SetAttributes(startAngle= self.sliders.card.startAngle.value, endAngle=self.sliders.card.endAngle.value)
        self.dials.card.Information.Text = "Start angle: {}".format(int(self.sliders.card.startAngle.value))
        self.dials.card.OutlineDial.animated = True
        self.dials.card.PieChartDial.animated = True

    def SetTrackWidth(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.PieChartDial.animated = False
        self.dials.card.OutlineDial.SetAttributes(TrackWidth=self.sliders.card.trackWidth.value)
        self.dials.card.PieChartDial.SetAttributes(TrackWidth=self.sliders.card.trackWidth.value)
        self.dials.card.Information.Text = "Track: {}".format(int(self.sliders.card.trackWidth.value))
        self.dials.card.OutlineDial.animated = True
        self.dials.card.PieChartDial.animated = True

    def SetFillingWidth(self, *args):
        self.dials.card.OutlineDial.animated = False
        self.dials.card.PieChartDial.animated = False
        self.dials.card.OutlineDial.SetAttributes(FillingWidth=self.sliders.card.fillingWidth.value)
        self.dials.card.PieChartDial.SetAttributes(FillingWidth=self.sliders.card.fillingWidth.value)
        self.dials.card.Information.Text = "Filling: {}".format(int(self.sliders.card.fillingWidth.value))
        self.dials.card.OutlineDial.animated = True
        self.dials.card.PieChartDial.animated = True
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
            self.buttons.card.startingPoint.on_press = self.SwitchEdges

            self.sliders.card.valueSlider.bind(value = self.SetValue)
            self.sliders.card.startAngle.bind(value = self.SetStart)
            self.sliders.card.endAngle.bind(value = self.SetEnd)
            self.sliders.card.trackWidth.bind(value = self.SetTrackWidth)
            self.sliders.card.fillingWidth.bind(value = self.SetFillingWidth)

            self.sliders.card.valueSlider.value  = self.dials.card.OutlineDial.Value
            self.sliders.card.startAngle.value   = self.dials.card.OutlineDial.Properties.startAngle
            self.sliders.card.endAngle.value     = self.dials.card.OutlineDial.Properties.endAngle
            self.sliders.card.trackWidth.value   = self.dials.card.OutlineDial.Properties.trackWidth
            self.sliders.card.fillingWidth.value = self.dials.card.OutlineDial.Properties.fillingWidth

            Debug.End()
    #endregion

#################################################################### WIDGETS
class MainWidget(Widget):
    pass
#====================================================================#
# Application Building
#====================================================================#
class KivyUIApp(MDApp):
    def build(self):
        Debug.Start()
        Debug.Log("Building application's parameters...")
        #---------------------------------------------------------# Title
        Debug.Log("Setting Name...")
        self.title = "BRS Dial Tester"
        #---------------------------------------------------------# Window properties
        Debug.Log("Setting Window configurations...")

        Window.borderless = False
        Window.resizable = True
        Window.left = -1024
        Window.top = 600
        Window.fullscreen = 'auto'
        #---------------------------------------------------------#
        Debug.Log("Building layouts")

        self.windowLayout = WindowLayout()
        Debug.End()
        return self.windowLayout

    def run(self):
        Debug.Start()
        Debug.Warn("Kivy application called the run function")
        Debug.End()
        return super().run()

    def on_start(self):
        Debug.Start("on_start")
        Debug.End()
#====================================================================#
# Application Running
#====================================================================#
Debug.enableConsole = True
Debug.Warn(logged = "Launching KivyUIApp through .run")
KivyUIApp().run()
Debug.Warn(logged = "============================END OF SCRIPT============================")

