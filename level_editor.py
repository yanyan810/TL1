import bpy

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

#オペレーターICO球生成
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_ico_sphere"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成します"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}

#メニュー実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました。")
        #オペレーターの命令処理を通知
        return {'FINISHED'}
    

#オペレーター 頂点を伸ばす
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばします"
    #リドゥ、アンドゥ可能オプション
    bl_options = {'REGISTER', 'UNDO'}

#メニュー実行したときに呼ばれるコールバック関数
    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました。")
        #オペレーターの命令処理を通知
        return {'FINISHED'}

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #blenderがクラスを識別するための固有文字列
    bl_idname = "TOPBAR_MT_my_menu"

    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by "+bl_info["author"]

    #サブメニューの描画
    def draw(self, context):
        
        #トップバーの「エディターメニュー」に項目(オペレーター)を追加
        layout = self.layout
        layout.operator(MYADDON_OT_stretch_vertex.bl_idname,
                        text=MYADDON_OT_stretch_vertex.bl_label)
        
        layout.operator(MYADDON_OT_create_ico_sphere.bl_idname,
                        text=MYADDON_OT_create_ico_sphere.bl_label)


    #既存メニューにサブメニューを追加
    def submenu(self, context):
        #トップバーの「エディターメニュー」にサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_stretch_vertex,
    TOPBAR_MT_my_menu,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #メニューに項目追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.submenu)
    print("レベルエディタが有効化されました。")

def unregister():
    #メニューから削除
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.submenu)
   
   #ブレンダーからクラス削除
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
   
    print("レベルエディタが無効化されました。")



#if __name__ == "__main__":
#    register()

#メニュー項目描画
def draw_menu_manual(self, context):
 #self : 呼び出し元のクラスインスタンス。
 #context : カーソルを合わせたときのポップアップのカスタマイズなどに使用

    #トップバーの「エディタメニュー」に項目(オペレーター)を追加
    self.layout.operator("wm.url_open_preset", text="Manual", icon="HELP")

