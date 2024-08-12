import bpy

from bpy.props import IntProperty, FloatProperty, FloatVectorProperty, BoolProperty

# プロパティの初期化
def init_props():
    bpy.types.Scene.akm_move_amt    = FloatProperty(default=0.10, min=0.10, max=0.50)
    bpy.types.Scene.akm_center      = BoolProperty(default=False)
    bpy.types.Scene.akm_hide_vert   = BoolProperty(default=True)
    bpy.types.Scene.akm_hide_view   = BoolProperty(default=True)
    bpy.types.Scene.akm_show_retopo = BoolProperty(default=False)
    bpy.types.Scene.akm_xray        = BoolProperty(default=False)

# プロパティのクリア
def clear_props():
    del bpy.types.Scene.akm_move_amt
    del bpy.types.Scene.akm_center
    del bpy.types.Scene.akm_hide_vert
    del bpy.types.Scene.akm_hide_view
    del bpy.types.Scene.akm_show_retopo
    del bpy.types.Scene.akm_xray

