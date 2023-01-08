#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from cgitb import text
from multiprocessing.reduction import steal_handle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.graphics import Color

import random
from BRS.GUI.Utilities.font import Font
from BRS.Utilities.states import StatesColors
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Status.Progress import Bar
from BRS.Utilities.states import States
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Status.ValueDisplay import PieChartDial
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
            self.padding = 25
            self.spacing = 50

            self.showTrack = TextButton(initialFont = ButtonFont, wantedText = "Hide Track")
            self.showFilling = TextButton(initialFont = ButtonFont, wantedText = "Hide Filling")
            self.showBackground = TextButton(initialFont = ButtonFont, wantedText = "Hide Background")
            self.switchState    = TextButton(initialFont = ButtonFont, wantedText = "Switch State")

            self.add_widget(self.showTrack)
            self.add_widget(self.showFilling)
            self.add_widget(self.showBackground)
            self.add_widget(self.switchState)

            self.showTrack.State = States.Active
            self.showFilling.State = States.Active
            self.showBackground.State = States.Active
            self.switchState.State = States.Active

            with self.canvas:
                self.color = Color(0, 0, 1, 1)  # red
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

            self.padding = 50
            self.spacing = 25

            self.valueSlider    = Slider(min = 0, max = 100)
            self.fillingWidth   = Slider(min = 0, max = 100)
            self.trackWidth     = Slider(min = 0, max = 100)
            self.startAngle     = Slider(min = -360, max = 360)
            self.endAngle       = Slider(min = -360, max = 360)

            self.valueSlider.orientation = "vertical"
            self.fillingWidth.orientation = "vertical"
            self.trackWidth.orientation = "vertical"
            self.startAngle.orientation = "vertical"
            self.endAngle.orientation = "vertical"

            self.valueSlider.value_track = True
            self.fillingWidth.value_track = True
            self.trackWidth.value_track = True
            self.startAngle.value_track = True
            self.endAngle.value_track = True

            self.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(States.Active)
            self.endAngle.value_track_color  = StatesColors.Pressed.GetColorFrom(States.Active)

            self.add_widget(self.valueSlider )
            self.add_widget(self.fillingWidth)
            self.add_widget(self.trackWidth  )
            self.add_widget(self.startAngle  )
            self.add_widget(self.endAngle    )

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

            self.padding = 50
            self.spacing = 50
            self.orientation = "vertical"

            self.PieChartDial = PieChartDial(min=0, max=100, endAngle=360, startAngle=0)
            self.PieChartDial.animated = True

            self.Information = TextButton(initialFont=ButtonFont)
            self.Information.Text = "PieChartDial"


            self.add_widget(self.Information)
            self.add_widget(self.PieChartDial)
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
        if(self.dials.PieChartDial.ShowTrack):
            self.dials.PieChartDial.ShowTrack = False
            self.buttons.showTrack.State = States.Inactive
            self.buttons.showTrack.Text  = "Show track"
        else:
            self.dials.PieChartDial.ShowTrack = True
            self.buttons.showTrack.State = States.Active
            self.buttons.showTrack.Text  = "Hide track"
    def HideFilling(self):
        if(self.dials.PieChartDial.ShowFilling):
            self.dials.PieChartDial.ShowFilling = False
            self.buttons.showFilling.State = States.Inactive
            self.buttons.showFilling.Text  = "Show Filling"
        else:
            self.dials.PieChartDial.ShowFilling = True
            self.buttons.showFilling.State = States.Active
            self.buttons.showFilling.Text  = "Hide Filling"
    def HideBackground(self):
        if(self.dials.PieChartDial.ShowBackground):
            self.dials.PieChartDial.ShowBackground = False
            self.buttons.showBackground.State = States.Inactive
            self.buttons.showBackground.Text  = "Show Background"
        else:
            self.dials.PieChartDial.ShowBackground = True
            self.buttons.showBackground.State = States.Active
            self.buttons.showBackground.Text  = "Hide Background"
    def SwitchState(self):
        state = self.dials.PieChartDial.State

        if(state == 7):
            self.dials.PieChartDial.State = States.Disabled
            self.dials.Information.State = States.Disabled
            self.dials.Information.Text = "State: Disabled"
        else:
            state += 1

            if state == States.Active:
                self.dials.Information.Text = "State: Active"
            if state == States.Inactive:
                self.dials.Information.Text = "State: Inactive"
            if state == States.Warning:
                self.dials.Information.Text = "State: Warning"
            if state == States.Warning:
                self.dials.Information.Text = "State: Warning"
            if state == States.Error:
                self.dials.Information.Text = "State: Error"
            if state == States.Locked:
                self.dials.Information.Text = "State: Locked"
            if state == States.Unavailable:
                self.dials.Information.Text = "State: Unavailable"
            if state == States.Good:
                self.dials.Information.Text = "State: Good"

            self.dials.Information.State = state
            self.dials.PieChartDial.State = state

        self.buttons.switchState.State = self.dials.PieChartDial.State
        self.buttons.showBackground.State = self.dials.PieChartDial.State
        self.buttons.showFilling.State = self.dials.PieChartDial.State
        self.buttons.showTrack.State = self.dials.PieChartDial.State

        self.sliders.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.PieChartDial.State)
        self.sliders.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.PieChartDial.State)
        self.sliders.endAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.PieChartDial.State)
        self.sliders.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.PieChartDial.State)
        self.sliders.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.PieChartDial.State)

    def SetValue(self, *args):
        self.dials.PieChartDial.animated = False
        self.dials.PieChartDial.Value = self.sliders.valueSlider.value
        self.dials.Information.Text = "Value: {}".format(int(self.sliders.valueSlider.value))
        self.dials.PieChartDial.animated = True
    def SetEnd(self, *args):
        self.dials.PieChartDial.animated = False
        self.dials.PieChartDial.SetAttributes(endAngle = self.sliders.endAngle.value, startAngle= self.sliders.startAngle.value)
        self.dials.Information.Text = "End angle: {}".format(int(self.sliders.endAngle.value))
        self.dials.PieChartDial.animated = True
    def SetStart(self, *args):
        self.dials.PieChartDial.animated = False
        self.dials.PieChartDial.SetAttributes(startAngle= self.sliders.startAngle.value, endAngle=self.sliders.endAngle.value)
        self.dials.Information.Text = "Start angle: {}".format(int(self.sliders.startAngle.value))
        self.dials.PieChartDial.animated = True
    def SetTrackWidth(self, *args):
        self.dials.PieChartDial.animated = False
        self.dials.PieChartDial.SetAttributes(TrackWidth=self.sliders.trackWidth.value)
        self.dials.Information.Text = "Track: {}".format(int(self.sliders.trackWidth.value))
        self.dials.PieChartDial.animated = True
    def SetFillingWidth(self, *args):
        self.dials.PieChartDial.animated = False
        self.dials.PieChartDial.SetAttributes(FillingWidth=self.sliders.fillingWidth.value)
        self.dials.Information.Text = "Filling: {}".format(int(self.sliders.fillingWidth.value))
        self.dials.PieChartDial.animated = True
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

            self.buttons.switchState.on_press = self.SwitchState
            self.buttons.showTrack.on_press = self.HideTrack
            self.buttons.showFilling.on_press = self.HideFilling
            self.buttons.showBackground.on_press = self.HideBackground

            self.sliders.valueSlider.bind(value = self.SetValue)
            self.sliders.startAngle.bind(value = self.SetStart)
            self.sliders.endAngle.bind(value = self.SetEnd)
            self.sliders.trackWidth.bind(value = self.SetTrackWidth)
            self.sliders.fillingWidth.bind(value = self.SetFillingWidth)

            self.sliders.valueSlider.value = self.dials.PieChartDial.Value
            self.sliders.startAngle.value = self.dials.PieChartDial.Properties.startAngle
            self.sliders.endAngle.value = self.dials.PieChartDial.Properties.endAngle
            self.sliders.trackWidth.value = self.dials.PieChartDial.Properties.trackWidth
            self.sliders.fillingWidth.value = self.dials.PieChartDial.Properties.fillingWidth

            Debug.End()
    #endregion

#################################################################### WIDGETS
class MainWidget(Widget):
    pass
#====================================================================#
# Application Building
#====================================================================#
class KivyUIApp(App):
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

