import * as THREE from 'three';

import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';

let camera, scene, renderer;

init();

function init() {
    const container = document.createElement('div');
    document.body.appendChild(container);

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.25, 20);
    camera.position.set(- 1.8, 0.6, 2.7);

    scene = new THREE.Scene();

    new RGBELoader()
        .setPath('./textures/')
        .load('royal_esplanade_4k.hdr', function (texture) {

            texture.mapping = THREE.EquirectangularReflectionMapping;
            scene.background = texture;
            scene.environment = texture;
            render();

            // model
            const loader = new GLTFLoader().setPath('./models/');
            loader.load('cafeteria.glb', async function (gltf) {
                const model = gltf.scene;
                // wait until the model can be added to the scene without blocking due to shader compilation
                await renderer.compileAsync(model, camera, scene);
                scene.add(model);

                renderTreeView(model);


                renderToFile();

                render();

            });

        });

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1;
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.addEventListener('change', render); // use if there is no animation loop
    controls.minDistance = 2;
    controls.maxDistance = 10;
    controls.target.set(0, 0, - 0.2);
    controls.update();

    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}

function render() {
    renderer.render(scene, camera);
}

function renderToFile() {
    const canvas = renderer.domElement;
    const width = canvas.width;
    const height = canvas.height;

    const dataUrl = canvas.toDataURL('image/png');
    const data = dataUrl.replace(/^data:image\/\w+;base64,/, '');
    const buf = new Buffer(data, 'base64');
    fs.writeFile('out.png', buf, function (err) {
        if (err) throw err;
        console.log('It\'s saved!');
    });
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


function buildTreeView(json, containerId) {
    // Recursive function to process each node
    function createNode(node) {
        let element = document.createElement('li');
        let span = document.createElement('span');
        span.classList.add('caret');
        span.textContent = node.name;
        element.appendChild(span);

        if (node.children && node.children.length > 0) {
            let ul = document.createElement('ul');
            ul.classList.add('nested');
            node.children.forEach(child => {
                ul.appendChild(createNode(child));
            });
            element.appendChild(ul);
        }
        return element;
    }

    // Clear existing content
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    // Start with the root node
    let ul = document.createElement('ul');
    ul.id = 'myUL';
    ul.appendChild(createNode(json));
    container.appendChild(ul);

    // Add event listeners for toggling
    var toggler = container.getElementsByClassName("caret");
    for (let i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
        });
    }
}



function renderTreeView(model) {
    console.log(getSimplifiedJson(model));
    buildTreeView(getSimplifiedJson(model), 'tree-container');
}


