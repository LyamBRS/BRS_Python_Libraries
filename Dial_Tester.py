#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from distutils.log import debug
from email.policy import default
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
    def getMeTheFuckingValues(self):
        Debug.Log("Size of layout: {}".format(self.size))
        Debug.Log("Pos of layout: {}".format(self.pos))
        Debug.Log("size_hint_max of layout: {}".format(self.size_hint_max))
        Debug.Log("size_hint_min of layout: {}".format(self.size_hint_min))
        Debug.Log("pos_hint of layout: {}".format(self.pos_hint))
        Debug.Log("size_hint_x of layout: {}".format(self.size_hint_x))
        Debug.Log("size_hint_y of layout: {}".format(self.size_hint_y))
        Debug.Log("size_hint_max_x of layout: {}".format(self.size_hint_max_x))
        Debug.Log("size_hint_max_y of layout: {}".format(self.size_hint_max_y))
        Debug.Log("size_hint_min_x of layout: {}".format(self.size_hint_min_x))
        Debug.Log("size_hint_min_y of layout: {}".format(self.size_hint_min_y))
        Debug.Log("parent: {}".format(str(self.parent)))
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("ButtonLayout")
            super(ButtonLayout, self).__init__(**kwargs)

            Debug.Log("Size of layout: {}".format(self.size))
            Debug.Log("Pos of layout: {}".format(self.pos))
            Debug.Log("size_hint_max of layout: {}".format(self.size_hint_max))
            Debug.Log("size_hint_min of layout: {}".format(self.size_hint_min))
            Debug.Log("pos_hint of layout: {}".format(self.pos_hint))
            Debug.Log("size_hint_x of layout: {}".format(self.size_hint_x))
            Debug.Log("size_hint_y of layout: {}".format(self.size_hint_y))
            Debug.Log("size_hint_max_x of layout: {}".format(self.size_hint_max_x))
            Debug.Log("size_hint_max_y of layout: {}".format(self.size_hint_max_y))
            Debug.Log("size_hint_min_x of layout: {}".format(self.size_hint_min_x))
            Debug.Log("size_hint_min_y of layout: {}".format(self.size_hint_min_y))
            Debug.Log("parent: {}".format(str(self.parent)))

            self.orientation = "vertical"
            self.padding = 50
            self.spacing = 25

            self.showTrack = TextButton(initialFont = ButtonFont, wantedText = "Hide Track")
            self.showFilling = TextButton(initialFont = ButtonFont, wantedText = "Hide Filling")
            self.showBackground = TextButton(initialFont = ButtonFont, wantedText = "Hide Background")
            self.switchState    = TextButton(initialFont = ButtonFont, wantedText = "Switch State")

            self.showTrack.on_press = self.getMeTheFuckingValues

            self.add_widget(self.showTrack)
            self.add_widget(self.showFilling)
            self.add_widget(self.showBackground)
            self.add_widget(self.switchState)

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

            Debug.Log("Size of layout: {}".format(self.size))
            Debug.Log("Pos of layout: {}".format(self.pos))
            Debug.Log("size_hint_max of layout: {}".format(self.size_hint_max))
            Debug.Log("size_hint_min of layout: {}".format(self.size_hint_min))
            Debug.Log("pos_hint of layout: {}".format(self.pos_hint))
            Debug.Log("size_hint_x of layout: {}".format(self.size_hint_x))
            Debug.Log("size_hint_y of layout: {}".format(self.size_hint_y))
            Debug.Log("size_hint_max_x of layout: {}".format(self.size_hint_max_x))
            Debug.Log("size_hint_max_y of layout: {}".format(self.size_hint_max_y))
            Debug.Log("size_hint_min_x of layout: {}".format(self.size_hint_min_x))
            Debug.Log("size_hint_min_y of layout: {}".format(self.size_hint_min_y))

            Debug.Log("parent: {}".format(str(self.parent)))

            self.padding = 50
            self.spacing = 25

            self.valueSlider    = Slider(min = 0, max = 100)
            self.fillingWidth   = Slider(min = 10, max = 100)
            self.trackWidth     = Slider(min = 10, max = 100)
            self.startAngle     = Slider(min = -180, max = 180)
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

            Debug.Log("Size of layout: {}".format(self.size))
            Debug.Log("Pos of layout: {}".format(self.pos))
            Debug.Log("size_hint_max of layout: {}".format(self.size_hint_max))
            Debug.Log("size_hint_min of layout: {}".format(self.size_hint_min))
            Debug.Log("pos_hint of layout: {}".format(self.pos_hint))
            Debug.Log("size_hint_x of layout: {}".format(self.size_hint_x))
            Debug.Log("size_hint_y of layout: {}".format(self.size_hint_y))
            Debug.Log("size_hint_max_x of layout: {}".format(self.size_hint_max_x))
            Debug.Log("size_hint_max_y of layout: {}".format(self.size_hint_max_y))
            Debug.Log("size_hint_min_x of layout: {}".format(self.size_hint_min_x))
            Debug.Log("size_hint_min_y of layout: {}".format(self.size_hint_min_y))
            Debug.Log("parent: {}".format(str(self.parent)))

            self.temporaryButton = Button()
            self.temporaryButton.size_hint = (1,1)

            # self.PieChartDial = PieChartDial(min=0, max=100, endAngle=360, startAngle=0)

            with self.canvas:
                Color(1, 0, 0, 1)  # red

            self.add_widget(self.temporaryButton)
            # self.add_widget(self.PieChartDial)
            # self.PieChartDial.SetAttributesFromParent()
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

            Debug.Log("Size of layout: {}".format(self.size))
            Debug.Log("Pos of layout: {}".format(self.pos))
            Debug.Log("size_hint_max of layout: {}".format(self.size_hint_max))
            Debug.Log("size_hint_min of layout: {}".format(self.size_hint_min))
            Debug.Log("pos_hint of layout: {}".format(self.pos_hint))
            Debug.Log("size_hint_x of layout: {}".format(self.size_hint_x))
            Debug.Log("size_hint_y of layout: {}".format(self.size_hint_y))
            Debug.Log("size_hint_max_x of layout: {}".format(self.size_hint_max_x))
            Debug.Log("size_hint_max_y of layout: {}".format(self.size_hint_max_y))
            Debug.Log("size_hint_min_x of layout: {}".format(self.size_hint_min_x))
            Debug.Log("size_hint_min_y of layout: {}".format(self.size_hint_min_y))
            Debug.Log("parent: {}".format(str(self.parent)))

            self.buttons = ButtonLayout()
            self.dials   = DialLayout()
            self.sliders = SliderLayout()

            self.add_widget(self.buttons)
            self.add_widget(self.dials)
            self.add_widget(self.sliders)
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
        Debug.End()

        self.windowLayout = WindowLayout()
        return self.windowLayout

    def run(self):
        Debug.Start()
        Debug.Warn("Kivy application called the run function")
        Debug.End()
        return super().run()
    
    def on_start(self):
        Debug.Start("on_start")
        Debug.Log("Button's X: {}".format(self.windowLayout.dials.temporaryButton.pos))
        self.windowLayout.dials.temporaryButton.pos = (0,0)
        Debug.End()
#====================================================================#
# Application Running
#====================================================================#
Debug.enableConsole = True
Debug.Warn(logged = "Launching KivyUIApp through .run")
KivyUIApp().run()
Debug.Warn(logged = "============================END OF SCRIPT============================")

