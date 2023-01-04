#################################################################### IMPORTS
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from BRS.GUI.Utilities.font import Font
from BRS.GUI.Inputs.buttons import TextButton
from BRS.Utilities.states import States
from BRS.Debug.consoleLog import Debug
#################################################################### Configs
amogusFont = Font()
amogusFont.isBold = True
#################################################################### GridLayout
class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        Debug.Start()
        # Call gridlayout constructor
        super(MyGridLayout, self).__init__(**kwargs)
        self.col = 1
        self.size = (Window.width,Window.height)

        # Add the RoundedButton widget
        Debug.Log("Initializing the main TextButton")
        self.rounded_button = TextButton()

        self.rounded_button.Text = "Among us"
        x = (Window.width/2) - self.rounded_button.width/2
        y = (Window.height/2) - self.rounded_button.height/2
        self.rounded_button.pos = x,y
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
        self.SetToDisable.pos = (1,0)
        self.SetToWarning.pos = (125,0)
        self.SetToActive.pos = (250, 0)
        self.SetToInactive.pos = (375, 0)
        self.SetToError.pos = (500, 0)
        self.SetToLocked.pos = (625, 0)
        self.SetToUnavailable.pos = (750, 0)
        self.SetToGood.pos = (875, 0)
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

        Debug.End()
        #endregion

    def SetStateTo_Disable(self):
        self.rounded_button.State = States.Disabled
    def SetStateTo_Inactive(self):
        self.rounded_button.State = States.Inactive
    def SetStateTo_Active(self):
        self.rounded_button.State = States.Active
    def SetStateTo_Error(self):
        self.rounded_button.State = States.Error
    def SetStateTo_Locked(self):
        self.rounded_button.State = States.Locked
    def SetStateTo_Unavailable(self):
        self.rounded_button.State = States.Unavailable
    def SetStateTo_Warning(self):
        self.rounded_button.State = States.Warning
    def SetStateTo_Good(self):
        self.rounded_button.State = States.Good
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
        Window.fullscreen = 'auto'
        Window.borderless = False
        Window.resizable = True
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