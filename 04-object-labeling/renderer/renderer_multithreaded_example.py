import trimesh
import pyrender
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import numpy as np
import concurrent.futures
import ctypes
# Assuming you're on a Unix-like system
x11 = ctypes.cdll.LoadLibrary('libX11.so')
x11.XInitThreads()
import multiprocessing
from multiprocessing import Pool

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
        nodes.append(
            pyrender.Node(
                light=pyrender.DirectionalLight(color=np.ones(3), intensity=1.0),
                matrix=matrix,
            )
        )

    return nodes

def render_to_image(scene, filename="rendered_image.png", camera_pose=None):
    color, depth = pyrender.OffscreenRenderer(400, 400).render(scene)
    fig = plt.figure()
    plt.axis("off")
    plt.imshow(color)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # Use bbox_inches and pad_inches to remove extra padding around the image
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

def look_at(camera_position, target_position):
    # Convert positions to numpy arrays for easier calculations
    cam_pos = np.array(camera_position)
    target_pos = np.array(target_position)

    # Calculate direction vector from camera to target (forward vector)
    forward_vector = target_pos - cam_pos
    forward_vector /= np.linalg.norm(forward_vector)

    # Assume up vector as Y-axis for simplicity
    up_vector = np.array([0, 1, 0])

    # Calculate right vector
    right_vector = np.cross(up_vector, forward_vector)
    right_vector /= np.linalg.norm(right_vector)

    # Recalculate the up vector
    up_vector = np.cross(forward_vector, right_vector)

    # Construct rotation matrix
    rotation_matrix = np.array(
        [right_vector, up_vector, -forward_vector]
    )  # note the negation of the forward vector
    rotation_matrix = np.transpose(rotation_matrix)  # transpose to align axes

    # Create camera pose matrix
    camera_pose = np.eye(4)
    camera_pose[:3, :3] = rotation_matrix
    camera_pose[:3, 3] = cam_pos

    return camera_pose

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

    # Compute the new camera positions
    scale = max(bbox_extents)
    camera_distance = scale * distance

    # Define the angle for the 3/4 view
    angle = np.radians(45)  # 45 degrees for a 3/4 view

    # Compute four camera poses
    camera_poses = []
    for i in range(4):
        # Rotate the camera around the Y axis (upward) and lift it up a bit
        x_offset = camera_distance * np.cos(angle + np.pi / 2 * i)
        z_offset = camera_distance * np.sin(angle + np.pi / 2 * i)
        y_offset = camera_distance * 0.5  # Adjust for a higher view

        # Calculate camera position
        camera_position = [
            bbox_center[0] + x_offset,
            bbox_center[1] + y_offset,
            bbox_center[2] + z_offset,
        ]

        # Use look_at function to orient the camera towards the mesh's center
        camera_pose = look_at(camera_position, bbox_center)
        camera_poses.append(camera_pose)

    return camera_poses

def render_meshes_from_scene(glb_path, output_dir, yfov=np.pi / 3.0, aspect_ratio=1.0, num_processes=None):
    # Load the scene to enumerate meshes
    trimesh_scene = trimesh.load(glb_path, process=False)
    scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert the set of nodes to a list to enable indexing
    node_list = list(scene.get_nodes())

    # Prepare a list of tasks for parallel execution
    tasks = []
    for index, node in enumerate(node_list):
        if isinstance(node, pyrender.Node) and node.mesh is not None:
            tasks.append((glb_path, output_dir, index, yfov, aspect_ratio))

    # Use multiprocessing to render meshes in parallel
    # num_processes can be specified; if None, it defaults to the number of CPU cores
    with Pool(processes=num_processes) as pool:
        pool.starmap(render_single_mesh, tasks)

# The render_single_mesh function also needs to be updated to use the index
def render_single_mesh(glb_path, output_dir, node_index, yfov, aspect_ratio):
    # Load the scene
    trimesh_scene = trimesh.load(glb_path, process=False)
    scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

    # Add Raymond lights to the scene
    raymond_lights = create_raymond_lights()
    for light_node in raymond_lights:
        scene.add_node(light_node)

    # Create a single camera instance
    camera = pyrender.PerspectiveCamera(yfov=yfov, aspectRatio=aspect_ratio)
    scene.add(camera)

    # Convert the set of nodes to a list to enable indexing
    node_list = list(scene.get_nodes())

    # Find and render the specific mesh
    node = node_list[node_index]
    if isinstance(node, pyrender.Node) and node.mesh is not None:
        # Focus camera on the current mesh
        camera_poses = focus_camera_on_mesh(scene, node, 2)

        pose_index = 0
        for pose in camera_poses:
            scene.set_pose(scene.main_camera_node, pose)
            # Render the scene with the current mesh
            render_to_image(
                scene, filename=f"{output_dir}/rendered_mesh_{node_index}_{pose_index}.png"
            )
            pose_index += 1
    print("Finished rendering mesh", node_index)        

# Usage
num_cores = 8  # for example, 8 processes
render_meshes_from_scene("./cafeteria.glb", "./render", num_processes=num_cores)
