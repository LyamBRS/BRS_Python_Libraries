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
from distutils.text_file import TextFile
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding
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
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton, MDFillRoundFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
#endregion
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.attributes import Shadow
#====================================================================#
# Functions
#====================================================================#
def GetWiFiButton(wifiDictionary) -> MDFillRoundFlatIconButton:
    """
        GetWiFiButton:
        ==============
        Summary:
        --------
        This function returns a
        MDFillRoundFlatIconButton
        made from a wifiDictionary returned by
        GetWiFiNetworks.
    """
    Debug.Start("GetWiFiButton")

    icon = GetWifiIcon(wifiDictionary["strength"], wifiDictionary["mode"])
    button = MDFillRoundFlatIconButton()
    button.text = wifiDictionary["ssid"]
    button.icon = icon

    button.size_hint = (1,1)

    return button
    Debug.End()

def GetWiFiNotAvailableCard(textToDisplay) -> Execution:
    """
        GetWiFiNotAvailableCard:
        ========================
        Summary:
        --------
        Returns a card containing the error encountered
        when trying to get the WiFi networks
        available to use.

        Warning:
        --------
        This card will pop up from the bottom
        into view using animations.
    """
    Debug.Start("GetWiFiNotAvailableCard")

    Card = MDCard()
    Card.orientation = "vertical"
    Card.elevation = Shadow.Elevation.default
    Card.shadow_softness = Shadow.Smoothness.default
    Card.radius = Rounding.Cards.default
    Card.size_hint = (0.75,0.75)
    Card.pos_hint = {"center_x":0.5, "center_y":-1}
    Card.padding = 20

    anim = Animation(pos_hint = {"center_x":0.5, "center_y":0.45}, t="in_out_back")
    anim.start(Card)

    NoWiFiIcon = MDFloatingActionButton()
    NoWiFiIcon.icon = "router-wireless-off"
    NoWiFiIcon.size_hint = (0.25,0.25)
    NoWiFiIcon.icon_size = 50
    NoWiFiIcon.pos_hint = {"center_x":0.5, "center_y":0.5}
    NoWiFiIcon.halign = "center"
    NoWiFiIcon.valign = "center"
    NoWiFiIcon.theme_icon_color = "Custom"

    color = MDApp.get_running_app().theme_cls.accent_palette
    NoWiFiIcon.md_bg_color = get_color_from_hex(colors[color]["500"])

    textDisplayed = MDLabel()
    textDisplayed.font_style = "H5"
    textDisplayed.valign = "center"
    textDisplayed.text = textToDisplay

    Card.add_widget(NoWiFiIcon)
    Card.add_widget(textDisplayed)
    Debug.End()
    return Card

class WiFiSelectionCard(MDCard):
    #region   --------------------------- DOCSTRING
    '''
        This class makes a widget that displays
        an elongated WiFi card that can swipe
        left or right.

        DEPRECATED AND NOT FUNCTIONAL.
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
        self.WiFiIconButton.icon_size = iconSize

        padding = (self.height - self.WiFiIconButton.width) * 0.55
        self.padding = [padding,0,padding,0]

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
        # self.bind(height = self._UpdateWidget)

        # Icon.
        icon = GetWifiIcon(wifiDictionary["strength"], wifiDictionary["mode"])
        self.WiFiIconButton = MDFloatingActionButton()
        Debug.Log(icon)
        self.WiFiIconButton.icon = icon
        self.WiFiIconButton.icon_size = self.height / 2
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