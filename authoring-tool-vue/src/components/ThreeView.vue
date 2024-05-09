<template>
  <div class="three-view" ref="threeView"></div>
</template>

<script>
import * as THREE from "three";

export default {
  mounted() {
    this.initThreeJS();
  },
  methods: {
    initThreeJS() {
      const width = this.$refs.threeView.clientWidth;
      const height = this.$refs.threeView.clientHeight;

      // Scene
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0xabcdef);

      // Camera
      const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
      camera.position.z = 5;

      // Renderer
      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(width, height);
      this.$refs.threeView.appendChild(renderer.domElement);

      // Animation Loop
      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      };
      animate();
    },
  },
};
</script>

<style scoped>
.three-view {
  flex: 1;
  height: 100vh;
}
</style>
