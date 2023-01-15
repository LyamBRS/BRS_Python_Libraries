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

import random
from BRS.GUI.Utilities.font import Font
from BRS.Utilities.states import StatesColors
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Status.Progress import Bar
from BRS.Utilities.states import States
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Status.ValueDisplay import OutlineDial, PieChartDial
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
            self.spacing = 25

            self.showTrack = TextButton(initialFont = ButtonFont, wantedText = "Hide Track")
            self.showFilling = TextButton(initialFont = ButtonFont, wantedText = "Hide Filling")
            self.showBackground = TextButton(initialFont = ButtonFont, wantedText = "Hide Background")
            self.switchState    = TextButton(initialFont = ButtonFont, wantedText = "Switch State")
            self.startingPoint      = TextButton(initialFont = ButtonFont, wantedText = "Edges")

            self.add_widget(self.showTrack)
            self.add_widget(self.showFilling)
            self.add_widget(self.showBackground)
            self.add_widget(self.switchState)
            self.add_widget(self.startingPoint)

            self.showTrack.State = States.Active
            self.showFilling.State = States.Active
            self.showBackground.State = States.Active
            self.switchState.State = States.Active
            self.startingPoint.State = States.Active

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
            self.spacing = 25
            self.orientation = "vertical"

            self.OutlineDial = OutlineDial(min=0, max=100, endAngle=360, startAngle=0)
            self.OutlineDial.animated = True

            self.PieChartDial = PieChartDial(min=0, max=100, endAngle=360, startAngle=0)
            self.PieChartDial.animated = True

            self.Information = TextButton(initialFont=ButtonFont)
            self.Information.Text = "PieChartDial"

            # self.add_widget(self.Information)
            self.add_widget(self.OutlineDial)
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
        if(self.dials.OutlineDial.ShowTrack):
            self.dials.OutlineDial.ShowTrack = False
            self.dials.PieChartDial.ShowTrack = False
            self.buttons.showTrack.State = States.Inactive
            self.buttons.showTrack.Text  = "Show track"
        else:
            self.dials.OutlineDial.ShowTrack = True
            self.dials.PieChartDial.ShowTrack = True
            self.buttons.showTrack.State = States.Active
            self.buttons.showTrack.Text  = "Hide track"

    def HideFilling(self):
        if(self.dials.OutlineDial.ShowFilling):
            self.dials.OutlineDial.ShowFilling = False
            self.dials.PieChartDial.ShowFilling = False
            self.buttons.showFilling.State = States.Inactive
            self.buttons.showFilling.Text  = "Show Filling"
        else:
            self.dials.OutlineDial.ShowFilling = True
            self.dials.PieChartDial.ShowFilling = True
            self.buttons.showFilling.State = States.Active
            self.buttons.showFilling.Text  = "Hide Filling"
    def HideBackground(self):
        if(self.dials.OutlineDial.ShowBackground):
            self.dials.OutlineDial.ShowBackground = False
            self.dials.PieChartDial.ShowBackground = False
            self.buttons.showBackground.State = States.Inactive
            self.buttons.showBackground.Text  = "Show Background"
        else:
            self.dials.OutlineDial.ShowBackground = True
            self.dials.PieChartDial.ShowBackground = True
            self.buttons.showBackground.State = States.Active
            self.buttons.showBackground.Text  = "Hide Background"
    def SwitchState(self):
        state = self.dials.OutlineDial.State

        if(state == 7):
            self.dials.OutlineDial.State = States.Disabled
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
            self.dials.OutlineDial.State = state
            self.dials.PieChartDial.State = state

        # Changing the states of all the buttons
        self.buttons.switchState.State = self.dials.OutlineDial.State
        self.buttons.showBackground.State = self.dials.OutlineDial.State
        self.buttons.showFilling.State = self.dials.OutlineDial.State
        self.buttons.showTrack.State = self.dials.OutlineDial.State
        self.buttons.startingPoint.State = self.dials.OutlineDial.State

        # Changing the track color of sliders
        self.sliders.valueSlider.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.OutlineDial.State)
        self.sliders.startAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.OutlineDial.State)
        self.sliders.endAngle.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.OutlineDial.State)
        self.sliders.trackWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.OutlineDial.State)
        self.sliders.fillingWidth.value_track_color = StatesColors.Pressed.GetColorFrom(self.dials.OutlineDial.State)
    def SwitchEdges(self):
        # Inverse the current value
        self.dials.OutlineDial.StartFromMiddle = not self.dials.OutlineDial.StartFromMiddle

        # Change the text
        if(self.dials.OutlineDial.StartFromMiddle):
            self.buttons.startingPoint.Text = "Middle"
        else:
            self.buttons.startingPoint.Text = "Edges"

    def SetValue(self, *args):
        self.dials.OutlineDial.animated = False
        self.dials.PieChartDial.animated = False
        self.dials.OutlineDial.Value = self.sliders.valueSlider.value
        self.dials.PieChartDial.Value = self.sliders.valueSlider.value
        self.dials.Information.Text = "Value: {}".format(int(self.sliders.valueSlider.value))
        self.dials.OutlineDial.animated = True
        self.dials.PieChartDial.animated = True

    def SetEnd(self, *args):
        self.dials.OutlineDial.animated = False
        self.dials.PieChartDial.animated = False
        self.dials.PieChartDial.SetAttributes(endAngle = self.sliders.endAngle.value, startAngle= self.sliders.startAngle.value)
        self.dials.OutlineDial.SetAttributes(endAngle = self.sliders.endAngle.value, startAngle= self.sliders.startAngle.value)
        self.dials.Information.Text = "End angle: {}".format(int(self.sliders.endAngle.value))
        self.dials.OutlineDial.animated = True
        self.dials.PieChartDial.animated = True

    def SetStart(self, *args):
        self.dials.OutlineDial.animated = False
        self.dials.PieChartDial.animated = False
        self.dials.OutlineDial.SetAttributes(startAngle= self.sliders.startAngle.value, endAngle=self.sliders.endAngle.value)
        self.dials.PieChartDial.SetAttributes(startAngle= self.sliders.startAngle.value, endAngle=self.sliders.endAngle.value)
        self.dials.Information.Text = "Start angle: {}".format(int(self.sliders.startAngle.value))
        self.dials.OutlineDial.animated = True
        self.dials.PieChartDial.animated = True

    def SetTrackWidth(self, *args):
        self.dials.OutlineDial.animated = False
        self.dials.PieChartDial.animated = False
        self.dials.OutlineDial.SetAttributes(TrackWidth=self.sliders.trackWidth.value)
        self.dials.PieChartDial.SetAttributes(TrackWidth=self.sliders.trackWidth.value)
        self.dials.Information.Text = "Track: {}".format(int(self.sliders.trackWidth.value))
        self.dials.OutlineDial.animated = True
        self.dials.PieChartDial.animated = True

    def SetFillingWidth(self, *args):
        self.dials.OutlineDial.animated = False
        self.dials.PieChartDial.animated = False
        self.dials.OutlineDial.SetAttributes(FillingWidth=self.sliders.fillingWidth.value)
        self.dials.PieChartDial.SetAttributes(FillingWidth=self.sliders.fillingWidth.value)
        self.dials.Information.Text = "Filling: {}".format(int(self.sliders.fillingWidth.value))
        self.dials.OutlineDial.animated = True
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
            self.buttons.startingPoint.on_press = self.SwitchEdges

            self.sliders.valueSlider.bind(value = self.SetValue)
            self.sliders.startAngle.bind(value = self.SetStart)
            self.sliders.endAngle.bind(value = self.SetEnd)
            self.sliders.trackWidth.bind(value = self.SetTrackWidth)
            self.sliders.fillingWidth.bind(value = self.SetFillingWidth)

            self.sliders.valueSlider.value  = self.dials.OutlineDial.Value
            self.sliders.startAngle.value   = self.dials.OutlineDial.Properties.startAngle
            self.sliders.endAngle.value     = self.dials.OutlineDial.Properties.endAngle
            self.sliders.trackWidth.value   = self.dials.OutlineDial.Properties.trackWidth
            self.sliders.fillingWidth.value = self.dials.OutlineDial.Properties.fillingWidth

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

