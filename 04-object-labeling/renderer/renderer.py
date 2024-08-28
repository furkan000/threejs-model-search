import trimesh
import pyrender
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


def create_raymond_lights(mesh_bbox_center, mesh_bbox_extents):
    thetas = np.pi * np.array([1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0])
    phis = np.pi * np.array([0.0, 1.0 / 3.0, 2.0 / 3.0, 3.0 / 3.0, 4.0 / 3.0, 5.0 / 3.0])
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

        # Position the light closer to the mesh
        light_position = mesh_bbox_center + z * (np.max(mesh_bbox_extents) * 2.5)
        matrix[:3, 3] = light_position
        nodes.append(
            pyrender.Node(
                light=pyrender.DirectionalLight(color=np.ones(3), intensity=4.0),
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
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

def look_at(camera_position, target_position):
    cam_pos = np.array(camera_position)
    target_pos = np.array(target_position)
    forward_vector = target_pos - cam_pos
    forward_vector /= np.linalg.norm(forward_vector)
    up_vector = np.array([0, 1, 0])
    right_vector = np.cross(up_vector, forward_vector)
    right_vector /= np.linalg.norm(right_vector)
    up_vector = np.cross(forward_vector, right_vector)
    rotation_matrix = np.array([right_vector, up_vector, -forward_vector])
    rotation_matrix = np.transpose(rotation_matrix)
    camera_pose = np.eye(4)
    camera_pose[:3, :3] = rotation_matrix
    camera_pose[:3, 3] = cam_pos
    return camera_pose

def focus_camera_on_mesh(scene, mesh_node, distance=2):
    mesh = mesh_node.mesh
    if mesh is None or len(mesh.primitives) == 0:
        raise ValueError("Mesh node has no primitives.")

    vertices = mesh.primitives[0].positions
    bbox_min = np.min(vertices, axis=0)
    bbox_max = np.max(vertices, axis=0)
    bbox_center = (bbox_max + bbox_min) / 2
    bbox_extents = bbox_max - bbox_min
    scale = max(bbox_extents)
    camera_distance = scale * distance
    angle = np.radians(45)

    camera_poses = []
    for i in range(4):
        x_offset = camera_distance * np.cos(angle + np.pi / 2 * i)
        z_offset = camera_distance * np.sin(angle + np.pi / 2 * i)
        y_offset = camera_distance * 0.5
        camera_position = [
            bbox_center[0] + x_offset,
            bbox_center[1] + y_offset,
            bbox_center[2] + z_offset,
        ]
        camera_pose = look_at(camera_position, bbox_center)
        camera_poses.append(camera_pose)

    return camera_poses, bbox_center, bbox_extents

def render_meshes_from_scene(glb_path, output_dir, yfov=np.pi / 10.0, aspect_ratio=1.0):
    trimesh_scene = trimesh.load(glb_path)
    scene = pyrender.Scene(ambient_light=[400., 400., 400.]).from_trimesh_scene(trimesh_scene)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mesh_index = 0
    camera = pyrender.PerspectiveCamera(yfov=yfov, aspectRatio=aspect_ratio)
    scene.add(camera)
    

    for node in scene.get_nodes():
        if isinstance(node, pyrender.Node) and node.mesh is not None:
            for other_node in scene.get_nodes():
                if other_node.mesh is not None and other_node != node:
                    other_node.mesh.is_visible = False

            node.mesh.is_visible = True

            # Calculate camera poses and light positions
            camera_poses, bbox_center, bbox_extents = focus_camera_on_mesh(scene, node, 2)
            raymond_lights = create_raymond_lights(bbox_center, bbox_extents)

            for light_node in raymond_lights:
                scene.add_node(light_node)

            pose_index = 0
            for pose in camera_poses:
                scene.set_pose(scene.main_camera_node, pose)
                render_to_image(
                    scene, filename=f"{output_dir}/rendered_mesh_{mesh_index}_{pose_index}.png"
                )
                pose_index += 1

            for light_node in raymond_lights:
                scene.remove_node(light_node)

            mesh_index += 1

# Usage
render_meshes_from_scene("./modern_interior_pack.glb", "./render_interior")
