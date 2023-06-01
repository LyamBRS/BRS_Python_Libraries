#====================================================================#
# File Information
#====================================================================#
"""_summary_
    This file contains GUI color classes. Such as statesColors or
    UIcolors.

    The classes contained in this file are references only. Do not
    construct them
"""
#====================================================================#
# Imports
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
from ...Debug.consoleLog import Debug
from kivymd.app import MDApp
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
LoadingLog.Start("colors.py")

#====================================================================#
# Functions
#====================================================================#
def GetAccentColor(variant:str = "500") -> None:
    """
        GetAccentColor:
        ===============
        Summary:
        --------
        This function returns the accent color
        of the application.

        Arguments:
        ----------
        - "50"
        - "100"
        - "200"
        - "300"
        - "400"
        - "500" Default value
        - "600"
        - "700"
        - "800"
        - "900"
        - "A100"
        - "A200"
        - "A400"
        - "A700"
        - "Dark"
        - "Light"

        Returns:
        --------
        - (0,0,0) to (1,1,1)
    """
    Debug.Start("GetAccentColor")

    try:
        if(variant == "Dark"):
            color = MDApp.get_running_app().theme_cls.accent_dark
            Debug.Log("Returning darker color")
            Debug.End()
            return color
        elif(variant == "Light"):
            color = MDApp.get_running_app().theme_cls.accent_light
            Debug.Log("Returning lighter color")
            Debug.End()
            return color
        else:
            color = MDApp.get_running_app().theme_cls.accent_palette
            color = get_color_from_hex(colors[color][variant])
    except:
        Debug.Error("Failed to get accent color.")
        Debug.Log("Returning red")
        color = (1,0,0)
    Debug.End()
    return color

def GetPrimaryColor(variant:str = "500") -> None:
    """
        GetPrimaryColor:
        ===============
        Summary:
        --------
        This function returns the primary color
        of the application.

        Arguments:
        ----------
        - "50"
        - "100"
        - "200"
        - "300"
        - "400"
        - "500" Default value
        - "600"
        - "700"
        - "800"
        - "900"
        - "A100"
        - "A200"
        - "A400"
        - "A700"
        - "Dark"
        - "Light"

        Returns:
        --------
        - (0,0,0) to (1,1,1)
    """
    Debug.Start("GetAccentColor")

    try:
        if(variant == "Dark"):
            color = MDApp.get_running_app().theme_cls.primary_dark
            Debug.Log("Returning darker color")
            Debug.End()
            return color
        elif(variant == "Light"):
            color = MDApp.get_running_app().theme_cls.primary_light
            Debug.Log("Returning lighter color")
            Debug.End()
            return color
        else:
            color = MDApp.get_running_app().theme_cls.primary_palette
            color = get_color_from_hex(colors[color][variant])
    except:
        Debug.Error("Failed to get primary color.")
        Debug.Log("Returning red")
        color = (1,0,0)
    Debug.End()
    return color

def GetMDCardColor(theme:str = "Dark") -> None:
    """
        GetCardColor:
        ============
        Summary:
        --------
        This function returns the primary color
        of the application.

        Arguments:
        ----------
        - "Dark" - default value
        - "Light"

        Returns:
        --------
        - (0,0,0) to (1,1,1)
    """
    Debug.Start("GetMDCardColor")

    try:
        if(theme == "Dark"):
            # color = MDApp.get_running_app().theme_cls.bg_dark
            hex = colors["Dark"]["CardsDialogs"]
            color = get_color_from_hex(hex)
            Debug.Log("Returning darker color")
            Debug.End()
            return color
        elif(theme == "Light"):
            # color = MDApp.get_running_app().theme_cls.bg_light
            hex = colors["Light"]["CardsDialogs"]
            color = get_color_from_hex(hex)
            Debug.Log("Returning lighter color")
            Debug.End()
            return color
        Debug.End()
        return (1,0,0)
    except:
        Debug.Error("Failed to get primary color.")
        Debug.Log("Returning red")
        color = (1,0,0)
    Debug.End()
    return color


def GetAppTheme() -> str:
    """
        GetAppTheme:
        ============
        Summary:
        --------
        Returns either "Light"
        or "Dark"
    """
    Debug.Start("GetAppTheme")
    try:
        color = MDApp.get_running_app().theme_cls.theme_style
        Debug.End()
        return color
    except:
        Debug.Error("Failed to get app theme.")
        Debug.Log("Returning red")
        color = (1,0,0)
    Debug.End()
    return "Error"
#====================================================================#
# Classes
#====================================================================#
class GUIColors:
    #region   --------------------------- DOCSTRING
    '''
        This is a reference style class which means you should only reference
        it and get data from it. See it like an enum in C#.

        This class contains the colors used for standard GUI applications.
        - Window Color
        - Card Color
    '''
    #endregion
    #region   --------------------------- MEMBERS
    Card = (255/255., 255/255., 255/255., 1.)
    '''RGBA color to use with Card layouts'''

    CardShadow = (0,0,0,1.)
    """RGBA color used for the cards layouts shadows."""

    Window = (255/255., 255/255., 255/255., 1.)
    """RGBA color used as the application's background color."""
    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass

LoadingLog.End("colors.py")