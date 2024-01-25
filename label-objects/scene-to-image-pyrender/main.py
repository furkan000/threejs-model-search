import trimesh
import pyrender
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def create_raymond_lights():
    thetas = np.pi * np.array([1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0])
    phis = np.pi * np.array([0.0, 2.0 / 3.0, 4.0 / 3.0])

    nodes = []
    for phi, theta in zip(phis, thetas):
        xp = np.sin(theta) * np.cos(phi)
        yp = np.sin(theta) * np.sin(phi)
        zp = np.cos(theta)

        z = np.array([xp, yp, zp])
        z = z / np.linalg.norm(z)
        x = np.array([-z[1], z[0], 0.0])
        if np.linalg.norm(x) == 0:
            x = np.array([1.0, 0.0, 0.0])
        x = x / np.linalg.norm(x)
        y = np.cross(z, x)

        matrix = np.eye(4)
        matrix[:3, :3] = np.c_[x, y, z]
        nodes.append(pyrender.Node(
            light=pyrender.DirectionalLight(color=np.ones(3), intensity=1.0),
            matrix=matrix
        ))

    return nodes

def render_to_image(scene, filename='rendered_image.png', camera_pose=None):
    color, depth = pyrender.OffscreenRenderer(400, 400).render(scene)
    fig = plt.figure()
    plt.axis('off')
    plt.imshow(color)
    plt.savefig(filename)
    plt.close(fig)

# Function to move camera to focus on a single mesh
def focus_camera_on_mesh(scene, mesh_node, distance=2):
    # Compute the mesh's bounding box from its vertices
    mesh = mesh_node.mesh
    if mesh is None or len(mesh.primitives) == 0:
        raise ValueError("Mesh node has no primitives.")

    # Get vertices of the first primitive (assuming one primitive per mesh)
    vertices = mesh.primitives[0].positions

    # Calculate the centroid and extents of the bounding box
    bbox_min = np.min(vertices, axis=0)
    bbox_max = np.max(vertices, axis=0)
    bbox_center = (bbox_max + bbox_min) / 2
    bbox_extents = bbox_max - bbox_min

    # Compute the new camera position
    # Adjust the distance based on the size of the bounding box
    scale = max(bbox_extents)
    camera_distance = scale * distance

    # Camera pointing towards the mesh, positioned along the z-axis
    camera_pose = np.array([
        [1, 0, 0, bbox_center[0]],
        [0, 1, 0, bbox_center[1]],
        [0, 0, 1, bbox_center[2] + camera_distance],
        [0, 0, 0, 1]
    ])
    # print(camera_pose)
    return camera_pose


# Load scene
trimesh_scene = trimesh.load('./Box.glb')
scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

# Add Raymond lights to the scene
raymond_lights = create_raymond_lights()
for light_node in raymond_lights:
    scene.add_node(light_node)


# Delete directory if it already exists
# if os.path.exists('./render'):
#     os.system('rm -rf ./render')

# Create a new directory for the rendered images
if not os.path.exists('./render'):
    os.makedirs('./render')

# Initialize an index for naming files
mesh_index = 0


# Create a single camera instance outside the loop
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
scene.add(camera)



# Iterate over each mesh node in the scene and render it
for node in scene.get_nodes():
    if isinstance(node, pyrender.Node) and node.mesh is not None:
        print(node)
        # Disable all other mesh nodes
        for other_node in scene.get_nodes():
            if other_node.mesh is not None and other_node != node:
                # other_node.mesh.is_visible = False
                pass

        # for other_node in scene.get_nodes():
        #     if other_node.mesh is not None and other_node != node:
        #         other_node.mesh.is_visible = True
                

        # Focus camera on the current mesh
        camera_pose = focus_camera_on_mesh(scene, node, 2)
        scene.set_pose(scene.main_camera_node, camera_pose)

        # Render the scene with the current mesh
        render_to_image(scene, filename=f'./render/rendered_mesh_{mesh_index}.png')

        # Increment the  index for the next mesh
        mesh_index += 1