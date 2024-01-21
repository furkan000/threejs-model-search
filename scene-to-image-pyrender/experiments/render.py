import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt

def renderToImage(scene):
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
    s = np.sqrt(2)/2
    camera_pose = np.array([
    [0.0, -s,   s,   0.3],
    [1.0,  0.0, 0.0, 0.0],
    [0.0,  s,   s,   0.35],
    [0.0,  0.0, 0.0, 1.0],
    ])
    scene.add(camera, pose=camera_pose)
    # scene.ambient_light = np.array([0.2, 0.2, 0.2])
    

    color, depth = pyrender.OffscreenRenderer(400, 400).render(scene)
    # plt.figure()
    # plt.axis('off')
    # plt.imshow(color)
    # plt.show()
    



trimesh_scene: trimesh.scene.scene.Scene = trimesh.load('./cafeteria.glb')
scene: pyrender.scene.Scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

nodes = list(scene.nodes)

# for node in nodes[0:20]:
#     node.mesh.is_visible = False


# node: pyrender.node.Node = list(nodes)[0]
# node.mesh.is_visible = False


renderToImage(scene)
pyrender.Viewer(scene, use_raymond_lighting=True)
