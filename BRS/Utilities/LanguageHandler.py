#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from ..Debug.LoadingLog import LoadingLog
LoadingLog.Start("LanguageHandler.py")

import os
from .FileHandler import FilesFinder,IsPathValid
from ..Debug.consoleLog import Debug
import gettext
from .FileHandler import AppendPath
#====================================================================#
# Functions
#====================================================================#
def _(string:str) ->str:
    """
        Translation unit used by gettext GNU API.
        You need to have built Applanguage prior to using this.
        Otherwise, it will simply return the input string no less.
    """
    Debug.Start("_ translator", DontDebug=True)
    Debug.Log(f"Amount of times overwrote: {AppLanguage.OverWriteCount}")
    Debug.Log(f"Language used: {AppLanguage.Current}")

    string = AppLanguage.Translate(string)
    # Debug.Log(f"Result: {string}")
    Debug.End(ContinueDebug=True)
    return string
#====================================================================#
# Classes
#====================================================================#
class AppLanguage:
    #region   --------------------------- DOCSTRING
    '''
        Class that loads all the available language packs at the start
        of the application.

        Also allows translations of words.
        Not used in the library.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    OverWriteCount:int = 0

    pathToLanguageFolders:str = None
    """
        The path to the folder which contains the language folders.
        Defaults to `None`
    """
    AvailableLanguages:list = None
    """
        List of all the available languages defined by their folders names.
        Defaults to `None`
    """
    Current:str = None
    """
        Holds the name of the folder of the current language.
        Defaults to `None`
    """
    LanguageFiles:FilesFinder = None
    """
        Holds the FilesFinder class which holds all the language files loaded.
        Defaults to `None`
    """
    #endregion
    #region   --------------------------- METHODS
    def LoadLanguage(language:str) -> bool:
        """
            LoadLanguage:
            =============
            Summary:
            --------
            Function that allows you to change the application's currently loaded language.
            Loads the default when building the class.

            Returns:
            --------#####################################
                - True: Successfully loaded the language
                - False: Could not load the language
        """
        Debug.Start("AppLanguage.LoadLanguage")
        path = AppLanguage.pathToLanguageFolders

        # - Setting new current language
        AppLanguage.Current = language

        # - Check if the locale path is still valid
        if(IsPathValid(path)):
            # - Find all the language files available at the specified path.
            newPath = AppendPath(path, "\\")
            newPath = AppendPath(newPath, language + "\\LC_MESSAGES\\")
            AppLanguage.LanguageFiles = FilesFinder(".mo", newPath)
            Debug.Log(f"Locale path: {path}")
            Debug.Log(f"Loading language: {language}")
            Debug.Log(f"Compiled files found: {AppLanguage.LanguageFiles.fileList}")

            # - Create the translation from the main Messages file.
            trans = gettext.translation("Messages", localedir=path, languages=[language])

            # - Add the fallback .mo files to the main Messages file
            for langFile in AppLanguage.LanguageFiles.fileList:
                if(langFile != "Messages.mo"):
                    langFile = langFile.replace(".mo","")
                    Debug.Log(f"Added: {langFile}, as a fallback")
                    trans.add_fallback(gettext.translation(langFile, localedir=path, languages=[language]))

            # - Overwrite the translation function to the gettext equivalent
            Debug.Warn("Overwriting _ function")
            AppLanguage.OverWriteCount = AppLanguage.OverWriteCount+1
            AppLanguage.Translate = trans.gettext
            Debug.End()
            return True
        else:
            Debug.End()
            return False

    def Translate(string:str)->str:
        """
            Interfaces gettext api and returns the translated string
        """
        Debug.Start("AppLanguage.Translate default function", DontDebug=True)
        Debug.Warn(f"Returning {string} untranslated")
        Debug.End(ContinueDebug=True)
        return string
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self,
                 pathToLanguageFolders:str,
                 defaultLanguage:str
                 ):
        Debug.Start("AppLanguage: Init")

        # Check if path is valid
        valid = IsPathValid(pathToLanguageFolders)
        if(not valid):
            raise(f"Invalid language folder path given: {pathToLanguageFolders}")
        self.pathToLanguageFolders = pathToLanguageFolders

        # Get all the folders available
        dirs = [name for name in os.listdir(pathToLanguageFolders) if os.path.isdir(os.path.join(pathToLanguageFolders, name))]
        self.AvailableLanguages = dirs

        # Check if default language is found inside of the available languages
        if(defaultLanguage in dirs):
            self.Current = defaultLanguage
            Debug.Log(f"Initialisation successful, {self.Current} is being loaded")
            self.LoadLanguage(self.Current)
        else:
            raise("Default language does not exist in the list of available languages")
        Debug.End()
    #endregion
    pass

LoadingLog.End("LanguageHandler.py")