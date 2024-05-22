import { writable } from "svelte/store";
// import { label } from "three/examples/jsm/nodes/Nodes.js";

export const tree = writable({ label: "root", children: [] });
export const modelUrl = writable("./models/cafeteria.glb");
