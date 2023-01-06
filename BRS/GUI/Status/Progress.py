#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from BRS.Utilities.states import States,StatesColors
from BRS.GUI.Utilities.font import Font
from BRS.Debug.consoleLog import Debug

from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.clock import Clock
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Bar(ProgressBar, Widget):
    #region   --------------------------- DOCSTRING
    ''' 
    '''
    #endregion
    #region   --------------------------- MEMBERS
    _wantedValue : float = 0
    #endregion
    #region   --------------------------- GET SET
    @property
    def State(self) -> int:
        return self._state

    @State.setter
    def State(self, newState:States) -> None:
        #Save new state in private variable
        self._state = newState

        #Set new colors to use depending on button's current Kivy state
        """ if self.state == "down":  # if the button is being pressed
            self.color.rgba = StatesColors.Pressed.GetColorFrom(self.State)
            self._label.color = StatesColors.Text.GetColorFrom(self.State)
        else:
            self.color.rgba = StatesColors.Default.GetColorFrom(self.State)
            self._label.color = StatesColors.Text.GetColorFrom(self.State) """
    # ------------------------------------------------------
    @property
    def Value(self) -> int:
        return self.value

    @Value.setter
    def Value(self, wantedValue:float) -> None:
        #Save new state in private variable
        self._wantedValue = wantedValue
        Clock.schedule_once(self._UpdateValue, 0.1)

    #endregion
    #region   --------------------------- METHODS
    def _UpdateValue(self, dt):
        print("PROGRESS BAR GO BR")
        if(self.value != self._wantedValue):
            if(self.value < self._wantedValue):
                self.value = self.value + 1
            else:
                self.value = self.value - 1
            Clock.schedule_once(self._UpdateValue, 0.01)


    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass