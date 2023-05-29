#====================================================================#
# File Information
#====================================================================#
"""
    textfield.py
    ============
    I truly don't know why this isn't already a standard Kivy feature
    when you specify that you're running on mobile touchscreen without
    keyboards but who knows.

    This file contains a class that can be used to replace your
    textfield. It uses the Information class to detect if you're
    running on Linux or other platforms to detect if you should
    have a pop up virtual keyboard or not.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("textfield.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ..Utilities.colors import GetPrimaryColor, GetAccentColor
from ..Utilities.references import Shadow, Rounding
from ...Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.vkeyboard import VKeyboard
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class VirtualKeyboardTextField(MDTextField):
    """
        VirtualKeyboardTextField:
        =========================
        Summary:
        --------
        Class that replaces :ref:`MDTextField`.
        Replace any MDTextField you have in your
        application by this class in order to have
        a pop up keyboard displayed on Linux devices
        and nothing different happen on Windows device.

        Warning:
        --------
        This automatically makes use of the Information
        class located in BRS.Utilities.Information.
        Do not separate this class from this file.
    """
    dialogShown:bool = None
    """
        reference to the dialog created
        when on_focus is called.
    """
    oldText:str = None
    """
        reference to the previous
        text that was in the textField
        so the cancel button works.
    """
    capslockState:bool = False
    """
        Used to keep track of the virtual
        keyboard's capslock state.

        DONT MESS WITH THIS ONE BRUH.
    """

    alwaysDisplayKeyboard:bool = False
    """
        alwaysDisplayKeyboard:
        ======================
        Summary:
        --------
        Setting this to true will
        always deploy a virtual
        keyboard on your screen
        when you focus on the textfield.
        Otherwise, ONLY LINUX MACHINES WILL
        POP UP A KEYBOARD. this is because
        there's ain't no way I can check
        if you got access to some keyboards.
    """

    def __init__(self, **kwargs):
        super(VirtualKeyboardTextField, self).__init__(**kwargs)

    def _CreateDialog(self, *args):
        """
            _CreateDialog:
            ==============
            Summary:
            --------
            Creates and shows the pop up
            dialog with its keyboard.

            THIS IS CALLED INTERNALLY... but
            if you really wanted to, you could
            force display it by simply calling
            this method. It should still work.
        """
        if(self.dialogShown != True):
            # Create dialog
            self.dialog = MDDialog(
                title=self.hint_text,
                type = "custom",
                buttons=[
                    MDFlatButton(text=_("Cancel"), on_release = self.Cancel),
                    MDFillRoundFlatButton(text=_("Confirm"), on_release = self.Confirm)
                ]
            )
            self.dialog.text = self.text + "_"
            self.dialog.auto_dismiss = False

            self.dialog.elevation = Shadow.Elevation.default
            self.dialog.shadow_softness = Shadow.Smoothness.default
            self.dialog.shadow_radius = Rounding.default
            self.dialog.radius = [Rounding.default, Rounding.default, Rounding.default, Rounding.default]

            self.dialog.pos_hint = {"center_y":0.75}

            self.keyboardLayout = MDFloatLayout()
            self.virtualKeyboard = VKeyboard(on_key_up = self.KeyUp, pos_hint={"center_x":0.5})

            self.virtualKeyboard.key_background_color = GetAccentColor("Light")
            self.virtualKeyboard.background_color = GetAccentColor("Dark")
            self.virtualKeyboard.have_shift = False
            self.virtualKeyboard.have_special = False
            self.keyboardLayout.add_widget(self.virtualKeyboard)
            self.dialog.add_widget(self.keyboardLayout)
            self.dialogShown = True
            self.capslockState = False
            self.oldText = self.text
            self.dialog.open()

    def Cancel(self, *args):
        """
            CALLBACK when cancel button is pressed.
            Dont use this manually and dont overwrite it.
        """
        self.text = self.oldText
        self.dialog.dismiss()

    def Confirm(self, *args):
        """
            CALLBACK when the confirm button is pressed.
            Dont use this manually and dont overwrite it.
        """
        self.text = self.dialog.text[:-1] # removes the underscore
        self.dialog.dismiss()

    def KeyUp(self, keyboard, keycode, *args):
        """
            KeyUp:
            ======
            Summary:
            --------
            Function executed when a key is
            released on the virtual keyboard

            Warning:
            --------
            Shift does not work.
            layout and escape button are disregarded.
            Do not use this manually.
        """
        if isinstance(keycode, tuple):
            keycode = keycode[1]

        previousText = self.dialog.text[:-1]

        if(keycode == "backspace"):
            previousText = previousText[:-1]
            keycode = ""

        if(keycode == "spacebar"):
            keycode = " "

        if(keycode == "tab"):
           keycode = "    "

        if(keycode == "layout"):
            #Couldn't be bothered tbh
            return

        if(keycode == "shift"):
            #Couldn't be bothered tbh
            return

        if(keycode == "escape"):
            self.Cancel()
            self.focus = False
            return

        if(keycode == "capslock"):
           keycode = ""
           self.capslockState = not self.capslockState

        if(keycode == "enter"):
            self.Confirm()
            self.focus = False
            return

        if(keycode == "None" or keycode == "none" or keycode == None):
            return

        if(self.capslockState):
            keycode = keycode.upper()

        self.dialog.text = f"{previousText}{keycode}_"

    def on_focus(self, instance_text_field, focus: bool) -> None:
        """
            on_focus:
            =========
            Summary:
            --------
            Do not overwrite this function. Otherwise,
            the dialogs won't be created.
            This is a copy paste from KivyMD MDTextfield
            with the added dialog creation in it.
        """
        if focus:

            self.oldText = self.text

            if(Information.platform == "Linux" or self.alwaysDisplayKeyboard):
                self._CreateDialog()

            if self.mode == "rectangle":
                self.set_notch_rectangle()
            self.set_static_underline_color([0, 0, 0, 0])
            if (
                self.helper_text_mode in ("on_focus", "persistent")
                and self.helper_text
            ):
                self.set_helper_text_color(self.helper_text_color_focus)
            if self.mode == "fill":
                self.set_fill_color(self.fill_color_focus)
            self.set_active_underline_width(self.width)

            self.set_pos_hint_text(
                (28 if self.mode != "line" else 18)
                if self.mode != "rectangle"
                else 10
            )
            self.set_hint_text_color(focus)
            self.set_hint_text_font_size(12)

            if self.max_text_length:
                self.set_max_length_text_color(self.max_length_text_color)
            if self.icon_right:
                self.set_icon_right_color(self.icon_right_color_focus)
            if self.icon_left:
                self.set_icon_left_color(self.icon_left_color_focus)

            if self.error:
                if self.hint_text:
                    self.set_hint_text_color(focus, self.error)
                if self.helper_text:
                    self.set_helper_text_color(self.error_color)
                if self.max_text_length:
                    self.set_max_length_text_color(self.error_color)
                if self.icon_right:
                    self.set_icon_right_color(self.error_color)
                if self.icon_left:
                    self.set_icon_left_color(self.error_color)
        else:
            self.dialogShown = False
            if self.helper_text_mode == "persistent" and self.helper_text:
                self.set_helper_text_color(self.helper_text_color_normal)
            if self.mode == "rectangle" and not self.text:
                self.set_notch_rectangle(joining=True)
            if not self.text:
                if self.mode == "rectangle":
                    y = 38
                elif self.mode == "fill":
                    y = 46
                else:
                    y = 34

                self.set_pos_hint_text(y)
                self.set_hint_text_font_size(16)
            if self.icon_right:
                self.set_icon_right_color(self.icon_right_color_normal)
            if self.icon_left:
                self.set_icon_left_color(self.icon_left_color_normal)
            if self.hint_text:
                self.set_hint_text_color(focus, self.error)

            self.set_active_underline_width(0)
            self.set_max_length_text_color([0, 0, 0, 0])

            if self.mode == "fill":
                self.set_fill_color(self.fill_color_normal)

            self.error = self._get_has_error() or self.error
            if self.error:
                self.set_static_underline_color(self.error_color)
            else:
                self.set_static_underline_color(self.line_color_normal)

#====================================================================#
LoadingLog.End("textfield.py")