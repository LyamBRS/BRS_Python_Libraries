#====================================================================#
# File Information
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("font.py")
#====================================================================#
# Imports
#====================================================================#
from typing import Any
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivymd.uix.button import MDFlatButton
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Font:
    #region   --------------------------- DOCSTRING
    '''
    The font class is used to specify a font for text based data in a GUI
    This is used by larger GUI classes like buttons and labels for example
    '''
    #endregion
    #region   --------------------------- MEMBERS
    size : Any = '15sp'
    '''[KIVY]: Font size of the text, in pixels.'''
    blended : bool = True
    '''Whether blended or solid font rendering should be used.'''
    context : Any = "None"
    '''[KIVY]: Font context. None means the font is used in isolation, so you are guaranteed to be drawing with the TTF file resolved by font_name. Specifying a value here will load the font file into a named context, enabling fallback between all fonts in the same context. If a font context is set, you are not guaranteed that rendering will actually use the specified TTF file for all glyphs (Pango will pick the one it thinks is best).'''
    family : str = "None"
    '''[KIVY]: Font family, this is only applicable when using font_context option. The specified font family will be requested, but note that it may not be available, or there could be multiple fonts registered with the same family.'''
    hinting : str = "normal"
    '''[KIVY]: normal, light, mono'''
    name : str = 'Roboto'
    '''[KIVY]: filename of the font to use'''
    kerning : bool = True
    '''[KIVY]: Whether kerning is enabled for font rendering. You should normally only disable this if rendering is broken with a particular font file.'''
    isBold : bool = False
    '''Defines if this font is bold or not.\n Defaults to: False'''
    isItalic : bool = False
    '''Defines if the font is italic or not.\n Defaults to: False'''
    isUnderline : bool = False
    '''Defines if the font is underlined or not.\n Defaults to: False'''
    isStrikethrough : bool = False
    '''Defines if the font is striked through or not.\n Default: False'''
    #endregion
    #region   --------------------------- METHODS
    #-----------------------------------#
    def Delete(self):
        '''
            Deletes all the variables used in this function via "del".
            Example:
            del self.size
        '''
        del self.size
        del self.blended
        del self.context
        del self.name
        del self.family
        del self.kerning
        del self.hinting
        del self.isBold
        del self.isStrikethrough
        del self.isItalic
        del self.isUnderline
    #-----------------------------------#
    def SetAll(self,newSize : Any = size,
                    newBlended : bool = blended,
                    newContext : str = context,
                    newName : str = name,
                    newFamily : str = family,
                    newHinting : str = hinting,
                    newKerning : bool = kerning,
                    newBold : bool = isBold,
                    newItalic : bool = isItalic,
                    newUnderline : bool = isUnderline,
                    newStrikethrough : bool = isStrikethrough,) -> None:
        '''Used to set all the values of the Font class to new values or current value if not specified.
            See __init__ function for a quick list of default values'''
        self.size = newSize
        self.blended = newBlended
        self.context = newContext
        self.name = newName
        self.family = newFamily
        self.kerning = newKerning
        self.hinting = newHinting

        self.isBold = newBold
        self.isStrikethrough = newStrikethrough
        self.isItalic = newItalic
        self.isUnderline = newUnderline
    #-----------------------------------#
    def GetFrom(self, thatLabel:Label = None, thatButton:Button = None, thatTextInput:TextInput = None, thatFont:Any = None):
        '''Copy all the font attribute of a referenced uix element into the font class.'''
        #If we are copying from a label
        if(thatLabel != None):
            self.size =             thatLabel.font_size
            self.blended =          thatLabel.font_blended
            self.context =          thatLabel.font_context
            self.name =             thatLabel.font_name
            self.family =           thatLabel.font_family
            self.kerning =          thatLabel.font_kerning
            self.hinting =          thatLabel.font_hinting

            self.isBold =           thatLabel.bold
            self.isStrikethrough =  thatLabel.strikethrough
            self.isItalic =         thatLabel.italic
            self.isUnderline =      thatLabel.underline
        # If we are copying from a button
        elif(thatButton != None):
            self.size =             thatButton.font_size
            self.blended =          thatButton.font_blended
            self.context =          thatButton.font_context
            self.name =             thatButton.font_name
            self.family =           thatButton.font_family
            self.kerning =          thatButton.font_kerning
            self.hinting =          thatButton.font_hinting

            self.isBold =           thatButton.bold
            self.isStrikethrough =  thatButton.strikethrough
            self.isItalic =         thatButton.italic
            self.isUnderline =      thatButton.underline
        # If we are copying from a textinput
        elif(thatTextInput != None):
            self.size =             thatTextInput.font_size
            self.blended =          thatTextInput.font_blended
            self.context =          thatTextInput.font_context
            self.name =             thatTextInput.font_name
            self.family =           thatTextInput.font_family
            self.kerning =          thatTextInput.font_kerning
            self.hinting =          thatTextInput.font_hinting

            self.isBold =           thatTextInput.bold
            self.isStrikethrough =  thatTextInput.strikethrough
            self.isItalic =         thatTextInput.italic
            self.isUnderline =      thatTextInput.underline

        #If we are copying from an other font class
        elif(thatFont != None):
            self.size =             thatFont.size
            self.blended =          thatFont.blended
            self.context =          thatFont.context
            self.name =             thatFont.name
            self.family =           thatFont.family
            self.kerning =          thatFont.kerning
            self.hinting =          thatFont.hinting

            self.isBold =           thatFont.isBold
            self.isStrikethrough =  thatFont.isStrikethrough
            self.isItalic =         thatFont.isItalic
            self.isUnderline =      thatFont.isUnderline

        del thatButton
        del thatLabel
        del thatTextInput
        del thatFont
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self):
        """
        Initializes all the class's members to their default values:
            - size =            '15sp'
            - context =         "None"
            - name =            'Roboto'
            - family =          "None"
            - hinting =         'normal'
            - kerning =         True
            - blended =         True
            - isBold =          False
            - isStrikethrough = False
            - isItalic =        False
            - isUnderline =     False
            .
        """
        self.size = '15sp'
        self.blended = True
        self.context = "None"
        self.name = 'Roboto'
        self.family = "None"
        self.kerning = True
        self.hinting = 'normal'

        self.isBold = False
        self.isStrikethrough = False
        self.isItalic = False
        self.isUnderline = False
        return
    #endregion
    pass
#====================================================================#
LoadingLog.End("font.py")