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

#====================================================================#
# Functions
#====================================================================#

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