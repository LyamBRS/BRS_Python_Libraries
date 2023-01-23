#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
from kivy.graphics.svg import Svg
from kivy.uix.widget import Widget
from kivy.graphics import RoundedRectangle
from kivy.graphics import MatrixInstruction, Translate, PopMatrix, PushMatrix
from kivy.graphics.transformation import Matrix
from kivy.uix.image import Image


from BRS.GUI.Utilities.drawings import BRS_SVGWidgetAttributes
from BRS.Utilities.states import States,StatesColors
from BRS.Debug.consoleLog import Debug
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class SVGDisplay(Widget, BRS_SVGWidgetAttributes):
    #region   --------------------------- DOCSTRING
    '''
    '''
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    #region   -- Private
    # ------------------------------------------------------
    def _AnimatingShapes(self, animation, value, theOtherOne):
        """
            Called when Animations are executed.
            Call which shapes need to be set to new values here.

            See PieChartDial for an example.
        """
        Debug.Start("SVGDisplay: _AnimatingShapes")

        # [Step 2]: Update background's positions
        self.background.pos   = (self._current_pos[0], self._current_pos[1])
        self.background.size  = (self._current_size[0], self._current_size[1])
        Debug.End()
    # ------------------------------------------------------
    def _AnimatingColors(self, animation, value, theOtherOne):
        """ Called when color related animations are executed """
        Debug.Start("_AnimatingColors")

        # [Step 0]: Update widget's colors with these colors
        Debug.Log("Color = {}".format(self._current_trackColor))
        self.backgroundColor.rgba   = self._current_backgroundColor
        Debug.End()
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, initialState = States.Disabled, file = "", radius=10, **kwargs):
        super(SVGDisplay, self).__init__(**kwargs)
        Debug.Start("SVGDisplay")
        #region --------------------------- Set Variables
        self.radius = radius
        self._svg_path = file
        #endregion
        #region --------------------------- Set Classes
        #endregion
        #region --------------------------- Set Canvas
        with self.canvas:
            # Color setups and variables

            # Background
            self.background = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.radius, self.radius, self.radius, self.radius])

            # SVG
            PushMatrix()
            self.matrix = MatrixInstruction()
            self.matrix.matrix = Matrix().scale(0.5,0.5,1)
            self.translate = Translate(self.pos[0],self.pos[1])
            self.svg = Svg(self._svg_path)
            PopMatrix()

            # Binding events
            self.bind(pos=self._UpdateShape, size=self._UpdateShape)
        #endregion
        #region --------------------------- Set Widgets
        #endregion
        #region --------------------------- Set GetSets
        self.State = initialState
        #endregion
        Debug.End()
    #endregion
    pass