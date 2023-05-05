#====================================================================#
# File Information
#====================================================================#
"""
    networks.py
    =============
    This file contains functions and classes used to handle networks
    display such as wifi icons or ethernet ports.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
from ...Debug.consoleLog import Debug
LoadingLog.Start("WiFi.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ...Utilities.Information import Information
from ...Utilities.Enums import Execution
from ..Utilities.networks import GetWifiIcon
#endregion
#region -------------------------------------------------------- Kivy
from kivy.metrics import dp
from kivy.core.window import Window
#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.boxlayout import MDBoxLayout
#endregion
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.attributes import Shadow
#====================================================================#
# Functions
#====================================================================#
class WiFiSelectionCard(MDCard):
    #region   --------------------------- DOCSTRING
    '''
        This class makes a widget that displays
        an elongated WiFi card that can swipe
        left or right.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- GET SET
    #endregion
    #region   --------------------------- METHODS
    def _UpdateWidget(self, *args) -> None:
        """
            _UpdateWidget:
            ==============
            Summary:
            --------
            This function is a callback function
            that is executed each time the widget's
            size changes.
        """
        h = self.height
        radius = [dp(h / 2)]
        iconSize = h / 1.25
        self.radius = radius
        self.shadow_radius = radius
        self.WiFiIconButton.size = (iconSize, iconSize)
        self.WiFiIconButton.icon_size = h

        padding = (self.height - self.WiFiIconButton.width) * 0.55
        self.padding = [padding,0,padding,0]

        Debug.enableConsole = True
        Debug.Log("HERE")
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 wifiDictionary,
                 **kwargs):
        super(WiFiSelectionCard, self).__init__(**kwargs)
        Debug.Start("WiFiSelectionCard")
        #region --------------------------- Initial check ups

        # To have a perfect circle edges.
        self.radius = [dp(self.height / 2)]
        self.bind(height = self._UpdateWidget)

        # Icon.
        icon = GetWifiIcon(wifiDictionary["strength"], wifiDictionary["mode"])
        self.WiFiIconButton = MDFloatingActionButton()
        # self.WiFiIconButton.icon = "github"
        self.WiFiIconButton.icon_size = self.height
        self.WiFiIconButton.pos_hint = {"center_x":0.125, "center_y":0.5}
        self.WiFiIconButton.height = self.height / 1.25
        self.WiFiIconButton.width = self.height / 1.25

        padding = self.height - self.WiFiIconButton.height
        self.padding = [padding,0,padding,0]

        # Shadows
        self.shadow_radius = [dp(self.height / 2)]
        self.shadow_softness = Shadow.Smoothness.default
        self.elevation = Shadow.Elevation.pressed
        self.WiFiIconButton.elevation = 0

        self.add_widget(self.WiFiIconButton)

        #endregion
        Debug.End()
    #endregion
    pass
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("networks.py")