#################################################################### IMPORTS
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window

import random
from BRS.GUI.Utilities.font import Font
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Status.Progress import Bar
from BRS.Utilities.states import States
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Status.ValueDisplay import PieChartDial
#################################################################### Configs
amogusFont = Font()
amogusFont.isBold = True
#################################################################### GridLayout
class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        Debug.Start("MyGridLayout")
        # Call gridlayout constructor
        super(MyGridLayout, self).__init__(**kwargs)
        self.col = 1
        self.size = (Window.width,Window.height)

        # Add the RoundedButton widget
        Debug.Log("Initializing the main TextButton")
        self.rounded_button = TextButton()

        self.rounded_button.Text = "Test new coordinates"
        self.rounded_button.width = 200
        x = (Window.width/2) - self.rounded_button.width/2
        y = (Window.height/2) - self.rounded_button.height/2
        self.rounded_button.pos = (x,y)
        self.rounded_button.on_press = self.GetNewDialCoordinates
        self.add_widget(self.rounded_button)  # add the RoundedButton widget to the MyGridLayout widget

        #region - States Buttons
        Debug.Log("Initializing State changers rounded text buttons")
        self.SetToDisable       = TextButton(wantedText = "Disabled",   initialState = States.Disabled,     initialFont = amogusFont, radius=22)
        self.SetToWarning       = TextButton(wantedText = "Warning",    initialState = States.Warning,      initialFont = amogusFont, radius=22)
        self.SetToActive        = TextButton(wantedText = "Active",     initialState = States.Active,       initialFont = amogusFont, radius=22)
        self.SetToInactive      = TextButton(wantedText = "Inactive",   initialState = States.Inactive,     initialFont = amogusFont, radius=22)
        self.SetToError         = TextButton(wantedText = "Error",      initialState = States.Error,        initialFont = amogusFont, radius=22)
        self.SetToLocked        = TextButton(wantedText = "Locked",     initialState = States.Locked,       initialFont = amogusFont, radius=22)
        self.SetToUnavailable   = TextButton(wantedText = "Unavailable",initialState = States.Unavailable,  initialFont = amogusFont, radius=22)
        self.SetToGood          = TextButton(wantedText = "Good",       initialState = States.Good,         initialFont = amogusFont, radius=22)
        Debug.Log("Success")

        Debug.Log("Success")
        self.SetToDisable.pos = ('1sp',0)
        self.SetToWarning.pos = ('125sp',0)
        self.SetToActive.pos = ('250sp', 0)
        self.SetToInactive.pos = ('375sp', 0)
        self.SetToError.pos = ('500sp', 0)
        self.SetToLocked.pos = ('625sp', 0)
        self.SetToUnavailable.pos = ('750sp', 0)
        self.SetToGood.pos = ('875sp', 0)
        Debug.Log("Success")

        Debug.Log("Overwriting space changer's press events")
        self.SetToDisable.on_press = self.SetStateTo_Disable
        self.SetToWarning.on_press = self.SetStateTo_Warning
        self.SetToActive.on_press = self.SetStateTo_Active
        self.SetToInactive.on_press = self.SetStateTo_Inactive
        self.SetToError.on_press = self.SetStateTo_Error
        self.SetToLocked.on_press = self.SetStateTo_Locked
        self.SetToUnavailable.on_press = self.SetStateTo_Unavailable
        self.SetToGood.on_press = self.SetStateTo_Good
        Debug.Log("Success")

        Debug.Log("Adding widgets to the gridlayout")
        self.add_widget(self.SetToDisable)
        self.add_widget(self.SetToWarning)
        self.add_widget(self.SetToActive)
        self.add_widget(self.SetToInactive)
        self.add_widget(self.SetToError)
        self.add_widget(self.SetToLocked)
        self.add_widget(self.SetToUnavailable)
        self.add_widget(self.SetToGood)
        Debug.Log("Success")

        Debug.Log("Adding progress bar for testing purposes")
        self.progressBar = Bar(max = 100)
        self.progressBar.pos = (100,200)
        self.progressBar.height = 100
        self.progressBar.background_color = [1,0,1,1]
        self.add_widget(self.progressBar)
        Debug.Log("Success")

        Debug.Log("Adding slider for testing purposes")
        self.slider = Slider(max = 100)
        self.slider.pos = (100,300)
        self.slider.cursor_size = ("25sp","25sp")
        self.slider.bind(value=self.SliderMoving)
        self.slider.value_track = True
        self.slider.value_track_color = [1,1,0,1]
        self.add_widget(self.slider)
        Debug.Log("Success")

        Debug.Log("Adding BRS PieChartDial")
        self.PieChartDial = PieChartDial(min = 0, max = 70, startAngle=0, endAngle=360, trackWidth=10, fillingWidth=50)
        self.PieChartDial.Size = (200,200)
        self.PieChartDial.Pos = (400,400)
        self.add_widget(self.PieChartDial)
        self.PieChartDial.animated = True

        Debug.End()
        #endregion

    def GetNewDialCoordinates(self):
        Debug.Start("GetNewDialCoordinates")
        x = random.randint(0,Window.width/2)
        y = random.randint(0,Window.height/2)

        start = random.randint(0,360)
        end = random.randint(start,360)

        track = random.randint(0,90)
        filling = random.randint(0,90)
        Debug.Log("filling = {}".format(filling))

        self.PieChartDial.SetAttributes(position=(x,y), TrackWidth=track, FillingWidth=filling, startAngle=start, endAngle=end)
        Debug.End()

    def SetStateTo_Disable(self):
        self.rounded_button.State = States.Disabled
        self.progressBar.Value = 0
        self.PieChartDial.Value = 0
        self.PieChartDial.State = States.Disabled
    def SetStateTo_Inactive(self):
        self.rounded_button.State = States.Inactive
        self.progressBar.Value = 100
        self.PieChartDial.Value = 30
        self.PieChartDial.State = States.Inactive
    def SetStateTo_Active(self):
        self.rounded_button.State = States.Active
        self.PieChartDial.State = States.Active
        self.PieChartDial.Value = 20
    def SetStateTo_Error(self):
        self.rounded_button.State = States.Error
        self.PieChartDial.State = States.Error
        self.PieChartDial.Value = 40
    def SetStateTo_Locked(self):
        self.rounded_button.State = States.Locked
        self.PieChartDial.State = States.Locked
        self.PieChartDial.Value = 50
        self.PieChartDial.ShowBackground = not self.PieChartDial.ShowBackground
    def SetStateTo_Unavailable(self):
        self.rounded_button.State = States.Unavailable
        self.PieChartDial.State = States.Unavailable
        self.PieChartDial.Value = 60
        self.PieChartDial.ShowTrack = not self.PieChartDial.ShowTrack
    def SetStateTo_Warning(self):
        self.rounded_button.State = States.Warning
        self.PieChartDial.State = States.Warning
        self.PieChartDial.Value = 10
    def SetStateTo_Good(self):
        self.rounded_button.State = States.Good
        self.PieChartDial.State = States.Good
        self.PieChartDial.Value = 70
        self.PieChartDial.ShowFilling = not self.PieChartDial.ShowFilling
    def SliderMoving(self, a, b):
        Debug.Start()
        Debug.Log(f"SliderMoving: New slider value: {self.slider.value}")
        self.progressBar.Value = self.slider.value

        self.PieChartDial.animated = False
        self.PieChartDial.Value = self.slider.value
        self.PieChartDial.animated = True
        Debug.End()
#################################################################### WIDGETS
class MainWidget(Widget):
    pass

#################################################################### APPLICATION CLASS
class KivyUIApp(App):
    def build(self):
        Debug.Start()
        Debug.Log("Building application's parameters...")
        #---------------------------------------------------------# Title
        Debug.Log("Setting Name...")
        self.title = "Window Name"
        #---------------------------------------------------------# Window properties
        Debug.Log("Setting Window configurations...")

        Window.borderless = False
        Window.resizable = True
        Window.left = -1024
        Window.top = 600
        Window.fullscreen = 'auto'
        #---------------------------------------------------------#
        Debug.End()
        return MyGridLayout()

    Bruh = 0
    def run(self):
        Debug.Start()
        Debug.Warn("Kivy application called the run function")
        Debug.End()
        return super().run()
#################################################################### RUN APPLICATION
Debug.enableConsole = True
Debug.Warn(logged = "Launching KivyUIApp through .run")
KivyUIApp().run()
Debug.Warn(logged = "============================END OF SCRIPT============================")