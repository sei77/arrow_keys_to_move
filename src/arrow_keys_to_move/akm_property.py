import bpy

from bpy.props import IntProperty, FloatProperty, FloatVectorProperty, BoolProperty

# プロパティの初期化
def init_props():
    bpy.types.Scene.akm_move_amt = FloatProperty(default=0.2, min=0.1, max=0.5)
    bpy.types.Scene.akm_center   = BoolProperty(default=True)

# プロパティのクリア
def clear_props():
    del bpy.types.Scene.akm_move_amt
    del bpy.types.Scene.akm_center

