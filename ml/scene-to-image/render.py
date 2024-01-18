import trimesh
import pyrender
cafeteria: pyrender.Scene = trimesh.load('./cafeteria.glb')


# mesh = pyrender.Mesh.from_trimesh(cafeteria)
# scene = pyrender.Scene()
# scene.add(mesh)

# add camera to cafetaria


pyrender.Viewer(cafeteria, use_raymond_lighting=True)

# print(cafeteria)