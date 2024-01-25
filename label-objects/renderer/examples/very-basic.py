import trimesh
import pyrender

trimesh_scene = trimesh.load('./cafeteria.glb')
scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)
pyrender.Viewer(scene, use_raymond_lighting=True)