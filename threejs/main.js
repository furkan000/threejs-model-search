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
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { FXAAShader } from "three/addons/shaders/FXAAShader.js";

var l = function () {
  console.log.apply(console, arguments);
}


let container, stats;
let camera, scene, renderer, controls;
let composer, effectFXAA, outlinePass;
let model;
let mixer;

let clips;



let hideGui = false;



// Highlight & GUI

let selectedObjects = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

const obj3d = new THREE.Object3D();
const group = new THREE.Group();
const loader = new GLTFLoader();


const params = {
  edgeStrength: 10.0,
  edgeGlow: 0.245,
  edgeThickness: 1.0,
  pulsePeriod: 0,
  rotate: false,
  usePatternTexture: false,
  search: "",
  testFunction: testFunction
};


// wait one second
setTimeout(function () {
  outlinePass.edgeStrength = Number(params.edgeStrength);
  outlinePass.edgeGlow = Number(params.edgeGlow);
  outlinePass.edgeThickness = Number(params.edgeThickness);
  outlinePass.pulsePeriod = Number(params.pulsePeriod);
  outlinePass.visibleEdgeColor.set("#ffffff");
  outlinePass.hiddenEdgeColor.set("#190a05");
}, 1000);


// Init gui

const gui = new GUI({ width: 280 });

if (hideGui) {
  gui.hide();
}





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

gui.add(params, 'testFunction');

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



function loadGLTFModel(path) {
  loader.load(path, async function (gltf) {
    if (model != undefined) {
      scene.remove(model);
    }

    model = gltf.scene;
    // wait until the model can be added to the scene without blocking due to shader compilation
    renderer.compile(model, camera, scene);




    scene.add(model);
    mixer = new THREE.AnimationMixer(model);
    clips = gltf.animations;



    console.log(gltf.animations);
    // gltf.animations; // Array<THREE.AnimationClip>
    // gltf.scene; // THREE.Group
    // gltf.scenes; // Array<THREE.Group>
    // gltf.cameras; // Array<THREE.Camera>

    // console.log((gltf.scene));
    // console.log(JSON.stringify(getSimplifiedJson(model)));

    render();
  });
}


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
  // controls.maxDistance = 100;
  controls.enablePan = false;
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.update();



  new RGBELoader().setPath("textures/").load("autoshop_01_4k.hdr", function (texture) {
    texture.mapping = THREE.EquirectangularReflectionMapping;

    scene.background = texture;
    scene.environment = texture;

    render();

    // model
  });





  // loadGLTFModel("models/Engine/scene.gltf");
  // loadGLTFModel("models/DamagedHelmet/DamagedHelmet.gltf");
  loadGLTFModel("models/downloaded/b16d287497b24d8b9e2b94baf7f6b3e2.glb")


  // const loader = new GLTFLoader().setPath("models/");



  window.addEventListener("resize", onWindowResize);

  if (!hideGui) {
    stats = new Stats();
  }
  // container.appendChild(stats.dom);

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
  // renderer.domElement.addEventListener("pointermove", onPointerMove);

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
  // stats.begin();
  const timer = performance.now();
  if (params.rotate) {
    group.rotation.y = timer * 0.0001;
  }
  controls.update();
  composer.render();
  // stats.end();
  if (mixer != null) {
    mixer.update(1 / 100);
  }
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
    // meshName: meshName,
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
  // console.log(selectedObjects);
}




// ############ INTERFACE ############

// TODO: fix
function highlight(searchTerms) {
  const searchStringLower = searchTerms.map(term => term.toLowerCase());
  selectedObjects = [];

  scene.traverse(function (object) {
    if (object.isMesh == true) {
      const objectNameLower = object.name.toLowerCase();
      if (searchStringLower.some(term => objectNameLower.includes(term))) {
        selectedObjects.push(object);
      }
    }
  });

  if (selectedObjects.length > 0) {
    outlinePass.selectedObjects = selectedObjects;
  }
}

function recolor(objectNames, color) {
  scene.traverse(function (object) {
    if (objectNames.includes(object.name)) {
      object.traverse(function (child) {
        if (child instanceof THREE.Mesh && child.material) {
          // Clone the material
          var newMaterial = child.material.clone();
          // Set the color of the new material
          newMaterial.color.set(color);
          // Apply the new material to the mesh
          child.material = newMaterial;
          // If the object has multiple materials
          if (Array.isArray(child.material)) {
            child.material = child.material.map(material => {
              const newMaterial = material.clone();
              newMaterial.color.set(color);
              return newMaterial;
            });
          }
        }
      });
    }
  });
}

function resize(objectNames, scaleX, scaleY, scaleZ) {
  scene.traverse(function (object) {
    if (objectNames.includes(object.name)) {
      object.scale.set(scaleX, scaleY, scaleZ);
    }
  });
}

function rotate(objectNames, rotationX, rotationY, rotationZ) {
  scene.traverse(function (object) {
    if (objectNames.includes(object.name)) {
      object.rotation.set(rotationX, rotationY, rotationZ);
    }
  });
}

function move(objectNames, translateX, translateY, translateZ) {
  scene.traverse(function (object) {
    if (objectNames.includes(object.name)) {
      object.position.x += translateX;
      object.position.y += translateY;
      object.position.z += translateZ;
    }
  });
}

function hide(objectNames) {
  scene.traverse(function (object) {
    if (objectNames.includes(object.name)) {
      object.visible = false;
    }
  });
}

function playAnimations(clipNames) {
  clipNames.forEach(clipName => {
    let selectedClip = clips.find(clip => clip.name === clipName);
    if (selectedClip) {
      const action = mixer.clipAction(selectedClip);
      action.clampWhenFinished = true;
      action.setLoop(THREE.LoopOnce);
      action.play();
    }
  });

  // clips.forEach(function (clip) {
  //   mixer.clipAction(clip).play();
  // });

}



