import * as THREE from "three";

import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";

import { tree } from "./store.js";

export let model;

export function run() {
  const renderer = new THREE.WebGLRenderer({ canvas: document.querySelector("canvas"), antialias: true });
  const loader = new GLTFLoader();

  const camera = new THREE.PerspectiveCamera(50, 1, 1, 2000);
  camera.position.z = 400;

  const scene = new THREE.Scene();

  const light1 = new THREE.PointLight(0xff80c0, 2, 0);
  light1.position.set(200, 100, 300);
  scene.add(light1);

  new RGBELoader().setPath("./textures/").load("autumn_field_puresky_4k.hdr", function (texture) {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = texture;
    scene.environment = texture;
    render();

    const loader = new GLTFLoader().setPath("./models/");
    loader.load("cafeteria.glb", async function (gltf) {
      model = gltf.scene;
      await renderer.compileAsync(model, camera, scene);
      scene.add(model);

      updateTreeObject();

      render();
    });
  });

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener("change", render);
  controls.minDistance = 2;
  controls.maxDistance = 10;
  controls.target.set(0, 0, -0.2);
  controls.update();

  function resizeCanvasToDisplaySize() {
    const canvas = renderer.domElement;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    if (canvas.width !== width || canvas.height !== height) {
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
    }
  }

  function render() {
    resizeCanvasToDisplaySize();
    renderer.render(scene, camera);
  }

  requestAnimationFrame(render);
}

export function updateTreeObject() {
  tree.set(getSimplifiedJson(model));
}

export function getSimplifiedJson(o) {
  if (o == null || o.type == "Mesh") return undefined;

  let meshName = undefined;
  let children = undefined;

  if (o.children != null && o.children.length == 1 && o.children[0].type == "Mesh") {
    meshName = o.children[0].name;
  }

  if (o.children != null && o.children.length > 0) {
    children = o.children.map((c) => getSimplifiedJson(c));
  }

  if (children != null) {
    children = children.filter((c) => c != null);
  }

  if (children != null && children.length == 0) {
    children = undefined;
  }

  return {
    id: o.id,
    label: o.name,
    meshName: meshName,
    children: children,
    ...(o.description ? { description: o.description } : {}),
  };
}

export function highlightObjectById(id) {
  const object = findObjectById(model, id);

  

  if (object) {
    console.log(`Object with ID ${id} found`);
    console.log(object);
  } else {
    console.log(`Object with ID ${id} not found`);
  }
}

export function findObjectById(object, id) {
  // console.log(object.id);
  if (object.id == id) {
    return object;
  }
  for (let i = 0; i < object.children.length; i++) {
    const result = findObjectById(object.children[i], id);
    if (result) {
      return result;
    }
  }
  return null;
}

export function renameObjectById(id, newLabel) {
  const object = findObjectById(model, id);

  if (object) {
    object.name = newLabel;
    console.log(`Object with ID ${id} renamed to ${newLabel}`);
    updateTreeObject();
  } else {
    console.log(`Object with ID ${id} not found`);
  }
}

export function helloWorld() {
  console.log(model);
  console.log("Hello, World!");
}
