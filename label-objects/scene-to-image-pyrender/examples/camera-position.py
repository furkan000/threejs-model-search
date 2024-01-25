import trimesh
import pyrender
import numpy as np

trimesh_scene = trimesh.load('./Box.glb')
scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.414)
camera_pose = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
])
scene.add(camera, pose=camera_pose)

pyrender.Viewer(scene, use_raymond_lighting=True)