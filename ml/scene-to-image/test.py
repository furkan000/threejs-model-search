import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt

def add_raymond_lights(scene, intensity=1.0):
    # Set up three directional lights (like in Raymond lighting)
    light1 = pyrender.DirectionalLight(color=np.ones(3), intensity=intensity)
    light2 = pyrender.DirectionalLight(color=np.ones(3), intensity=intensity)
    light3 = pyrender.DirectionalLight(color=np.ones(3), intensity=intensity)

    # Position the lights around the scene
    light1_pose = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, -10],
        [0, 0, 1, 10],
        [0, 0, 0, 1]
    ])
    light2_pose = np.array([
        [1, 0, 0, 10],
        [0, 1, 0, 0],
        [0, 0, 1, 10],
        [0, 0, 0, 1]
    ])
    light3_pose = np.array([
        [1, 0, 0, -10],
        [0, 1, 0, 0],
        [0, 0, 1, -10],
        [0, 0, 0, 1]
    ])

    scene.add(light1, pose=light1_pose)
    scene.add(light2, pose=light2_pose)
    scene.add(light3, pose=light3_pose)

def renderToImage(scene):
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
    s = np.sqrt(2)/2
    camera_pose = np.array([
        [0.0, -s, s, 0.3],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, s, s, 0.35],
        [0.0, 0.0, 0.0, 1.0],
    ])
    scene.add(camera, pose=camera_pose)
    color, depth = pyrender.OffscreenRenderer(400, 400).render(scene)
    plt.figure()
    plt.axis('off')
    plt.imshow(color)
    plt.show()

trimesh_scene: trimesh.scene.scene.Scene = trimesh.load('./cafeteria.glb')
scene: pyrender.scene.Scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

# Add Raymond lights to the scene
add_raymond_lights(scene, intensity=3.0)

nodes = list(scene.nodes)
renderToImage(scene)
