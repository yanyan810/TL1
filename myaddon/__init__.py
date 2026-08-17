if "bpy" in locals():
    import importlib
    importlib.reload(myaddon_operator)
    importlib.reload(myaddon_export)
    from . import spawn
    importlib.reload(spawn)
    importlib.reload(myaddon_menu)
    importlib.reload(myaddon_draw)
    importlib.reload(disabled)
    importlib.reload(export_obj)
else:
    import bpy
    from . import myaddon_operator
    from . import myaddon_export
    from . import myaddon_menu
    from . import myaddon_draw
    from . import disabled
    from . import export_obj
    from . import spawn

bl_info = {
    "name": "レベルエディタ",
    "author": "Haruhi Miyazawa",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# Blenderに登録するクラスリスト
classes = (
    myaddon_operator.MYADDON_OT_create_ico_sphere,
    myaddon_operator.MYADDON_OT_stretch_vertex,
    myaddon_export.MYADDON_OT_export_scene,
    myaddon_menu.TOPBAR_MT_my_menu,
    myaddon_operator.MYADDON_OT_add_filename,
    myaddon_operator.OBJECT_PT_file_name,
    myaddon_operator.MYADDON_OT_add_collider,
    myaddon_operator.OBJECT_PT_collider,
    # 無効オプション追加オペレータ
    disabled.MYADDON_OT_add_disabled,
    # 無効オプションパネル
    disabled.OBJECT_PT_disabled,
    # SpawnPoint
    spawn.MYADDON_OT_spawn_import_symbol,
    spawn.MYADDON_OT_spawn_create_symbol,
    spawn.MYADDON_OT_spawn_create_player_symbol,
    spawn.MYADDON_OT_spawn_create_enemy_symbol,
    # 個別OBJ書き出し
    export_obj.MYADDON_OT_export_objects_as_obj,
    export_obj.OBJECT_PT_export_obj,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューに項目追加
    bpy.types.TOPBAR_MT_editor_menus.append(myaddon_menu.TOPBAR_MT_my_menu.submenu)
    #3Dビューに描画関数を追加
    myaddon_draw.DrawCollider.handle = bpy.types.SpaceView3D.draw_handler_add(myaddon_draw.DrawCollider.draw_collider, (), "WINDOW", "POST_VIEW")
    print("レベルエディタが有効化されました。")

def unregister():
    #メニューから削除
    bpy.types.TOPBAR_MT_editor_menus.remove(myaddon_menu.TOPBAR_MT_my_menu.submenu)
    #3Dビューから描画関数を削除
    bpy.types.SpaceView3D.draw_handler_remove(myaddon_draw.DrawCollider.handle, "WINDOW")
   
    #ブレンダーからクラス削除
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
   
    print("レベルエディタが無効化されました。")

if __name__ == "__main__":
    register()
