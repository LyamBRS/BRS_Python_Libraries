#====================================================================#
# File Information
#====================================================================#
"""
    This file contains KivyMD theme used in BRS applications.
"""
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("Application_Themes.py")
#====================================================================#
# Imports
#====================================================================#
from kivymd.theming import ThemeManager
from kivymd.theming import ThemableBehavior
#====================================================================#
# Themes
#====================================================================#
colors = {
    "Primary": {
        "0":"",
        "10":"",
        "20":"",
        "25":"",
        "30":"",
        "35":"",
        "40":"",
        "50":"",
        "60":"",
        "70":"",
        "80":"",
        "90":"",
        "95":"",
        "98":"",
        "99":"",
        "100":"",
    },
    "Secondary": {
        "0":"",
        "10":"",
        "20":"",
        "25":"",
        "30":"",
        "35":"",
        "40":"",
        "50":"",
        "60":"",
        "70":"",
        "80":"",
        "90":"",
        "95":"",
        "98":"",
        "99":"",
        "100":"",
    },
    "Tertiary": {
        "0":"",
        "10":"",
        "20":"",
        "25":"",
        "30":"",
        "35":"",
        "40":"",
        "50":"",
        "60":"",
        "70":"",
        "80":"",
        "90":"",
        "95":"",
        "98":"",
        "99":"",
        "100":"",
    },

    "Dark": {
        "StatusBar": "#212121",
        "AppBar": "#121212",
        "Background": "#303030",
        "CardsDialogs": "#424242",
        "FlatButtonDown": "#666666",
        "Tabs": "#212121"
    },
    "Light": {
        "StatusBar": "#E0E0E0",
        "AppBar": "#FFFFFF",
        "Background": "#F5F5F5",
        "CardsDialogs": "#FFFFFF",
        "FlatButtonDown": "#CCCCCC",
        "Tabs": "#E0E0E0"
    },
}

font_styles = {
    "H1": {
        "font_name": "Roboto",
        "font_size": 36,
        "color": (0, 0, 0, 1),
        "bold": True,
    },
    "H2": {
        "font_name": "Roboto",
        "font_size": 24,
        "color": (0, 0, 0, 1),
        "bold": True,
    },
    "H3": {
        "font_name": "Roboto",
        "font_size": 18,
        "color": (0, 0, 0, 1),
        "bold": True,
    },
    "Body": {
        "font_name": "Roboto",
        "font_size": 14,
        "color": (0, 0, 0, 1),
        "bold": False,
    },
}

custom_theme = {
    "colors": colors,
    "font_styles": font_styles,
    "tabbar_background_color": (0.2, 0.2, 0.2, 1),
    "tabbar_text_color": (1, 1, 1, 1),
    "tabbar_selected_text_color": (0, 0, 0, 1),
    "toolbar_background_color": (0.2, 0.2, 0.2, 1),
    "toolbar_text_color": (1, 1, 1, 1),
}

# ThemableBehavior.set_current_theme(custom_theme)
LoadingLog.End("Application_Themes.py")