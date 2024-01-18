from pygltflib import GLTF2, Node, Scene, Mesh

gltf = GLTF2().load("/home/furkan/Masterarbeit/threejs-model-search/ml/scene-to-image/cafeteria.glb")

scene: int = gltf.scene
scenes: list[Scene] = gltf.scenes
nodes: list[Node] = gltf.nodes
meshes: list[Mesh] = gltf.meshes

root_children_indices: list[int] = scenes[scene].nodes
root_children: list[Node] = [nodes[i] for i in root_children_indices]

a = root_children[0]
b = a.children