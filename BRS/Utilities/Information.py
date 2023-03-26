#====================================================================#
#region ---- File Information
#====================================================================#
"""
    Information.py
    ==============
    This file holds a class which purpose is to hold all the generic
    information gathered when running your application. For example,
    this class can hold the python version running the application,
    the OS that is running it and other various precious information
    that you may want to access without having to constantly call
    functions to get it.
"""
#endregion
#====================================================================#
#region ---- Loading Logs
#====================================================================#
from ...BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Information.py")
#endregion
#====================================================================#
#region ---- Imports
#====================================================================#
#region ------------------------------------------------------ Python
#endregion
#region --------------------------------------------------------- BRS
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
#endregion
#endregion
#====================================================================#
#region ---- Functions
#====================================================================#
#endregion
#====================================================================#
#region ---- Classes
#====================================================================#
LoadingLog.Class("AppInfo")
class AppInfo:
    #region   --------------------------------------------- DOCSTRING
    '''
        AppInfo:
        ========
        Summary:
        --------
        Class holding your application's informations so that it can
        be accessed by other python scripts easily without having to
        call multiple functions.

        Members:
        --------
        - OS
        - Hardware
        - Framework
        - Version
        - Name
        - Description

        Methods:
        --------

        Methods:
        --------
    '''
    #endregion
    #region   ----------------------------------------------- MEMBERS
    OS:str = None
    '''
        OS:
        ===
        Summary:
        --------
        String member which holds the OS which is running your application.
        The possible values that this member can hold are listed in the
        next section. You need to fill this yourself at some point during the
        launching of your application.

        Values:
        -------
        - `None` : Default value
        - `"Windows"` : The application is running on Windows.
        - `"Linux"` : The application is running on a Linux distro
        - `"MacOS"` : The application is running on an Apple desktop
        - `"IOS"`   : The application is running on an Apple phone
        - `"Android"`: The application is running on Android
    '''
    # ---------------------------------------------------------------
    Hardware:str = None
    '''
        Hardware:
        =========
        Summary:
        --------
        String type member which purpose is to hold the type of
        hardware that is currently running your Python application.
        You need to figure out yourself a way to detect this. The
        possible values that this member can hold are defined in
        the next section.

        Values:
        -------
        - `None`: Default value.
        - `Desktop` : The application is running on a desktop or laptop.
        - `Server` : The application is running on a server.
        - `Mobile` : The application is running on a mobile device.
        - `IoT` : The application is running on an IoT such as Raspberry Pi.
        - `Web` : The application is running on a website environement.
        - `VM`  : The application is running on a virtual machine of some sort.
    '''
    # ---------------------------------------------------------------
    Framework:str = None
    '''
        Framework:
        =========
        Summary:
        --------
        String type member which purpose is to hold the type of
        framework that is currently running your Python application.
        You need to figure out yourself a way to detect this. Some
        of the possible values that this member can hold are defined
        in the next section.

        Values:
        -------
        - `None`: Default value.
        - `"Kivy"` : The application is running Kivy
        - `"KivyMD"` : The application is running KivyMD
    '''
    # ---------------------------------------------------------------
    Version:str = None
    '''
        Version:
        ========
        Summary:
        --------
        String type member which purpose is to hold the version of
        your application. The version must not have any letters in
        it to simplify the decryption by other python scripts.
        You need to set this yourself one way or an other.
        The possible values for this are endless although some are
        defined in the next section for uniformisation purposes.

        Values:
        -------
        - `None`: Default value.
        - `"Dev"` : Developement version.
    '''
    # ---------------------------------------------------------------
    Name:str = None
    '''
        Name:
        =====
        Summary:
        --------
        String type member which purpose is to hold the name of
        your application. Defaults to `None`.
    '''
    # ---------------------------------------------------------------
    Description:str = None
    '''
        Description:
        ============
        Summary:
        --------
        String type member which purpose is to hold the description of
        your application. It's goal is to be a short or long description
        of your application.
        Defaults to `None`.
    '''
    # ---------------------------------------------------------------
    #endregion
    #region   ----------------------------------------------- CLASSES
    class CanUse:
        '''
            CanUse:
            =======
            Summary:
            --------
            Defines if your application can use one of various
            external or internal components. This class is filled
            with members which are by default equal to `None` but
            should only be set to `True` or `False` when defined.

            Members:
            --------
            - `Internet (bool)`: Defaults to `None`.
            - `GPIO (bool)`: Defaults to `None`.
            - `BlueTooth (bool)`: Defaults to `None`.
            - `Ethernet (bool)`: Defaults to `None`.
            - `WiFi (bool)`: Defaults to `None`.
            - `UART (bool)`: Defaults to `None`.
            - `USB (bool)`: Defaults to `None`.
            - `AudioOutput (bool)`: Defaults to `None`.
            - `AudioInput (bool)`: Defaults to `None`.
            - `Camera (bool)`: Defaults to `None`.
            - `Languages (bool)`: Defaults to `None`
        '''
        Internet:bool = None
        '''
            Internet:
            =========
            Summary:
            --------
            Member which default value is `None`.
            If you set it to `True`, your application can successfully
            access anything on the internet. If set to `False`, your
            application has no internet access.

            Warning:
            --------
            Some BRS_Python_Libraries function may set this automatically
            when called.
        '''
        GPIO:bool = None
        '''
            GPIO:
            =====
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can use some sort of
            GPIO functionalities. If set to `False`, your application
            cannot use any sort of GPIO functionalities.
        '''
        Bluetooth:bool = None
        '''
            Bluetooth:
            ==========
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can use Bluetooth
            functionalities to connect or detect devices.
            If set to `False`, your application has no control of
            any sort of Bluetooth functionalities.
        '''
        Ethernet:bool = None
        '''
            Ethernet:
            =========
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can use Ethernet
            functionalities. Otherwise, no Ethernet is available
            or can be used.
            This differs from :ref:`Internet` as this only
            indicates if Ethernet can be used, not if the Ethernet
            has internet access.
        '''
        WiFi:bool = None
        '''
            WiFi:
            =====
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can use WiFi
            functionalities. Otherwise, no WiFi is available
            or can be used.
            This differs from :ref:`Internet` as this only
            indicates if WiFi can be used, not if the WiFi
            has internet access.
        '''
        UART:bool = None
        '''
            UART:
            =====
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can use UART
            functionalities. Otherwise, no UART functionalities
            can be used by your application.
        '''
        USB:bool = None
        '''
            USB:
            =====
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can use USB
            for various purposes which you define yourself.
            Otherwise, your application cannot use any sort
            of USB device or connection.
        '''
        AudioOutput:bool = None
        '''
            AudioOutput:
            ============
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can output
            audio in a way or another.
            Otherwise, your application cannot output
            audio in any ways shape or form.
        '''
        AudioInput:bool = None
        '''
            AudioInput:
            ==========
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can gather
            audio in a way or another.
            Otherwise, your application cannot gather
            audio in any ways shape or form.
        '''
        Camera:bool = None
        '''
            Camera:
            =======
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can gather
            video feed from a local camera.
            Otherwise, your application cannot gather
            video feed in any ways shape or form.
        '''
        Languages:bool = None
        '''
            Languages:
            ==========
            Summary:
            --------
            Member which default value is `None`.
            If set to `True`, your application can set
            a language by following the internalisation standard.
            Otherwise, your application has no way of changing it's
            language.

            See :ref:`LanguageHandler.py` for more information on
            languages.
        '''
    #endregion
    #region   ----------------------------------------------- METHODS
    #endregion
    pass
#endregion
#====================================================================#
LoadingLog.End("Information.py")