import os

import bpy


class SpawnNames:
    PROTOTYPE = 0
    INSTANCE = 1
    FILENAME = 2

    names = {
        "Enemy": ("PrototypeEnemySpawn", "EnemySpawn", "needle/needle.obj"),
        "Player": ("PrototypePlayerSpawn", "PlayerSpawn", "player/player.obj"),
    }


class MYADDON_OT_spawn_import_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_import_symbol"
    bl_label = "出現ポイントシンボルImport"
    bl_description = "出現ポイントのシンボルをImportします"

    def load_obj(self, type_name):
        if type_name not in SpawnNames.names:
            self.report({"ERROR"}, f"未対応のSpawnPointです: {type_name}")
            return {"CANCELLED"}

        prototype_name = SpawnNames.names[type_name][SpawnNames.PROTOTYPE]
        if bpy.data.objects.get(prototype_name) is not None:
            return {"CANCELLED"}

        addon_directory = os.path.dirname(__file__)
        relative_path = SpawnNames.names[type_name][SpawnNames.FILENAME]
        full_path = os.path.join(addon_directory, relative_path)

        if not os.path.exists(full_path):
            self.report({"ERROR"}, f"モデルファイルが見つかりません: {full_path}")
            return {"CANCELLED"}

        bpy.ops.object.select_all(action="DESELECT")
        bpy.ops.wm.obj_import(
            "EXEC_DEFAULT",
            filepath=full_path,
            display_type="THUMBNAIL",
            forward_axis="Z",
            up_axis="Y",
        )
        bpy.ops.object.transform_apply(
            location=False,
            rotation=True,
            scale=False,
            properties=False,
            isolate_users=False,
        )

        imported_objects = list(bpy.context.selected_objects)
        if len(imported_objects) == 0:
            self.report({"ERROR"}, f"インポートに失敗しました: {full_path}")
            return {"CANCELLED"}

        for index, object in enumerate(imported_objects):
            object.name = prototype_name if index == 0 else f"{prototype_name}_{index}"
            object["type"] = SpawnNames.names[type_name][SpawnNames.INSTANCE]
            bpy.context.collection.objects.unlink(object)

        return {"FINISHED"}

    def execute(self, context):
        self.load_obj("Enemy")
        self.load_obj("Player")
        return {"FINISHED"}


class MYADDON_OT_spawn_create_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_symbol"
    bl_label = "出現ポイントシンボルの作成"
    bl_description = "出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    type: bpy.props.StringProperty(name="Type", default="Player")

    def execute(self, context):
        if self.type not in SpawnNames.names:
            self.report({"ERROR"}, f"未対応のSpawnPointです: {self.type}")
            return {"CANCELLED"}

        prototype_name = SpawnNames.names[self.type][SpawnNames.PROTOTYPE]
        spawn_object = bpy.data.objects.get(prototype_name)

        if spawn_object is None:
            bpy.ops.myaddon.myaddon_ot_spawn_import_symbol("EXEC_DEFAULT")
            spawn_object = bpy.data.objects.get(prototype_name)

        if spawn_object is None:
            self.report({"ERROR"}, f"SpawnPointシンボルを読み込めませんでした: {self.type}")
            return {"CANCELLED"}

        bpy.ops.object.select_all(action="DESELECT")

        object = spawn_object.copy()
        if spawn_object.data is not None:
            object.data = spawn_object.data.copy()

        bpy.context.collection.objects.link(object)
        object.name = SpawnNames.names[self.type][SpawnNames.INSTANCE]
        object["type"] = SpawnNames.names[self.type][SpawnNames.INSTANCE]

        object.select_set(True)
        bpy.context.view_layer.objects.active = object

        return {"FINISHED"}


class MYADDON_OT_spawn_create_player_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_player_symbol"
    bl_label = "プレイヤー出現ポイントシンボルの作成"
    bl_description = "プレイヤー出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol("EXEC_DEFAULT", type="Player")
        return {"FINISHED"}


class MYADDON_OT_spawn_create_enemy_symbol(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_spawn_create_enemy_symbol"
    bl_label = "敵出現ポイントシンボルの作成"
    bl_description = "敵出現ポイントのシンボルを作成します"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.myaddon.myaddon_ot_spawn_create_symbol("EXEC_DEFAULT", type="Enemy")
        return {"FINISHED"}
