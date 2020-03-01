import bpy
import os
import sys

'''
Simplifies mesh to target number of faces
Requires Blender 2.8
Author: Rana Hanocka

@input: 
    <obj_file>
    <target_faces> number of target faces
    <outfile> name of simplified .obj file

@output:
    simplified mesh .obj
    to run it from cmd line:
    /opt/blender/blender --background --python blender_process.py /home/rana/koala.obj 1000 /home/rana/koala_1000.obj
'''


class Process:
    def __init__(self, obj_file, target_faces, export_name):
        assert (bpy.context.selected_objects != []), 'ERROR: no file present in blender context'
        mesh = self.load_obj(obj_file)
        self.hadDouble_vertices = False
        #self.clean_doubles(mesh)
        self.simplify(mesh, target_faces)
        self.export_obj(mesh, export_name)

    def load_obj(self, obj_file):
        bpy.ops.import_scene.obj(filepath=obj_file, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl",
                                 use_edges=True,
                                 use_smooth_groups=True, use_split_objects=False, use_split_groups=False,
                                 use_groups_as_vgroups=False, use_image_search=True, split_mode='ON')
        ob = bpy.context.selected_objects[0]
        assert (ob.type == 'MESH'), 'ERROR: object type does not match MESH type'
        return ob

    def subsurf(self, mesh):
        # subdivide mesh
        bpy.context.view_layer.objects.active = mesh
        mod = mesh.modifiers.new(name='Subsurf', type='SUBSURF')
        mod.subdivision_type = 'SIMPLE'
        bpy.ops.object.modifier_apply(modifier=mod.name)
        # now triangulate
        mod = mesh.modifiers.new(name='Triangluate', type='TRIANGULATE')
        bpy.ops.object.modifier_apply(modifier=mod.name)

    def simplify(self, mesh, target_faces):
        bpy.context.view_layer.objects.active = mesh
        mod = mesh.modifiers.new(name='Decimate', type='DECIMATE')
        bpy.context.object.modifiers['Decimate'].use_collapse_triangulate = True
        # upsample mesh if too low poly
        nfaces = len(mesh.data.polygons)
        while nfaces < target_faces:
            self.subsurf(mesh)
            nfaces = len(mesh.data.polygons)
        ratio = target_faces / float(nfaces)
        mod.ratio = float('%s' % ('%.6g' % (ratio)))
        print('faces: ', mod.face_count, mod.ratio)
        bpy.ops.object.modifier_apply(modifier=mod.name)

    def clean_doubles(self, mesh):
        vertexCount_before = len(mesh.vertices)
        bpy.context.scene.objects.active = mesh
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.gpencil.stroke_merge_by_distance(threshold=0.001)
        bpy.ops.object.editmode_toggle()

        vertexCount_after = len(mesh.vertices)
        if vertexCount_after < vertexCount_before:
            print('Remove double vertices for: %s' % mesh.name)
            self.hadDouble_vertices = True

    def repair_zeroArea_faces(self, mesh):
        pass

    def export_obj(self, mesh, export_name):
        outpath = os.path.dirname(export_name)
        if not os.path.isdir(outpath): os.makedirs(outpath)
        print('EXPORTING', export_name)
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select_set(state=True)
        bpy.ops.export_scene.obj(filepath=export_name, check_existing=False, filter_glob="*.obj;*.mtl",
                                 use_selection=True, use_animation=False, use_mesh_modifiers=True, use_edges=True,
                                 use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=True,
                                 use_uvs=False, use_materials=False, use_triangles=True, use_nurbs=False,
                                 use_vertex_groups=False, use_blen_objects=True, group_by_object=False,
                                 group_by_material=False, keep_vertex_order=True, global_scale=1, path_mode='AUTO',
                                 axis_forward='-Z', axis_up='Y')


"""
obj_file = sys.argv[-3]
target_faces = int(sys.argv[-2])
export_name = sys.argv[-1]


print('args: ', obj_file, target_faces, export_name)
blender = Process(obj_file, target_faces, export_name)
"""
