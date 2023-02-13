#====================================================================#
# File Information
#====================================================================#
print("cards.py")
#====================================================================#
# Imports
#====================================================================#
from ...Debug.consoleLog import Debug
from ...Utilities.states import States,StatesColors
from ...GUI.Utilities.colors import GUIColors
# from ...GUI.Utilities.font import Font
# from ...GUI.Utilities.attributes import DrawingProperties
# from ...GUI.Utilities.attributes import GetEllipse,GetLine
# from ...GUI.Utilities.attributes import UpdateEllipse,UpdateLine
from ...GUI.Utilities.attributes import BRS_ValueWidgetAttributes, BRS_BarGraphWidgetAttributes, BRS_CardLayoutAttributes
from ...GUI.Utilities.references import Shadow,Rounding
from ...Utilities.FileHandler import JSONdata

from kivymd.app import MDApp
from kivymd.uix.card import MDCard,MDCardSwipe,MDCardSwipeFrontBox,MDCardSwipeLayerBox,MDSeparator
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import BaseButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDLabel
from kivymd.color_definitions import palette,colors
from kivymd.theming import ThemeManager
from kivy.utils import get_color_from_hex

from kivy.uix.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
# from kivy.graphics import RoundedRectangle
# from kivy.graphics import Line
# from kivy.graphics import Color
# from kivy.graphics import Ellipse
# from kivy.event import EventDispatcher
from kivymd.uix.label import MDIcon
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class WidgetCard(BRS_CardLayoutAttributes, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        This class is a simple Layout class which takes the appearence of a simple
        card style container. This uses KivyMD cards.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #region   -- Private
    # ------------------------------------------------------
    def _AnimatingShapes(self, *args):
        """
            Called when Animations are executed.
            Call which shapes need to be set to new values here.

            See PieChartDial for an example.
        """
        Debug.Start("_AnimatingShapes")

        # [Step 1]: Update drawings based on new values
        self._MDCard.padding = self._current_padding
        self._MDCard.spacing = self._current_spacing
        self._MDCard.elevation = self._current_elevation
        self._MDCard.shadow_softness = self._current_ShadowSoftness

        # [Step 2]: Update background's positions
        self._MDCard.pos   = (self._current_pos[0], self._current_pos[1])
        self._MDCard.size  = (self._current_size[0], self._current_size[1])
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, *args):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        self._MDCard.md_bg_color = self._current_backgroundColor
        self._MDCard.shadow_color = self._current_backgroundShadowColor
        Debug.End()
    # ------------------------------------------------------
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 initialState = States.Disabled,
                 **kwargs):
        super(WidgetCard, self).__init__(**kwargs)
        Debug.Start("BoxLayoutCard")
        #region --------------------------- Initial check ups
        self.InitAnimations()
        x = self.pos[0]
        y = self.pos[1]
        w = self.size[0]
        h = self.size[1]
        #endregion
        #region --------------------------- Set Variables
        Debug.Log("Setting internal variables to new specified values")
        self._state = initialState
        #endregion
        #region --------------------------- Set Card
        # Setting card attributes
        # self._MDCard.md_bg_color = GUIColors.Card
        # self._MDCard.shadow_color = GUIColors.CardShadow
        self._MDCard.radius = Rounding.default

        self._MDCard.spacing = self._current_spacing
        self._MDCard.padding = self._current_padding
        self._MDCard.elevation = self._current_elevation
        self._MDCard.shadow_softness = self._current_ShadowSoftness
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Binding events to WidgetCard")
            self.bind(pos = self._UpdatePos, size = self._UpdateSize)

        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting PieChartDial's color animation properties")

        self._current_backgroundColor       = self._MDCard.md_bg_color
        self._wanted_BackgroundColor        = self._MDCard.md_bg_color

        Debug.Log("Setting PieChartDial's shape animation properties")

        self._current_pos           = (x, y)
        self._wanted_Pos            = (x, y)

        self._current_size          = (w, h)
        self._wanted_Size           = (w, h)

        self._current_pos_hint      = (x, y)
        self._wanted_Pos_hint       = (x, y)

        self._current_size_hint     = (w, h)
        self._wanted_Size_hint      = (w, h)

        self.add_widget(self._MDCard)
        #endregion
        Debug.End()
    #endregion
    pass

