
bl_info = {
    "name": "Bukowski Dealership Scene Setup",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os

class OBJECT_OT_setup_bukowski_scene(bpy.types.Operator):
    bl_idname = "object.setup_bukowski_scene"
    bl_label = "Setup Bukowski Scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Paths
        base_path = bpy.path.abspath("//")
        tex_path = os.path.join(base_path, "textures")

        # Create ground plane
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
        ground = bpy.context.active_object
        ground.name = "Ground"
        self.apply_material(ground, tex_path, "albedo.png", "roughness.png", "normal.png")

        # Create wall
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, -10, 5), rotation=(1.5708, 0, 0))
        wall = bpy.context.active_object
        wall.name = "Wall"
        self.apply_material(wall, tex_path, "albedo.png", "roughness.png", "normal.png")

        # Create inflatable tube man base
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.5, depth=6, location=(0, 2, 3))
        tube = bpy.context.active_object
        tube.name = "Inflatable_Bukowski"
        self.apply_material(tube, tex_path, "albedo.png", "roughness.png", "normal.png")

        return {'FINISHED'}

    def apply_material(self, obj, tex_path, color_file, rough_file, normal_file):
        mat = bpy.data.materials.new(name=obj.name + "_Material")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image.image = bpy.data.images.load(os.path.join(tex_path, color_file))
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

        roughness_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        roughness_image.image = bpy.data.images.load(os.path.join(tex_path, rough_file))
        roughness_image.image.colorspace_settings.name = 'Non-Color'
        mat.node_tree.links.new(bsdf.inputs['Roughness'], roughness_image.outputs['Color'])

        normal_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        normal_image.image = bpy.data.images.load(os.path.join(tex_path, normal_file))
        normal_image.image.colorspace_settings.name = 'Non-Color'

        normal_map = mat.node_tree.nodes.new('ShaderNodeNormalMap')
        mat.node_tree.links.new(normal_map.inputs['Color'], normal_image.outputs['Color'])
        mat.node_tree.links.new(bsdf.inputs['Normal'], normal_map.outputs['Normal'])

        obj.data.materials.append(mat)

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_setup_bukowski_scene.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_setup_bukowski_scene)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_setup_bukowski_scene)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
