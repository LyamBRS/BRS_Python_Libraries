#====================================================================#
# File Information
#====================================================================#
"""
    This file contains classes that can be seen as structures.
    The goal is to uniformize how widget are drawn on the screen.
"""
#====================================================================#
# Imports
#====================================================================#
from kivymd.theming import ThemeManager
#====================================================================#
# Themes
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Shadow:
    #region   --------------------------- DOCSTRING
    ''' Reference class for widget's supporting elevations.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    class Elevation:
        """Elevation attribute of widgets"""
        default:float = 2.5
        """Default value when the widget is not pressed not hovering"""
        hovering:float = 5.5
        """Elevation value when a cursor is above a widget """
        pressed:float = 2
        """Elevation value when a widget is pressed on."""

    class Smoothness:
        """shadow smootheness attribute of widgets"""
        default:float = 90
        """Default value when the widget is not pressed not hovering"""
        hovering:float = 30
        """Elevation value when a cursor is above a widget """
        pressed:float = 10
        """Elevation value when a widget is pressed on."""
     #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
class Rounding:
    #region   --------------------------- DOCSTRING
    ''' Reference class used for widget's rounded edges
    '''
    #endregion
    #region   --------------------------- MEMBERS
    default:float = "20dp"
    """Default value when the widget is not pressed not hovering"""
     #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#