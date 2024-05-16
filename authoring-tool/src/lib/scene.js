import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutlinePass } from "three/addons/postprocessing/OutlinePass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { FXAAShader } from "three/addons/shaders/FXAAShader.js";
import { tree } from "./store.js";

let externalFunction;
export function importExternalFunction(fn) {
  externalFunction = fn;
}

export let model;
let renderer, camera, scene, controls;
let composer, effectFXAA, outlinePass;
let canvas;

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let highlightedObject = null;
let isMouseDown = false;
let initialMouseDownPosition = new THREE.Vector2();

export function run() {
  initRenderer();
  initCamera();
  initScene();
  initLight();
  loadEnvironment();
  initPostProcessing();
  initControls();

  window.addEventListener("resize", onWindowResize, false);
  canvas.addEventListener("mousemove", onMouseMove, false);

  // Add event listeners for differentiating between click and drag
  canvas.addEventListener("mousedown", onMouseDown, false);
  canvas.addEventListener("mouseup", onMouseUp, false);
  canvas.addEventListener("mousemove", onMouseMove, false);
  canvas.addEventListener("dblclick", onMouseDblClick, false); // Add double-click event listener

  animate();
}

function initRenderer() {
  canvas = document.querySelector("canvas");
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
}

function initCamera() {
  camera = new THREE.PerspectiveCamera(50, 1, 1, 500);
  camera.position.z = 400;
}

function initScene() {
  scene = new THREE.Scene();
}

function initLight() {
  const light1 = new THREE.PointLight(0xff80c0, 2, 0);
  light1.position.set(200, 100, 300);
  scene.add(light1);
}

function loadEnvironment() {
  new RGBELoader().setPath("./textures/").load("autumn_field_puresky_4k.hdr", function (texture) {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.background = texture;
    scene.environment = texture;
    render();

    loadModel();
  });
}

function loadModel() {
  const loader = new GLTFLoader().setPath("./models/");
  loader.load("cafeteria.glb", async function (gltf) {
    model = gltf.scene;
    await renderer.compileAsync(model, camera, scene);
    scene.add(model);
    updateTreeObject();
    render();
  });
}

function initControls() {
  controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener("change", render);
  controls.minDistance = 2;
  controls.maxDistance = 20;
  controls.target.set(0, 0, -0.2);
  controls.update();
}

function initPostProcessing() {
  composer = new EffectComposer(renderer);

  const renderPass = new RenderPass(scene, camera);
  composer.addPass(renderPass);

  outlinePass = new OutlinePass(new THREE.Vector2(canvas.clientWidth, canvas.clientHeight), scene, camera);
  composer.setSize(canvas.clientWidth, canvas.clientHeight);

  // Make the highlighting effect more extreme
  outlinePass.edgeStrength = 10.0; // Default is 3.0
  outlinePass.edgeGlow = 1.0; // Default is 0.0
  outlinePass.edgeThickness = 3.0; // Default is 1.0
  outlinePass.pulsePeriod = 0; // Default is 0

  composer.addPass(outlinePass);

  const outputPass = new OutputPass();
  composer.addPass(outputPass);

  effectFXAA = new ShaderPass(FXAAShader);
  effectFXAA.uniforms["resolution"].value.set(1 / canvas.clientWidth, 1 / canvas.clientHeight);
  composer.addPass(effectFXAA);
}

export function resizeCanvasToDisplaySize() {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  if (canvas.width !== width || canvas.height !== height) {
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }
}

function onWindowResize() {
  resizeCanvasToDisplaySize();
  composer.setSize(canvas.clientWidth, canvas.clientHeight);
  effectFXAA.uniforms["resolution"].value.set(1 / canvas.clientWidth, 1 / canvas.clientHeight);
  render();
}

function render() {
  composer.render(scene, camera);
}

function animate() {
  requestAnimationFrame(animate);
  render();
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
  outlinePass.selectedObjects = [];

  if (object) {
    outlinePass.selectedObjects = [object];
    console.log(`Object with ID ${id} found and highlighted`);
    moveCameraToObject(object); // Move camera to the selected object
    render(); // Call render to update the scene immediately
  } else {
    console.log(`Object with ID ${id} not found`);
  }
}

function moveCameraToObject(object) {
  const box = new THREE.Box3().setFromObject(object);
  const center = new THREE.Vector3();
  box.getCenter(center);

  controls.target.copy(center);
  controls.update();

  const size = box.getSize(new THREE.Vector3());
  const maxDim = Math.max(size.x, size.y, size.z);

  // Desired percentage of the screen that the object should take up (e.g., 50%)
  const desiredObjectSize = 0.5;
  const fov = camera.fov * (Math.PI / 180);

  // Distance calculation to fit the object within the desired percentage of the screen
  const cameraZ = Math.abs(maxDim / (2 * Math.tan(fov / 2) * desiredObjectSize));

  // Adjust the camera position to zoom in or out based on object size
  const direction = new THREE.Vector3().subVectors(camera.position, controls.target).normalize();
  camera.position.copy(center).add(direction.multiplyScalar(cameraZ));

  camera.lookAt(center);
  controls.update();
}

export function findObjectById(object, id) {
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

function onMouseDown(event) {
  isMouseDown = true;
  initialMouseDownPosition.set(event.clientX, event.clientY);
}

function onMouseUp(event) {
  if (isMouseDown) {
    const finalMouseUpPosition = new THREE.Vector2(event.clientX, event.clientY);
    const moveDistance = initialMouseDownPosition.distanceTo(finalMouseUpPosition);

    // Define a threshold for detecting a drag versus a click
    const clickThreshold = 5; // Adjust as needed

    if (moveDistance < clickThreshold && highlightedObject) {
      moveCameraToObject(highlightedObject);
      render(); // Call render to update the scene immediately
    }
  }
  isMouseDown = false;
}

function onMouseMove(event) {
  // Convert mouse position to normalized device coordinates
  const rect = canvas.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  // Perform raycasting
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);

  if (intersects.length > 0) {
    const object = intersects[0].object;

    if (highlightedObject !== object) {
      highlightedObject = object;
      outlinePass.selectedObjects = [highlightedObject];
      render(); // Call render to update the scene immediately
    }
  } else {
    highlightedObject = null;
    outlinePass.selectedObjects = [];
    render(); // Call render to update the scene immediately
  }
}

function onMouseDblClick(event) {
  if (highlightedObject) {
    executeDoubleClickFunction(highlightedObject);
  }
}

function executeDoubleClickFunction(object) {
  // Define the function to be executed on double-click
  externalFunction(object.id);
  // Add any additional functionality here
}
