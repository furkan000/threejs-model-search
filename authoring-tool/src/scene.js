import * as THREE from "three";

import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RGBELoader } from "three/addons/loaders/RGBELoader.js";
import { GLTFExporter } from "three/addons/exporters/GLTFExporter.js";

export function run() {
  const renderer = new THREE.WebGLRenderer({ canvas: document.querySelector("canvas"), antialias: true });
  const loader = new GLTFLoader();

  // There's no reason to set the aspect here because we're going
  // to set it every frame anyway so we'll set it to 2 since 2
  // is the the aspect for the canvas default size (300w/150h = 2)
  const camera = new THREE.PerspectiveCamera(70, 2, 1, 1000);
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
}
