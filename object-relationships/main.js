import * as THREE from 'three';

import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';

let camera, scene, renderer, loader;

init();
render();

function init() {

    const container = document.createElement('div');
    document.body.appendChild(container);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1;
    container.appendChild(renderer.domElement);

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
    camera.position.set(0, 100, 0);
    camera.position.set(-1.8, 0.6, 2.7);

    const environment = new RoomEnvironment(renderer);
    const pmremGenerator = new THREE.PMREMGenerator(renderer);

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbbbbbb);
    scene.environment = pmremGenerator.fromScene(environment).texture;
    environment.dispose();

    const grid = new THREE.GridHelper(500, 10, 0xffffff, 0xffffff);
    grid.material.opacity = 0.5;
    grid.material.depthWrite = false;
    grid.material.transparent = true;
    scene.add(grid);

    const ktx2Loader = new KTX2Loader()
        .setTranscoderPath('jsm/libs/basis/')
        .detectSupport(renderer);

    loader = new GLTFLoader();
    loader.setKTX2Loader(ktx2Loader);
    loader.setMeshoptDecoder(MeshoptDecoder);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.addEventListener('change', render); // use if there is no animation loop
    controls.minDistance = 1;
    controls.maxDistance = 10;
    // controls.target.set(3, 3, 0);
    controls.update();

    window.addEventListener('resize', onWindowResize);

}

function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);

    render();

}

let model;

function loadModel(path) {
    loader.load(path, function (gltf) {
        model = gltf.scene;
        scene.add(model);
        render();
        model = gltf.scene;
    });
    return model;
}



let chair = loadModel('chair.glb')
console.log(model)
let taxi = loadModel('taxi.glb')

const sphere = new THREE.SphereGeometry();
const object = new THREE.Mesh(sphere, new THREE.MeshBasicMaterial(0xff0000));

let box = new THREE.BoxHelper(object, 0xffff00)
scene.add(box)
render()




function render() {
    renderer.render(scene, camera);
}