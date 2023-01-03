from logging import exception
from typing import Any
from BRS.References.states import States
from kivy.uix.button import Button
######################################################################
class Font:
    '''The font class is used to specify a font for text based data in a GUI
    This is used by larger GUI classes like buttons and labels for example'''

    #------------------------------------------# MEMBERS
    #region MEMBERS
    color: Any
    '''[KIVY]: rgba. defaults to: [1,1,1,1]'''
    size : Any
    '''[KIVY]: Font size of the text, in pixels.'''
    blended : bool
    '''Whether blended or solid font rendering should be used.'''
    context : Any
    '''[KIVY]: Font context. None means the font is used in isolation, so you are guaranteed to be drawing with the TTF file resolved by font_name. Specifying a value here will load the font file into a named context, enabling fallback between all fonts in the same context. If a font context is set, you are not guaranteed that rendering will actually use the specified TTF file for all glyphs (Pango will pick the one it thinks is best).'''
    family : str
    '''[KIVY]: Font family, this is only applicable when using font_context option. The specified font family will be requested, but note that it may not be available, or there could be multiple fonts registered with the same family.'''
    features : str
    '''[KIVY]: OpenType font features, in CSS format, this is passed straight through to Pango. The effects of requesting a feature depends on loaded fonts, library versions, etc. For a complete list of features, see:'''
    hinting : str
    '''[KIVY]: normal, light, mono'''
    name : str
    '''[KIVY]: filename of the font to use'''
    kerning : bool
    '''[KIVY]: Whether kerning is enabled for font rendering. You should normally only disable this if rendering is broken with a particular font file.'''

    bold : bool
    italic : bool
    underline : bool
    strikethrough : bool
    #endregion
    #------------------------------------------#

    #------------------------------------------# CONSTRUCTORS
    def __init__(self):
        self.size = '15sp'
        self.blended = True
        self.context = "None"
        self.name = 'Roboto'
        self.family = "None"
        self.features = ""
        self.kerning = True
        self.hinting = 'normal'
        self.color = [1,1,1,1]
        self.bold = False
        self.strikethrough = False
        self.italic = False
        self.underline = False
        return
    '''Will instanciate a standard Kivy button where each attributes will have to be manually specified afterwards'''
    #------------------------------------------#