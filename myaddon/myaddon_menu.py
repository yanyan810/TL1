import bpy
from . import myaddon_operator
from . import myaddon_export
from . import spawn

#トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    #blenderがクラスを識別するための固有文字列
    bl_idname = "TOPBAR_MT_my_menu"

    #メニューのラベルとして表示される文字列
    bl_label = "MyMenu"
    #著者表示用の文字列
    bl_description = "拡張メニュー by Haruhi Miyazawa"

    #サブメニューの描画
    def draw(self, context):
        
        #トップバーの「エディターメニュー」に項目(オペレーター)を追加
        layout = self.layout
        layout.operator(myaddon_operator.MYADDON_OT_stretch_vertex.bl_idname,
                        text=myaddon_operator.MYADDON_OT_stretch_vertex.bl_label)
        
        layout.operator(myaddon_operator.MYADDON_OT_create_ico_sphere.bl_idname,
                        text=myaddon_operator.MYADDON_OT_create_ico_sphere.bl_label)

        layout.operator(myaddon_export.MYADDON_OT_export_scene.bl_idname,
                        text=myaddon_export.MYADDON_OT_export_scene.bl_label)

        layout.operator(myaddon_operator.MYADDON_OT_add_filename.bl_idname,
                text=myaddon_operator.MYADDON_OT_add_filename.bl_label)

        layout.operator(spawn.MYADDON_OT_spawn_create_player_symbol.bl_idname,
                        text=spawn.MYADDON_OT_spawn_create_player_symbol.bl_label)

        layout.operator(spawn.MYADDON_OT_spawn_create_enemy_symbol.bl_idname,
                        text=spawn.MYADDON_OT_spawn_create_enemy_symbol.bl_label)

    #既存メニューにサブメニューを追加
    def submenu(self, context):
        #トップバーの「エディターメニュー」にサブメニューを追加
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

#メニュー項目描画
def draw_menu_manual(self, context):
 #self : 呼び出し元のクラスインスタンス。
 #context : カーソルを合わせたときのポップアップのカスタマイズなどに使用

    #トップバーの「エディタメニュー」に項目(オペレーター)を追加
    self.layout.operator("wm.url_open_preset", text="Manual", icon="HELP")
