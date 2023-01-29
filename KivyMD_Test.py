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
from kivymd.uix.button import MDRaisedButton,MDIconButton,MDFillRoundFlatButton,MDTextButton,MDFloatingActionButton,MDRectangleFlatButton
from kivymd.uix.card import MDCard

from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from BRS.Utilities.AppScreenHandler import AppManager
from PIL import Image

import random
from BRS.Debug.consoleLog import Debug
from BRS.Utilities.states import StatesColors
from BRS.Utilities.states import States
from BRS.GUI.Utilities.font import Font
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Containers.cards import WidgetCard
from BRS.GUI.Status.Progress import Bar
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
    def GoBackToWindowManager(self, instance):
        AppManager.manager.transition.direction = "down"
        AppManager.manager.current = "WindowManager"
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            super(ButtonLayout, self).__init__(**kwargs)
            Debug.Start("ButtonLayout")

            self.manager = kwargs.get('manager')

            self.orientation = "horizontal"
            self.padding = 25
            self.spacing = 25

            self.card = WidgetCard()
            self.card.Orientation = "horizontal"
            self.card._MDCard.orientation = "vertical"

            self.card.MainTheme = MDRaisedButton(text="Dark")
            self.card.Primary = MDRaisedButton(text="Red")

            self.card.IconButton = MDIconButton()

            png_file = r"C:\Users\cous5\Documents\BRS_Documents\Librairies\Icons\Applications\Icons_BRS\Logos\UniLetters\BRS_B.png"

            self.card.IconButton.icon = png_file

            self.card.GoBack = MDRectangleFlatButton(text="Go Back")
            self.card.GoBack.bind(on_press = self.GoBackToWindowManager)

            self.card.Add_Widget(self.card.GoBack)
            self.card.Add_Widget(self.card.MainTheme)
            self.card.Add_Widget(MDFillRoundFlatButton(text="MDFillRoundFlatButton"))
            self.card.Add_Widget(MDTextButton(text="MDTextButton"))
            self.card.Add_Widget(MDRaisedButton(text="MDRaisedButton"))
            self.card.Add_Widget(MDFloatingActionButton(text="MDFloatingActionButton"))
            self.card.Add_Widget(self.card.IconButton)
            self.card.Add_Widget(self.card.Primary)

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

            self.padding = 25
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

            self.card.Add_Widget(self.card.valueSlider )
            self.card.Add_Widget(self.card.fillingWidth)
            self.card.Add_Widget(self.card.trackWidth  )
            self.card.Add_Widget(self.card.startAngle  )
            self.card.Add_Widget(self.card.endAngle    )

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

            self.padding = 25
            self.spacing = 25

            self.card = WidgetCard()
            self.card.Orientation = "vertical"

            self.card.OutlineDial = OutlineDial(min=0, max=100, endAngle=360, startAngle=0)
            self.card.OutlineDial.animated = True

            self.card.PieChartDial = PieChartDial(min=0, max=100, endAngle=360, startAngle=0)
            self.card.PieChartDial.animated = True

            self.card.Add_Widget(self.card.OutlineDial)
            self.card.Add_Widget(self.card.PieChartDial)

            self.Information = TextButton(initialFont=ButtonFont)
            self.Information.Text = "PieChartDial"

            # self.add_widget(self.Information)
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
    def SetElevation(self,*args):
        self.buttons.card._MDCard.elevation = self.sliders.card.valueSlider.value

    def SetSmootness(self,*args):
        self.buttons.card._MDCard.shadow_softness = self.sliders.card.fillingWidth.value
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
            Debug.Start("WindowLayout")
            super(WindowLayout, self).__init__(**kwargs)

            self.manager = kwargs.get('manager')

            self.buttons = ButtonLayout()
            self.dials   = DialLayout()
            self.sliders = SliderLayout()

            self.sliders.card.fillingWidth.bind(value = self.SetSmootness)
            self.sliders.card.valueSlider.bind(value = self.SetElevation)

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
#         #---------------------------------------------------------#
#         Debug.Log("Building layouts")
#         self.windowLayout = WindowLayout()

#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Orange"
#         self.theme_cls.theme_style_switch_animation = True
#         self.theme_cls.theme_style_switch_animation_duration = 0.5

#         Debug.Log("Attributing functions to buttons")
#         self.windowLayout.buttons.card.MainTheme.on_press = self.SwitchMainTheme
#         self.windowLayout.buttons.card.Primary.on_press = self.SwitchPrimaryTheme
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

#     def SwitchMainTheme(self, *args):
#         if self.theme_cls.theme_style == "Dark":
#             self.theme_cls.theme_style = "Light"
#             self.windowLayout.buttons.card.MainTheme.text = "Light"

#         elif self.theme_cls.theme_style == "Light":
#             self.theme_cls.theme_style = "Dark"
#             self.windowLayout.buttons.card.MainTheme.text = "Dark"

#     def SwitchPrimaryTheme(self, *args):
#         Debug.Start("SwitchPrimaryTheme")
#         self.windowLayout.buttons.card.Primary.text = "Pressed"

#         ColorsRange = ("Red", "Blue", "Brown", "Lime", "Green", "Orange", "Yellow", "Pink", "DeepPurple", "Indigo", "LightBlue", "Cyan", "Teal", "Amber", "DeepOrange", "Gray", "BlueGray")
#         index = random.randint(0,16)
#         Debug.Log("New color is: {}".format(ColorsRange[index]))
#         self.theme_cls.primary_palette = ColorsRange[index]
#         self.windowLayout.buttons.card.Primary.text = self.theme_cls.primary_palette
#         Debug.End()

# #====================================================================#
# # Application Running
# #====================================================================#
# Debug.enableConsole = True
# Debug.Warn(logged = "Launching KivyUIApp through .run")
# KivyUIApp().run()
# Debug.Warn(logged = "============================END OF SCRIPT============================")

