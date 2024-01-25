import trimesh
import pyrender
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import numpy as np


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


# Load scene
trimesh_scene = trimesh.load("./cafeteria.glb")
scene = pyrender.Scene().from_trimesh_scene(trimesh_scene)

# Add Raymond lights to the scene
raymond_lights = create_raymond_lights()
for light_node in raymond_lights:
    scene.add_node(light_node)


# Delete directory if it already exists
# if os.path.exists('./render'):
#     os.system('rm -rf ./render')

# Create a new directory for the rendered images
if not os.path.exists("./render"):
    os.makedirs("./render")

# Initialize an index for naming files
mesh_index = 0


# Create a single camera instance outside the loop
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
scene.add(camera)
# add point light with camera as parent
# point_light = pyrender.PointLight(color=[1.0, 1.0, 1.0], intensity=1.0)
# scene.add(point_light, parent_node=scene.main_camera_node)


# Iterate over each mesh node in the scene and render it
for node in scene.get_nodes():
    if isinstance(node, pyrender.Node) and node.mesh is not None:
        print(mesh_index)
        # Disable all other mesh nodes
        for other_node in scene.get_nodes():
            if other_node.mesh is not None and other_node != node:
                other_node.mesh.is_visible = False
                pass

        node.mesh.is_visible = True

        # Focus camera on the current mesh
        camera_poses = focus_camera_on_mesh(scene, node, 2)

        pose_index = 0
        for pose in camera_poses:
            scene.set_pose(scene.main_camera_node, pose)
            # Render the scene with the current mesh
            render_to_image(
                scene, filename=f"./render/rendered_mesh_{mesh_index}_{pose_index}.png"
            )
            pose_index += 1

        # Increment the  index for the next mesh
        mesh_index += 1
