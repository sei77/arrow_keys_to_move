import bpy
import bmesh
from bpy.types import Panel, UIList, Operator
from bpy.props import IntProperty, FloatProperty, FloatVectorProperty, BoolProperty

# パネル登録
class AMT_PT_MainPanel(bpy.types.Panel):

    bl_label = "Arrow Keys to move"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Arrow Move"
    bl_context = "mesh_edit"
    
    def draw(self, context):
        
        layout = self.layout
        scene  = context.scene
        
        layout.prop(scene, "akm_center", text="Center of selected vertex")
        layout.prop(scene, "akm_move_amt", text="Amount of movement")


# 登録処理
def register():
    bpy.utils.register_class(AMT_PT_MainPanel)

# 登録解除処理
def unregister():
    bpy.utils.unregister_class(AMT_PT_MainPanel)

