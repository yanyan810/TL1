import bpy
import os


class MYADDON_OT_export_objects_as_obj(bpy.types.Operator):
    """シーン内の各MESHオブジェクトをFileNameプロパティに従い個別OBJとして書き出す"""
    bl_idname  = "myaddon.export_objects_as_obj"
    bl_label   = "オブジェクトを個別OBJで保存"
    bl_description = (
        "各MESHオブジェクトの FileName カスタムプロパティを元に\n"
        "resources/<name>/<name>.obj として個別書き出しします"
    )

    # ---- ファイルブラウザで保存先ディレクトリを選ばせる ----
    directory: bpy.props.StringProperty(
        name="保存先ディレクトリ",
        description="resources フォルダを選んでください",
        subtype="DIR_PATH",
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        base_dir = bpy.path.abspath(self.directory)
        if not base_dir:
            self.report({"ERROR"}, "保存先ディレクトリが設定されていません")
            return {"CANCELLED"}

        exported = 0
        skipped  = 0

        # 現在の選択状態を退避
        original_selection = list(context.selected_objects)
        original_active    = context.view_layer.objects.active

        # 全オブジェクトを走査
        for obj in context.scene.objects:

            # MESHタイプ以外はスキップ
            if obj.type != "MESH":
                skipped += 1
                continue

            # ---- FileName を決定 ----
            # カスタムプロパティ "file_name" があればそれを使う
            # なければオブジェクト名をそのまま使う
            if "file_name" in obj and obj["file_name"]:
                raw_name = str(obj["file_name"])
            else:
                raw_name = obj.name

            # "folder/model.obj" の形式ならそのまま、
            # それ以外なら "<name>/<name>" に正規化
            if "/" in raw_name or "\\" in raw_name:
                # 指定パスをそのまま使う
                rel_path = raw_name if raw_name.endswith(".obj") else raw_name + ".obj"
            else:
                # 拡張子を除いたベース名だけを使う
                base_name = os.path.splitext(raw_name)[0]
                rel_path  = f"{base_name}/{base_name}.obj"

            # 絶対パスに変換
            abs_path = os.path.join(base_dir, rel_path.replace("/", os.sep))

            # ディレクトリを作成
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)

            # ---- 対象オブジェクトだけを選択 ----
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # ---- OBJ エクスポート ----
            bpy.ops.wm.obj_export(
                filepath         = abs_path,
                export_selected_objects = True,   # 選択オブジェクトのみ
                export_uv        = True,
                export_normals   = True,
                export_materials = True,           # .mtl も一緒に出力
                export_triangulated_mesh = True,   # 三角ポリゴンに変換
                apply_modifiers  = True,
            )

            self.report({"INFO"}, f"保存: {abs_path}")
            print(f"[ExportOBJ] {obj.name} → {abs_path}")
            exported += 1

        # 元の選択状態に戻す
        bpy.ops.object.select_all(action="DESELECT")
        for obj in original_selection:
            obj.select_set(True)
        context.view_layer.objects.active = original_active

        self.report(
            {"INFO"},
            f"完了: {exported} 個出力 / {skipped} 個スキップ"
        )
        return {"FINISHED"}


class OBJECT_PT_export_obj(bpy.types.Panel):
    """個別OBJ書き出しパネル"""
    bl_label       = "OBJ個別書き出し"
    bl_idname      = "OBJECT_PT_export_obj"
    bl_space_type  = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context     = "object"
    bl_options     = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="各オブジェクトをFileNameに従いOBJ保存", icon="EXPORT")
        layout.operator(
            MYADDON_OT_export_objects_as_obj.bl_idname,
            text="全オブジェクトを個別OBJ保存",
            icon="FILE_TICK",
        )