class ProfileCard(BRS_CardLayoutAttributes, BaseButton, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
        This class is a simple Layout class which takes the appearence of a simple
        card style container. This uses KivyMD cards.

        Use `PressedEnd` to bind on_press
        your function that will replace `PressedEnd` must have a card input.
        `PressEnd(widget):` can work.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    Name:str = "Error"
    """
        The Username of the profile.
        Defaults to `"Error"`.
    """
    IconType:str = "Kivy"
    """
        If the profile has a kivyMD icon or a custom path based icon.
        Defaults to `"Kivy"`.
    """
    IconPath:str = "exclamation"
    """
        The path to the profile's icon. If `IconPath` equals `"Kivy"`, 
        this will be equal to the name of a material design KivyMD icon.
        Otherwise, it will be the full path to the profile's icon.
    """
    Style:str = "Light"
    """
        The profile's main theme. `"Light"` or `"Dark"`
    """
    Primary:str = "Purple"
    """
        The profile's primary color. Defaults to `"Purple"`
    """
    Accent:str = "Teal"
    """
        The profile's primary color. Defaults to `"Teal"`
    """
    Password:str = ""
    """
        The profile's loaded Password. Defaults to `""`.
    """
    CanBeUsed:bool = False
    """
        Defines if the profile loaded from JSONdata can be
        used and loaded. If false, the profile has an error
        and thus cannot be loaded as a profile.
    """
    json:JSONdata = None
    """
        Holds the full json profile data that was loaded when the card was created.
        Please `del` profile cards that you no longer use and display to free up memory.
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def PressedEnd(self, *args):
        """
            Function called by the card once the ripple effect
            comes to an end.
        """
        pass
    #endregion
    #region   -- Private
    # ------------------------------------------------------
    def _RippleHandling(self, object, finished):
        if(finished):
            self.PressedEnd(self)
    # ------------------------------------------------------
    def _AnimatingShapes(self, animation, value, theOtherOne):
        """
            Called when Animations are executed.
            Call which shapes need to be set to new values here.

            See PieChartDial for an example.
        """
        Debug.Start("_AnimatingShapes")

        # [Step 1]: Update drawings based on new values
        self._MDCard.padding = self._current_padding
        self._MDCard.spacing = self._current_spacing
        self._MDCard.elevation = self._current_elevation
        self._MDCard.shadow_softness = self._current_ShadowSoftness

        # [Step 2]: Update background's positions
        self._MDCard.pos   = (self._current_pos[0], self._current_pos[1])
        self._MDCard.size  = (self._current_size[0], self._current_size[1])
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        Debug.Log("Color = {}".format(self._current_trackColor))
        # self._MDCard.md_bg_color = self._current_backgroundColor
        # self._MDCard.shadow_color = self._current_backgroundShadowColor
        Debug.End()
    # ------------------------------------------------------
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 jsonPath:str,
                 fileName:str,
                 initialState = States.Disabled,
                 **kwargs):
        super(ProfileCard, self).__init__(**kwargs)
        Debug.Start("ProfileCard")
        #region --------------------------- Initial check ups
        self.InitAnimations()
        x = self.pos[0]
        y = self.pos[1]
        w = self.size[0]
        h = self.size[1]

        self.padding = 0
        self.spacing = 0

        # Handles a function that is called once the ripple animation finishes.
        print(self._finishing_ripple)
        self.bind(_finishing_ripple = self._RippleHandling)
        #endregion
        #region --------------------------- Read JSON
        self.json = JSONdata(fileName,jsonPath)
        self._MDCard.Icon = MDLabel(text="exclamation", font_style='Icon', font_size = "100sp", halign = "center")
        self._MDCard.Icon.font_size = "100sp"
        self._MDCard.Title = MDLabel(text="Error", font_style = "H4", halign = "center")
        self._MDCard.Separator = MDProgressBar()
        self._MDCard.Separator.size_hint = (1,0.05)

        self._MDCard.Separator.value_normalized = 1
        self._MDCard.orientation = "vertical"

        # JSON data parsing into a profile card
        if(self.json == None):
            self.IconPath = "exclamation"
            self.IconType = "Kivy"
            self.Name = "Error"
            self.CanBeUsed = False
        else:
            self.IconPath = self.json.jsonData["Generic"]["IconPath"]
            self.IconType = self.json.jsonData["Generic"]["IconType"]
            self.Name     = self.json.jsonData["Generic"]["Username"]
            self.Style    = self.json.jsonData["Theme"]["Style"]
            self.Primary  = self.json.jsonData["Theme"]["Primary"]
            self.Accent   = self.json.jsonData["Theme"]["Accent"]

        # Get the palette themes (Dark / Light)
        if(self.Style == "Dark"):
            CardBackground = (0.12,0.12,0.12,1)
            TextColor = (1,1,1,1)
        else:
            CardBackground = (1,1,1,1)
            TextColor = (0.12,0.12,0.12,1)

        # Get the primary palette color.
        print(colors[self.Primary]["500"])
        secondaryColor = get_color_from_hex(colors[self.Primary]["500"])

        # Inverse colors of widget if theme is not the same
        if(MDApp.get_running_app().theme_cls.theme_style != self.Style):
            self._MDCard.opposite_colors = True
            self._MDCard.bg_color = CardBackground
            self._MDCard.Title.opposite_colors = True
            self._MDCard.Icon.opposite_colors = True
            print("INVERTED")

        # - Set widget colors here
        self._MDCard.md_bg_color = CardBackground
        self._MDCard.color = CardBackground
        self._MDCard.Title.text_color = TextColor
        self._MDCard.Title.color = TextColor
        self._MDCard.Icon.text_color  = TextColor
        self._MDCard.Icon.color  = TextColor
        self._MDCard.Separator.back_color = secondaryColor
        self._MDCard.Separator.color = secondaryColor

        # Get the profile picture saved in the JSON
        if(self.IconType == "Kivy"):
            self._MDCard.Icon.text = md_icons[self.IconPath]
            print(self.IconPath)

        # Place the Username in the card
        self._MDCard.Title.text = self.Name

        print(" ==== " + self.Style)

        self._MDCard.add_widget(self._MDCard.Icon)
        self._MDCard.add_widget(self._MDCard.Title)
        self._MDCard.add_widget(self._MDCard.Separator)
        #endregion
        #region --------------------------- Set Variables
        Debug.Log("Setting internal variables to new specified values")
        self._state = initialState
        #endregion
        #region --------------------------- Set Card
        # Setting card attributes
        # self._MDCard.md_bg_color = GUIColors.Card
        self._MDCard.shadow_color = GUIColors.CardShadow
        self._MDCard.radius = Rounding.default

        self._MDCard.spacing = 0#self._current_spacing
        self._MDCard.padding = 0#self._current_padding
        self._MDCard.elevation = self._current_elevation
        self._MDCard.shadow_softness = self._current_ShadowSoftness
        #endregion
        #region --------------------------- Set Canvas
        Debug.Log("Creating Canvas")
        with self.canvas:
            Debug.Log("Binding events to WidgetCard")
            self.bind(pos = self._UpdatePos, size = self._UpdateSize)

        #endregion
        #region --------------------------- Set Animation Properties
        Debug.Log("Setting PieChartDial's color animation properties")

        self._current_backgroundColor       = self._MDCard.md_bg_color
        self._wanted_BackgroundColor        = self._MDCard.md_bg_color

        Debug.Log("Setting PieChartDial's shape animation properties")

        self._current_pos           = (x, y)
        self._wanted_Pos            = (x, y)

        self._current_size          = (w, h)
        self._wanted_Size           = (w, h)

        self._current_pos_hint      = (x, y)
        self._wanted_Pos_hint       = (x, y)

        self._current_size_hint     = (w, h)
        self._wanted_Size_hint      = (w, h)

        self.add_widget(self._MDCard)
        #endregion
        Debug.End()
    #endregion
    pass