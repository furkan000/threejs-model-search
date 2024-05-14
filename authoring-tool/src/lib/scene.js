import * as THREE from "three";

import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";

import { tree } from "./store.js";

export function run() {
  const renderer = new THREE.WebGLRenderer({ canvas: document.querySelector("canvas"), antialias: true });
  const loader = new GLTFLoader();

  // There's no reason to set the aspect here because we're going
  // to set it every frame anyway so we'll set it to 2 since 2
  // is the the aspect for the canvas default size (300w/150h = 2)
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

    // model
    const loader = new GLTFLoader().setPath("./models/");
    loader.load("cafeteria.glb", async function (gltf) {
      const model = gltf.scene;
      // wait until the model can be added to the scene without blocking due to shader compilation
      await renderer.compileAsync(model, camera, scene);
      scene.add(model);

      console.log(getSimplifiedJson(model));
      // objectTree = getSimplifiedJson(model);
      tree.set(getSimplifiedJson(model));

      render();
    });
  });

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener("change", render); // use if there is no animation loop
  controls.minDistance = 2;
  controls.maxDistance = 10;
  controls.target.set(0, 0, -0.2);
  controls.update();

  function resizeCanvasToDisplaySize() {
    const canvas = renderer.domElement;
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    if (canvas.width !== width || canvas.height !== height) {
      // you must pass false here or three.js sadly fights the browser
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();

      // set render target sizes here
    }
  }

  function render() {
    // time *= 0.0005; // seconds

    resizeCanvasToDisplaySize();

    // mesh.rotation.x = time * 0.5;
    // mesh.rotation.y = time * 1;

    renderer.render(scene, camera);
    // requestAnimationFrame(render);
  }

  requestAnimationFrame(render);

  function getSimplifiedJson(o) {
    // Return undefined if the object is null or its type is "Mesh"
    if (o == null || o.type == "Mesh") return undefined;

    let meshName = undefined;
    let children = undefined;

    // If the object has exactly one child of type "Mesh", assign its name to meshName
    if (o.children != null && o.children.length == 1 && o.children[0].type == "Mesh") {
      meshName = o.children[0].name;
    }

    // If the object has children, map them to their simplified JSON representations
    if (o.children != null && o.children.length > 0) {
      children = o.children.map((c) => getSimplifiedJson(c));
    }

    // Remove all null values from the children array
    if (children != null) {
      children = children.filter((c) => c != null);
    }

    // If children array is empty, set it to undefined
    if (children != null && children.length == 0) {
      children = undefined;
    }

    // Return the simplified JSON object with id, label, meshName, and children properties
    return {
      id: o.id, // Add the object id
      label: o.name,
      meshName: meshName,
      children: children,
    };
  }
}
