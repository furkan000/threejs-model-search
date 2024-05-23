import * as THREE from "three";

import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";

let camera, scene, renderer;

init();

function init() {
  const container = document.createElement("div");
  document.body.appendChild(container);

  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.25, 20);
  camera.position.set(0.25, 0.25, -0.5);

  scene = new THREE.Scene();

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  container.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener("change", render); // use if there is no animation loop
  controls.minDistance = 2;
  controls.maxDistance = 10;
  controls.target.set(0, 0, -0.2);
  controls.update();

  new RGBELoader().setPath("textures/").load("royal_esplanade_1k.hdr", function (texture) {
    texture.mapping = THREE.EquirectangularReflectionMapping;

    scene.background = texture;
    scene.environment = texture;

    render();

    // model

    const loader = new GLTFLoader().setPath("Engine/");
    loader.load("scene.gltf", function (gltf) {
      scene.add(gltf.scene);

      gltf.animations; // Array<THREE.AnimationClip>
      gltf.scene; // THREE.Group
      gltf.scenes; // Array<THREE.Group>
      gltf.cameras; // Array<THREE.Camera>
      gltf.asset; // Object

      // console.log("animations", gltf.animations);
      console.log("scene", gltf.scene);

      console.log(JSON.stringify(getSimplifiedJson(gltf.scene)));

      // console.log("scenes", gltf.scenes);
      // console.log("cameras", gltf.cameras);
      // console.log("asset", gltf.asset);

      render();
    });
  });

  window.addEventListener("resize", onWindowResize);
}

function getSimplifiedJson(o) {
  if (o == null || o.type == "Mesh") return undefined;

  let meshName = undefined;
  let children = undefined;

  if (o.children != null && o.children.length == 1 && o.children[0].type == "Mesh") {
    meshName = o.children[0].name;
  }

  if (o.children != null && o.children.length > 0) {
    children = o.children.map((c) => getSimplifiedJson(c));
  }

  // remove all null from children
  if (children != null) {
    children = children.filter((c) => c != null);
  }
  // if children is empty, set it to undefined
  if (children != null && children.length == 0) {
    children = undefined;
  }

  return {
    name: o.name,
    meshName: meshName,
    children: children,
  };
}

function findInJSON(jsonObject, searchString) {
  let results = [];

  function searchInObject(obj, search) {
    // Check if the object itself has name or meshName matching the search string
    if (("name" in obj && obj.name.includes(search)) || ("meshName" in obj && obj.meshName.includes(search))) {
      results.push(obj.name || obj.meshName);
    }
    // If the object has children, recursively search through them
    if ("children" in obj) {
      for (const child of obj.children) {
        searchInObject(child, search);
      }
    }
  }

  searchInObject(jsonObject, searchString);
  return results;
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize(window.innerWidth, window.innerHeight);

  render();
}

//

function render() {
  renderer.render(scene, camera);
}
