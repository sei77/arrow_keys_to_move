
bl_info = {
    "name"    : "Arrow Keys to move",
    "author"  : "sei77",
    "version" : (1, 0, 0),
    "blender" : (4, 0, 0),
    "category": "3D View"
}

import bpy
from . import akm_property
from . import akm_panel
from . import akm_ot_trans_move
from . import akm_dict

def register():
    akm_property.init_props()
    akm_panel.register()
    akm_ot_trans_move.register()
    bpy.app.translations.register(__name__, akm_dict.translation_dict)

def unregister():
    akm_ot_trans_move.unregister()
    akm_panel.unregister()
    akm_property.clear_props()
    bpy.app.translations.unregister(__name__)

if __name__ == "__main__":
    register()

