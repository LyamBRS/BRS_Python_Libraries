#====================================================================#
# File Information
#====================================================================#
"""
    ObjectView.py
    =============
    This file contains what's necessary to render a 3D object on
    your monitor in a KivyMD application.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ....BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("objectView.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy.graphics import RenderContext, Callback, PushMatrix, PopMatrix, Color, Translate, Rotate, Mesh, UpdateNormalMatrix
from .objloader import ObjFile
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#
def Lerp(current,wanted, delta):
    return current * (1-delta) + wanted * delta
#====================================================================#
# Classes
#====================================================================#
class ObjViewer(Widget):
    #region   --------------------------- DOCSTRING
    """
        ObjViewer:
        ===========
        Summary:
        --------
        Class built from Kivy's monkey 3D object example.
        This class allows easy implementation of simple
        3D objects into your MDApp.

        Warning:
        --------
        Your OBJ file must not use squares. Files with
        squares will render with holes. Only triangles
        work.
    """
    #endregion
    #region   --------------------------- MEMBERS
    ambiantLight = (0.1, 0.1, 0.1)
    """
        ambiantLight:
        =============
        Summary:
        --------
        The ambiant light around the rendered object. 
        This is only updated when :ref:`update_glsl` is
        called. Values needs to be within 0 and 1.
        Defaults to (0.1, 0.1, 0.1).
    """

    diffuseLight = (1.0, 1.0, 0.8)
    """
        ambiantLight:
        =============
        Summary:
        --------
        The diffused light around the rendered object. 
        This is only updated when :ref:`update_glsl` is
        called. Values needs to be within 0 and 1.
        Defaults to (1.0, 1.0, 0.8).
    """

    fov = 1
    """
        fov:
        ====
        Summary:
        --------
        The FOV with which the object is rendered.
        Defaults to 1.
    """

    _degreesX:int = 0
    _degreesY:int = 0
    _degreesZ:int = 0
    manuallyUpdated:bool = False

    RotationX = Rotate(0, 1, 0, 0)
    """
        RotationX:
        ==========
        Summary:
        --------
        Rotation object. This one controls the X axis.
        This means that if your object is a plane that is centered
        on 0,0,0 and points towards the negative Y axis,
        this object would allow you to roll the plane.
        This takes values in degrees

        Warning:
        --------
        Do not manually use this. Use SetAngles instead.
        if you're using continuous updates, it will lerp
        the current angle with the wanted one.
    """
    RotationY = Rotate(0, 0, 0, 1)
    """
        RotationY:
        ==========
        Summary:
        --------
        Rotation object. This one controls the X axis.
        This means that if your object is a plane that is centered
        on 0,0,0 and points towards the negative Y axis,
        this object would allow you to pitch the plane.
        This takes values in degrees

        Warning:
        --------
        Do not manually use this. Use SetAngles instead.
        if you're using continuous updates, it will lerp
        the current angle with the wanted one.
    """
    RotationZ = Rotate(0, 0, 1, 0)
    """
        RotationZ:
        ==========
        Summary:
        --------
        Rotation object. This one controls the X axis.
        This means that if your object is a plane that is centered
        on 0,0,0 and points towards the negative Y axis,
        this object would allow you to yaw the plane.
        This takes values in degrees

        Warning:
        --------
        Do not manually use this. Use SetAngles instead.
        if you're using continuous updates, it will lerp
        the current angle with the wanted one.
    """
    #endregion
    #region   --------------------------- METHODS
    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def SetNewAngles(self, newX=None, newY=None, newZ=None):
        """
            SetNewAngles:
            =============
            Summary:
            --------
            Sets new wanted angles for the object's
            axes. If equal to `None`, the old value
            will be kept instead.

            if your object was not created with
            automatic updates, this will call
            manual update and angles will be set
            automatically.
        """
        needToUpdate:bool = False
        
        if(newX != None):
            if(newX != self._degreesX):
                self._degreesX = newX
                needToUpdate = True

        if(newY != None):
            if(newY != self._degreesY):
                self._degreesY = newY
                needToUpdate = True

        if(newZ != None):
            if(newZ != self._degreesZ):
                self._degreesZ = newZ
                needToUpdate = True

        if(self.manuallyUpdated == True):
            if(needToUpdate):
                self.update_glsl(1)

    def update_glsl(self, delta):
        try:
            asp = self.width / float(self.height)
            proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, self.fov)
            self.canvas['projection_mat'] = proj
    
            self.canvas['diffuse_light'] = self.diffuseLight
            self.canvas['ambient_light'] = self.ambiantLight
    
            if(not self.manuallyUpdated):
                self.RotationX.angle = Lerp(self.RotationX.angle, self._degreesX, 0.01)
                self.RotationY.angle = Lerp(self.RotationY.angle, self._degreesY, 0.01)
                self.RotationZ.angle = Lerp(self.RotationZ.angle, self._degreesZ, 0.01)
            else:
                self.RotationX.angle = self._degreesX
                self.RotationY.angle = self._degreesY
                self.RotationZ.angle = self._degreesZ
        except:
            Clock.unschedule(self.update_glsl)

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0, 0, -3)
        self.RotationX = Rotate(0, 1, 0, 0)
        self.RotationY = Rotate(0, 0, 0, 1)
        self.RotationZ = Rotate(0, 0, 1, 0)

        m = list(self.scene.objects.values())[0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=m.vertices,
            indices=m.indices,
            fmt=m.vertex_format,
            mode='triangles',
        )
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, 
                 pathToOBJ:str = "", 
                 pathToglsl:str = "simple.glsl", 
                 updateIntervals = 1/60.,
                 diffusedLight = (1.0, 1.0, 0.8),
                 ambiantLight = (0.1, 0.1, 0.1),
                 updatedManually:bool = False,
                 **kwargs):

        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find(pathToglsl)
        self.scene = ObjFile(resource_find(pathToOBJ))
        super(ObjViewer, self).__init__(**kwargs)

        self.ambiantLight = ambiantLight
        self.diffuseLight = diffusedLight
        self.manuallyUpdated = updatedManually

        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)

        if(not updatedManually):
            Clock.schedule_interval(self.update_glsl, updateIntervals)
        else:
            Clock.schedule_once(self.update_glsl, 0.1)
    #endregion
    pass
#====================================================================#
LoadingLog.End("objectView.py")