let functionInterface = {
  highlight: highlight,
  recolor: recolor,
  resize: resize,
  rotate: rotate,
  move: move,
  hide: hide,
  playAnimations: playAnimations,
  playAnimation: playAnimation
}


// ########## CHAT FUNCTIONALITY ##########
let chatInput = document.getElementById('chat-input');

chatInput.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    // console.log("enter")
    sendMessage(chatInput.value); // Replace with the function you want to trigger
    event.preventDefault(); // Prevent the Enter key from creating a new line
    chatInput.value = ''; // Clear the input field
  }
});

function sendMessage(message) {
  if (message.startsWith("download ")) {
    // remove download from message at the beginning
    message = message.substring(9);
    makeRequest("http://localhost:5001/", message)
      .then(handleDownloadResponse)
      .catch(handleError);
  } else {
    makeRequest("http://localhost:5000/", message)
      .then(handleChatResponse)
      .catch(handleError);
  }

}





function makeRequest(url, data) {
  showToast("Processing...");

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "text/plain"
    },
    body: data
  }).then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // console.log(response);
    return response.text();
  });
}

function handleError(e) {
  console.log(e)
}

function handleChatResponse(res) {
  // console.log(res);
  executeFunctionCalls(res);
}


function handleDownloadResponse(res) {
  let location = "models/downloaded/" + res;
  loadGLTFModel(location)
}


// ########## PARSE RESPONSE ##########

function executeFunctionCalls(response) {
  console.log(response);

  let lines = response.split('\n');
  //trim whitespace at beginning and end of each line
  lines = lines.map(line => line.trim());
  // remove empty lines
  lines = lines.filter(line => line != '');

  for (let i = 0; i < lines.length; i++) {
    showToast(lines[i])
  }

  // remove unnecessary whitespace
  lines = lines.map(line => removeWhitespace(line));
  // split each line into an array of arguments
  lines = lines.map(line => splitString(line))
  // convert arguments to correct types

  l(lines)

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    lines[i] = line.map(arg => {
      if (arg.startsWith('[')) {
        console.log(arg)
        arg = arg.toString().replace(/'/g, '"');
        arg = JSON.parse(arg);
      } else if (arg.startsWith('0x')) {
        arg = parseInt(arg);
      } else if (isNumeric(arg)) {
        arg = parseFloat(arg);
      }
      return arg;
    });
  }

  console.log(lines);

  // call functions
  for (let line of lines) {
    let func = line[0];
    // console.log(func);
    let args = line.slice(1);
    functionInterface[func](...args);
  }
}

function removeWhitespace(str) {
  let insideBrackets = false;
  let insideQuotes = false;
  let quoteChar = '';
  let result = '';

  for (let i = 0; i < str.length; i++) {
    const char = str[i];

    // Toggle insideBrackets flag when encountering [ or ]
    if (char === '[' && !insideQuotes) {
      insideBrackets = true;
      result += char;
      continue;
    } else if (char === ']' && !insideQuotes) {
      insideBrackets = false;
      result += char;
      continue;
    }

    // Toggle insideQuotes flag when encountering ' or " if not already inside a different quote
    if ((char === "'" || char === '"') && (!insideQuotes || quoteChar === char)) {
      insideQuotes = !insideQuotes;
      quoteChar = insideQuotes ? char : '';
    }

    // If inside brackets but not inside quotes, skip whitespace characters
    if (insideBrackets && !insideQuotes && char === ' ') {
      continue;
    }

    result += char;
  }

  return result;
}

function isNumeric(str) {
  if (typeof str != "string") return false // we only process strings!  
  return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
    !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

function splitString(str) {
  // Regular expression to match text inside brackets or words outside
  const regex = /\[.*?\]|[\w]+/g;
  // Find all matches
  const matches = str.match(regex);

  // Check if matches were found
  if (matches) {
    // Process each match
    return matches.map(match => {
      // Remove leading and trailing spaces
      return match.trim();
    });
  } else {
    // Return an empty array if no matches were found
    return [];
  }
}


setTimeout(function () {
  testFunction();
}, 1000);



function findObjectByName(name) {
  let found = null;
  scene.traverse(function (object) {
    if (object.name === name) {
      found = object;
    }
  });
  return found;
}



function testFunction() {




  // let obj = findObjectByName("cylinderHeadRight");

  // mixer = new THREE.AnimationMixer(obj);
  // let action = mixer.clipAction(clips[0])
  // action.clampWhenFinished = true;
  // action.setLoop(THREE.LoopOnce);
  // action.play();

  // console.log(obj);

  // playAnimation(['piston001', 'piston002', 'piston003', 'piston004', 'piston005', 'piston006', 'piston007', 'piston008']);


  // let response = `rotate ['cylinderHeadRight','cylinderHeadLeft','cylinderHeadCoverRight','cylinderHeadCoverleft'] 0 0 180
  // highlight ['cylinderHeadRight','cylinderHeadLeft','cylinderHeadCoverRight','cylinderHeadCoverleft']`;
  // let response = `
  // // playAnimations ['Take 001']`;
  // executeFunctionCalls(response);
}


// let mixer; // Declare the mixer outside the function so it can be accessed globally

function playAnimation(objectNames) {
  objectNames.forEach(objectName => {
    let obj = findObjectByName(objectName);
    if (obj) {
      let action = mixer.clipAction(clips[0], obj); // Use the object as the second argument
      action.clampWhenFinished = true;
      action.setLoop(THREE.LoopOnce);
      action.play();
    }
  });
}



// clips.forEach(function (clip) {
//   mixer.clipAction(clip).play();
// });
