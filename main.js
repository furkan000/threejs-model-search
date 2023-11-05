import * as THREE from "three";

import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { GUI } from "three/addons/libs/lil-gui.module.min.js";

import Stats from "three/addons/libs/stats.module.js";

import { OBJLoader } from "three/addons/loaders/OBJLoader.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { ShaderPass } from "three/addons/postprocessing/ShaderPass.js";
import { OutlinePass } from "three/addons/postprocessing/OutlinePass.js";
// import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";

import { FXAAShader } from "three/addons/shaders/FXAAShader.js";

let container, stats;
let camera, scene, renderer, controls;
let composer, effectFXAA, outlinePass;
let model;

// Highlight & GUI

let selectedObjects = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

const obj3d = new THREE.Object3D();
const group = new THREE.Group();

const params = {
  edgeStrength: 10.0,
  edgeGlow: 1.0,
  edgeThickness: 4.0,
  pulsePeriod: 0,
  rotate: false,
  usePatternTexture: false,
  search: "",
};

// Init gui

const gui = new GUI({ width: 280 });

gui.add(params, "edgeStrength", 0.01, 10).onChange(function (value) {
  outlinePass.edgeStrength = Number(value);
});

gui.add(params, "edgeGlow", 0.0, 1).onChange(function (value) {
  outlinePass.edgeGlow = Number(value);
});

gui.add(params, "edgeThickness", 1, 4).onChange(function (value) {
  outlinePass.edgeThickness = Number(value);
});

gui.add(params, "pulsePeriod", 0.0, 5).onChange(function (value) {
  outlinePass.pulsePeriod = Number(value);
});

gui.add(params, "rotate");

gui.add(params, "usePatternTexture").onChange(function (value) {
  outlinePass.usePatternTexture = value;
});

gui.add(params, "search").onChange(findObject);

function Configuration() {
  this.visibleEdgeColor = "#ffffff";
  this.hiddenEdgeColor = "#ffffff";
  this.edgeStrength = 10.0;
  this.edgeGlow = 1.0;
  this.edgeThickness = 4.0;
  this.pulsePeriod = 0;
}

const conf = new Configuration();

gui.addColor(conf, "visibleEdgeColor").onChange(function (value) {
  outlinePass.visibleEdgeColor.set(value);
});

gui.addColor(conf, "hiddenEdgeColor").onChange(function (value) {
  outlinePass.hiddenEdgeColor.set(value);
});

init();
animate();

function init() {
  const container = document.createElement("div");
  document.body.appendChild(container);

  camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.25, 20);
  camera.position.set(-1.8, 0.6, 2.7);

  scene = new THREE.Scene();

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  container.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener("change", render); // use if there is no animation loop
  controls.minDistance = 0;
  controls.maxDistance = 1;
  controls.enablePan = false;
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.update();

  new RGBELoader().setPath("textures/").load("royal_esplanade_1k.hdr", function (texture) {
    texture.mapping = THREE.EquirectangularReflectionMapping;

    scene.background = texture;
    scene.environment = texture;

    render();

    // model

    const loader = new GLTFLoader().setPath("Engine/");
    loader.load("scene.gltf", async function (gltf) {
      model = gltf.scene;

      // wait until the model can be added to the scene without blocking due to shader compilation
      renderer.compile(model, camera, scene);

      scene.add(model);
      console.log(getSimplifiedJson(model));

      render();
    });
  });

  window.addEventListener("resize", onWindowResize);

  stats = new Stats();
  container.appendChild(stats.dom);

  // postprocessing

  composer = new EffectComposer(renderer);

  const renderPass = new RenderPass(scene, camera);
  composer.addPass(renderPass);

  outlinePass = new OutlinePass(new THREE.Vector2(window.innerWidth, window.innerHeight), scene, camera);
  composer.addPass(outlinePass);

  const textureLoader = new THREE.TextureLoader();
  textureLoader.load("textures/tri_pattern.jpg", function (texture) {
    outlinePass.patternTexture = texture;
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
  });

  const outputPass = new OutputPass();
  composer.addPass(outputPass);

  effectFXAA = new ShaderPass(FXAAShader);
  effectFXAA.uniforms["resolution"].value.set(1 / window.innerWidth, 1 / window.innerHeight);
  composer.addPass(effectFXAA);

  window.addEventListener("resize", onWindowResize);

  renderer.domElement.style.touchAction = "none";
  renderer.domElement.addEventListener("pointermove", onPointerMove);

  function onPointerMove(event) {
    if (event.isPrimary === false) return;

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    checkIntersection();
  }

  function addSelectedObject(object) {
    selectedObjects = [];
    selectedObjects.push(object);
  }

  function checkIntersection() {
    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObject(scene, true);

    if (intersects.length > 0) {
      const selectedObject = intersects[0].object;
      addSelectedObject(selectedObject);
      outlinePass.selectedObjects = selectedObjects;
    } else {
      // outlinePass.selectedObjects = [];
    }
  }
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

function animate() {
  requestAnimationFrame(animate);

  stats.begin();

  const timer = performance.now();

  if (params.rotate) {
    group.rotation.y = timer * 0.0001;
  }

  controls.update();

  composer.render();

  stats.end();
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

function findObject(searchString) {
  const searchStringLower = searchString.toLowerCase();
  selectedObjects = [];

  scene.traverse(function (object) {
    if (object.isMesh == true && object.name.toLowerCase().includes(searchStringLower)) {
      selectedObjects.push(object);
    }
  });
  if (selectedObjects.length > 0) {
    outlinePass.selectedObjects = selectedObjects;
  }
  // selectedObjects = searchResults;
  // animate();
  // return searchResults;
  console.log(selectedObjects);
}
