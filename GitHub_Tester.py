#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from github import Github as git
import subprocess


from BRS.Network.APIs.GitHub import GitHub
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
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("WindowLayout")
            super(WindowLayout, self).__init__(**kwargs)

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
        self.title = "BRS Github Tester"
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

print("\n")
print("\n")
print("\n")

GitHub.GetUser("LyamBRS")
print(str(GitHub.userInformation))
print("\n")
print("\n")
print("\n")
GitHub.GetUserRepositories()
print(str(GitHub.ListOfRepositories))
print("\n")

# KivyUIApp().run()
Debug.Warn(logged = "============================END OF SCRIPT============================")

