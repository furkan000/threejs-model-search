import * as THREE from 'three';

import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { GUI } from 'dat.gui'

let camera, scene, renderer, loader;
let models = [];
let boxHelpers = [];
let lastRelationship;

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

function loadModel(path) {
    loader.load(path, function (gltf) {
        let model = gltf.scene;
        scene.add(model);
        render();
        model = gltf.scene;
        // console.log(model);
        models.push(model);
    });
}

function addGui() {
    const gui = new GUI()

    const guiData = {
        scale: 1 // Initial scaling factor
    };

    const cubeFolder = gui.addFolder('Taxi')
    cubeFolder.add(models[0].position, 'x', -5, 5).onChange(calculateRelationshipAndAddBoundingBoxes)
    cubeFolder.add(models[0].position, 'y', -5, 5).onChange(calculateRelationshipAndAddBoundingBoxes)
    cubeFolder.add(models[0].position, 'z', -5, 5).onChange(calculateRelationshipAndAddBoundingBoxes)
    cubeFolder.add(guiData, 'scale', 0.1, 5).name('Taxi Scale').onChange((value) => { scaleTaxi(value); calculateRelationshipAndAddBoundingBoxes() })
    cubeFolder.open()
}

function scaleTaxi(scalar) {
    models[0].scale.set(scalar, scalar, scalar);
    render();
}

function convertBoxHelperToBox(boxHelper) {
    const b = new THREE.Box3().setFromObject(boxHelper);
    return new Box3D(b.min.x, b.min.y, b.min.z, b.max.x, b.max.y, b.max.z);
}

function calculateRelationshipAndAddBoundingBoxes() {
    addBoundingBoxes(models);
    let boxHelper1 = new THREE.BoxHelper(models[0], 0xffff00)
    let boxHelper2 = new THREE.BoxHelper(models[1], 0xffff00)
    let box1 = convertBoxHelperToBox(boxHelper1);
    let box2 = convertBoxHelperToBox(boxHelper2);

    if (lastRelationship != undefined && lastRelationship != box1.determineRelationship(box2)) {
        Toastify({
            text: box1.determineRelationship(box2),
            duration: 3000,
            gravity: "top",
            position: "center",
        }).showToast();
    }
    lastRelationship = box1.determineRelationship(box2);
}

function addBoundingBoxes(models) {
    boxHelpers.forEach(box => {
        scene.remove(box)
    });

    models.forEach(model => {
        let box = new THREE.BoxHelper(model, 0xffff00)
        boxHelpers.push(box);
        scene.add(box)
    });
    render();
}

function render() {
    renderer.render(scene, camera);
}

loadModel('chair.glb')
loadModel('taxi.glb')

// wait then do
setTimeout(function () {
    addGui();
    calculateRelationshipAndAddBoundingBoxes();
    render();
}, 1000);