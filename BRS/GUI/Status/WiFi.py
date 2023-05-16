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
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.colors import GetAccentColor
#endregion
#region -------------------------------------------------------- Kivy

#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButton, MDFillRoundFlatIconButton, BaseButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
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

    NoWiFiIcon = MDFloatingActionButton()
    NoWiFiIcon.icon = "router-wireless-off"
    NoWiFiIcon.size_hint = (0.25,0.25)
    NoWiFiIcon.icon_size = 50
    NoWiFiIcon.pos_hint = {"center_x":0.5, "center_y":0.5}
    NoWiFiIcon.halign = "center"
    NoWiFiIcon.valign = "center"
    NoWiFiIcon.theme_icon_color = "Custom"

    NoWiFiIcon.md_bg_color = GetAccentColor()

    textDisplayed = MDLabel()
    textDisplayed.font_style = "H5"
    textDisplayed.valign = "center"
    textDisplayed.text = textToDisplay

    Card.add_widget(NoWiFiIcon)
    Card.add_widget(textDisplayed)
    Debug.End()
    return Card


class WiFiSelectionCard(BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        WiFiSelectionCard:
        ==================
        Summary:
        --------
        This class is a widget class that displays
        a WiFi card based off a dictionary returned
        from a GetWiFiNetwork function.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def PressedEnd(self, *args):
        """
            PressedEnd:
            ===========
            Summary:
            --------
            Function called by the card once the ripple effect
            comes to an end.
        """
        pass

    def UpdateValues(self, WiFiNetworkDictionary:list) -> None:
        """
            UpdateValues:
            =============
            Summary:
            --------
            This function updates the widgets
            stored in this class through an
            input parameter that is a list
            of WiFi attributes. The same that
            is given when you initialize the
            class.
        """
        Debug.Start("UpdateValues")

        try:
            ssid = WiFiNetworkDictionary["ssid"]
        except:
            ssid = "ERROR"

        try:
            bssid = WiFiNetworkDictionary["bssid"]
        except:
            bssid = "???"

        try:
            icon = GetWifiIcon(WiFiNetworkDictionary["strength"], WiFiNetworkDictionary["mode"])
            accentColor = GetAccentColor()
        except:
            icon = "alert"
            accentColor = (255,0,0)

        self.Icon.icon = icon
        self.Name.text = ssid
        self.BSSID.text = bssid
        Debug.End()
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _RippleHandling(self, object, finished):
        if(finished):
            self.PressedEnd(self)
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 WiFiNetworkDictionary:dict,
                 **kwargs):
        super(WiFiSelectionCard, self).__init__(**kwargs)
        Debug.Start("WiFiSelectionCard")
        #region --------------------------- Initial check ups
        Debug.Log("1")
        self.padding = 0
        self.spacing = 0
        self.size = (600,100)

        #region ---------------------------- Getting network info

        try:
            ssid = WiFiNetworkDictionary["ssid"]
        except:
            ssid = "ERROR"

        try:
            bssid = WiFiNetworkDictionary["bssid"]
        except:
            bssid = "???"

        try:
            icon = GetWifiIcon(WiFiNetworkDictionary["strength"], WiFiNetworkDictionary["mode"])
            accentColor = GetAccentColor()
        except:
            icon = "alert"
            accentColor = (255,0,0)
        #endregion

        self.bind(_finishing_ripple = self._RippleHandling)

        self.Card = MDCard(spacing = 10, orientation = "horizontal")
        self.Card.elevation = Shadow.Elevation.default
        self.Card.shadow_softness = Shadow.Smoothness.default
        self.Card.radius = Rounding.Cards.default

        #endregion

        #region --------------------------- Widgets
        self.Layout = MDFloatLayout(size_hint = (0.25,1))

        self.Icon = MDFloatingActionButton(icon = icon, halign = "center", icon_size = 90)
        self.Icon.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }
        self.Icon.size_hint = (1,1)
        self.Icon.md_bg_color = accentColor

        self.Name = MDLabel(text=ssid, font_style = "H4", halign = "left")
        self.Name.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }

        self.BSSID = MDLabel(text=bssid, font_style = "Subtitle1", halign = "left")
        self.BSSID.pos_hint = { 'center_x': 0.5, 'center_y': 0.5 }
        #endregion

        self.textBox = MDBoxLayout(orientation = "vertical")
        self.textBox.add_widget(self.Name)
        self.textBox.add_widget(self.BSSID)

        self.Layout.add_widget(self.Icon)
        self.Card.add_widget(self.Layout)
        self.Card.add_widget(self.textBox)
        self.add_widget(self.Card)

        Debug.End()
    #endregion
    pass

#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("networks.py")