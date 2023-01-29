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
# -------------------------------------------------------------------
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
# -------------------------------------------------------------------
import random
from BRS.GUI.Utilities.font import Font
from BRS.GUI.Inputs.buttons import TextButton
from BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from BRS.GUI.Status.Indicators import SVGDisplay
from BRS.Utilities.states import StatesColors,States
from BRS.Utilities.AppScreenHandler import AppManager
from BRS.Debug.consoleLog import Debug
from BRS.GUI.Containers.cards import WidgetCard
# -------------------------------------------------------------------
from KivyMD_Test import WindowLayout as KivyMD_Test
from OutlineDial_Tester import WindowLayout as OutlineDial_Tester
from LineGraph_Tester import WindowLayout as LineGraph_Tester
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
class WindowManager(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("WindowManager")

        self.padding = 25
        self.spacing = 25

        self.Layout = BoxLayout()
        self.Layout.spacing = 25
        self.Layout.padding = 25

        self.Layout.card = WidgetCard()

        self.Layout.card.GoTo_KivyMD_Test = MDRaisedButton(text="KivyMD test")
        self.Layout.card.GoTo_KivyMD_Test.bind(on_press = self.GoTo_KivyMDTester)

        self.Layout.card.GoTo_OutlineDial_Tester = MDRaisedButton(text="OutlineDial test")
        self.Layout.card.GoTo_OutlineDial_Tester.bind(on_press = self.GoTo_OutlineDialTester)

        self.Layout.card.GoTo_LineGraph_Tester = MDRaisedButton(text="LineGraph test")
        self.Layout.card.GoTo_LineGraph_Tester.bind(on_press = self.GoTo_LineGraphTester)

        self.Layout.card.Add_Widget(self.Layout.card.GoTo_KivyMD_Test)
        self.Layout.card.Add_Widget(self.Layout.card.GoTo_OutlineDial_Tester)
        self.Layout.card.Add_Widget(self.Layout.card.GoTo_LineGraph_Tester)

        self.Layout.add_widget(self.Layout.card)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def GoTo_KivyMDTester(self, instance):
        AppManager.manager.transition.direction = "up"
        AppManager.manager.current = "KivyMD_Test"

    def GoTo_OutlineDialTester(self, instance):
        AppManager.manager.current = "OutlineDial_Tester"

    def GoTo_LineGraphTester(self, instance):
        AppManager.manager.current = "LineGraph_Tester"
# ------------------------------------------------------------------------
class KivyTesterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("KivyTesterScreen")
        self.add_widget(KivyMD_Test())
        Debug.End()
# ------------------------------------------------------------------------
class OutlineDialTesterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(OutlineDial_Tester())
# ------------------------------------------------------------------------
class LineGraphTesterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(LineGraph_Tester())
# ------------------------------------------------------------------------
class Application(MDApp):
    def build(self):
        AppManager.manager = ScreenManager()
        AppManager.manager.add_widget(WindowManager(name="WindowManager"))
        AppManager.manager.add_widget(KivyTesterScreen(name="KivyMD_Test"))
        AppManager.manager.add_widget(OutlineDialTesterScreen(name="OutlineDial_Tester"))
        AppManager.manager.add_widget(LineGraphTesterScreen(name="LineGraph_Tester"))
        AppManager.manager.current = "WindowManager"

        return AppManager.manager
# ------------------------------------------------------------------------

Application().run()