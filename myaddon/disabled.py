import bpy

# ===================================================
# オペレータ: 無効オプションを追加する
# ===================================================
class MYADDON_OT_add_disabled(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_add_disabled"
    bl_label = "無効オプション追加"
    bl_description = "無効フラグ(disabled)カスタムプロパティを追加します"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object is None:
            self.report({'WARNING'}, "オブジェクトが選択されていません")
            return {'CANCELLED'}

        # bool型のカスタムプロパティを追加
        # Falseで追加する（デフォルトは有効）
        context.object["disabled"] = False

        return {'FINISHED'}


# ===================================================
# パネル: 無効オプションパネル
# ===================================================
class OBJECT_PT_disabled(bpy.types.Panel):
    bl_idname = "OBJECT_PT_disabled"
    bl_label = "無効オプション"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        if context.object is None:
            return

        layout = self.layout

        if "disabled" in context.object:
            # カスタムプロパティがあればチェックボックスとして表示する
            layout.prop(context.object, '["disabled"]', text="無効 (ゲームに出さない)")
        else:
            # なければカスタムプロパティ追加用のボタン（オペレータ）を表示する
            layout.operator(MYADDON_OT_add_disabled.bl_idname)
