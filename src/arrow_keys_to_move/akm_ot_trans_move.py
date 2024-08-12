import bpy
import bmesh
import bpy_extras.view3d_utils
import mathutils
from mathutils import Vector

def move_vertex_to_view(context, x, y):
    # 現在の視点の方向を取得
    view_vector = context.region_data.view_rotation @ Vector((x, y, 0.0))
    
    # アクティブオブジェクトのメッシュデータを取得
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    # 選択された頂点を取得し、視点の方向に移動
    m = (x + y)
    for v in bm.verts:
        if v.select:
            if m < 0.0:
                v.co -= view_vector * m
            else:
                v.co += view_vector * m
    bmesh.update_edit_mesh(me)

class AKM_OT_ArrowMove(bpy.types.Operator):
    bl_idname = "akm.trans_move"
    bl_label  = "Arrow Keys to move"
    bl_options = {'REGISTER', 'UNDO'}
    
    def __init__(self):
        self.original_show_floor  = None
        self.original_show_axis_x = None
        self.original_show_axis_y = None
        self.original_show_cursor = None
        self.original_show_origin = None
        self.original_show_retopo = None
        self.original_cursor_location = None
        self.original_object_location = None
        self.original_sharing_xray = None
        
    def modal(self, context, event):
        
        # 編集を確定
        if event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'}:
            self.restore_view(context)
            if bpy.context.scene.akm_hide_vert:
                self.restore_verts_disp(context)
            context.area.header_text_set(None)
            return {'FINISHED'}
        # キャンセル
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.restore_view(context)
            self.restore_verts(context)
            if bpy.context.scene.akm_hide_vert:
                self.restore_verts_disp(context)
            context.area.header_text_set(None)
            return {'CANCELLED'}
        
        # 透過表示切替
        if event.type in {'X'} and event.value == 'PRESS':
            shading = context.space_data.shading
            if shading.show_xray:
                shading.show_xray = False
            else:
                shading.show_xray = True
            bpy.context.scene.akm_xray = shading.show_xray
        
        # リトポロジー切替
        if event.type in {'R'} and event.value == 'PRESS':
            space_data = context.space_data
            if space_data.overlay.show_retopology:
                space_data.overlay.show_retopology = False
            else:
                space_data.overlay.show_retopology = True
            bpy.context.scene.akm_show_retopo = space_data.overlay.show_retopology
        
        # 移動量変更
        move_amt = bpy.context.scene.akm_move_amt
        if event.ctrl:
            if event.type == 'WHEELUPMOUSE':
                if move_amt > 0.10:
                    bpy.context.scene.akm_move_amt -= 0.01
            if event.type == 'WHEELDOWNMOUSE':
                if move_amt < 0.50:
                    bpy.context.scene.akm_move_amt += 0.01
        
        # カーソル移動
        if event.type in {'LEFT_ARROW'} and event.value == 'PRESS':
            move_vertex_to_view(context, -move_amt,  0.0)
        elif event.type in {'RIGHT_ARROW'} and event.value == 'PRESS':
            move_vertex_to_view(context, +move_amt,  0.0)
        elif event.type in {'UP_ARROW'} and event.value == 'PRESS':
            move_vertex_to_view(context,  0.0, +move_amt)
        elif event.type in {'DOWN_ARROW'} and event.value == 'PRESS':
            move_vertex_to_view(context,  0.0, -move_amt)
        
        context.area.header_text_set(
            text="move amount: %.3f %s" % (bpy.context.scene.akm_move_amt, event.type))
        
        # 視点操作を許可
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'MOUSEMOVE'}:
            return {'PASS_THROUGH'}
        
        # テンキー操作を許可
        if event.type in {'NUMPAD_0', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3', 'NUMPAD_4', 
                          'NUMPAD_5', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 
                          'NUMPAD_PLUS', 'NUMPAD_MINUS', 'NUMPAD_ASTERIX', 
                          'NUMPAD_SLASH', 'NUMPAD_PERIOD'}:
            return {'PASS_THROUGH'}
        
        context.space_data.overlay.show_object_origins = False
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            if context.object.mode == 'EDIT' and context.object.type == 'MESH':
                if context.active_object:
                    self.save_verts(context)
                    self.save_view(context)
                    if bpy.context.scene.akm_hide_vert:
                        self.save_verts_disp(context)
                    if bpy.context.scene.akm_center:
                        self.center_cursor(context)
                    context.window_manager.modal_handler_add(self)
                    return {'RUNNING_MODAL'}
        
        return {'CANCELLED'}
    
    def save_view(self, context):
        
        # 現在の3Dビューの設定を保存
        space_data = context.space_data
        self.original_show_floor = space_data.overlay.show_floor
        self.original_show_axis_x = space_data.overlay.show_axis_x
        self.original_show_axis_y = space_data.overlay.show_axis_y
        self.original_show_cursor = space_data.overlay.show_cursor
        self.original_show_retopo = space_data.overlay.show_retopology
        self.original_show_origin = space_data.overlay.show_object_origins
        self.original_sharing_xray = space_data.shading.show_xray
        self.original_cursor_location = context.scene.cursor.location.copy()
        self.original_object_location = context.active_object.location.copy()
        
        # 床、座標軸、3Dカーソルを非表示に設定
        if bpy.context.scene.akm_hide_view:
            space_data.overlay.show_floor  = False
            space_data.overlay.show_axis_x = False
            space_data.overlay.show_axis_y = False
            space_data.overlay.show_cursor = False
        # リトポロジー表示切替
        if bpy.context.scene.akm_show_retopo:
            space_data.overlay.show_retopology = True
        # 透過表示切替
        if bpy.context.scene.akm_xray:
            space_data.shading.show_xray = True
        
    def restore_view(self, context):
        
        # 3Dビューの設定を元に戻す
        space_data = context.space_data
        space_data.overlay.show_floor  = self.original_show_floor
        space_data.overlay.show_axis_x = self.original_show_axis_x
        space_data.overlay.show_axis_y = self.original_show_axis_y
        space_data.overlay.show_cursor = self.original_show_cursor
        space_data.overlay.show_retopology = self.original_show_retopo
        space_data.overlay.show_object_origins = self.original_show_origin
        space_data.shading.show_xray = self.original_sharing_xray
        context.scene.cursor.location  = self.original_cursor_location
        context.active_object.location = self.original_object_location
    
    def save_verts_disp(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        self.unselected_verts = [v.index for v in context.active_object.data.vertices if not v.select and not v.hide]
        for v in self.unselected_verts:
            context.active_object.data.vertices[v].hide = True
        bpy.ops.object.mode_set(mode='EDIT')
    
    def restore_verts_disp(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        for v in self.unselected_verts:
            context.active_object.data.vertices[v].hide = False
        bpy.ops.object.mode_set(mode='EDIT')
    
    def save_verts(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        self.selected_verts = {}
        for v in context.active_object.data.vertices:
            if v.select:
                self.selected_verts[v.index] = v.co.copy()
        bpy.ops.object.mode_set(mode='EDIT')
    
    def restore_verts(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        for key in self.selected_verts.keys():
            context.active_object.data.vertices[key].co = self.selected_verts[key]
        bpy.ops.object.mode_set(mode='EDIT')
    
    def center_cursor(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        model_matrix = context.active_object.matrix_world
        if len(self.selected_verts) != 0:
            center = mathutils.Vector((0, 0, 0))
            for key in self.selected_verts.keys():
                center += self.selected_verts[key]
            center /= len(self.selected_verts)
            context.scene.cursor.location  = model_matrix @ center
        bpy.ops.object.mode_set(mode='EDIT')
    
def register():
    bpy.utils.register_class(AKM_OT_ArrowMove)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    km.keymap_items.new(AKM_OT_ArrowMove.bl_idname, 'LEFT_ARROW' , 'PRESS', ctrl=False, shift=False)
    km.keymap_items.new(AKM_OT_ArrowMove.bl_idname, 'RIGHT_ARROW', 'PRESS', ctrl=False, shift=False)
    km.keymap_items.new(AKM_OT_ArrowMove.bl_idname, 'UP_ARROW'   , 'PRESS', ctrl=False, shift=False)
    km.keymap_items.new(AKM_OT_ArrowMove.bl_idname, 'DOWN_ARROW' , 'PRESS', ctrl=False, shift=False)

def unregister():
    bpy.utils.unregister_class(AKM_OT_ArrowMove)


