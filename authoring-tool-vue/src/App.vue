<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Tree from 'primevue/tree';

import { NodeService } from '@/service/NodeService';
import { onMounted, ref } from 'vue'
import Button from "primevue/button"
import 'primeicons/primeicons.css'
import Sidebar from './components/Sidebar.vue';
import ThreeView from './components/ThreeView.vue';

import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import ThreeViewNew from './components/ThreeViewNew.vue';



const nodes = ref(null);

onMounted(async () => {
  nodes.value = await NodeService.getTreeNodes();
});

</script>

<template>
  <!-- <Splitter style="border: 0px;" >
    <SplitterPanel class="flex align-items-center justify-content-center">
      <Sidebar />
    </SplitterPanel>
    <SplitterPanel class="flex align-items-center justify-content-center">
      <ThreeView />
    </SplitterPanel>
  </Splitter> -->


  <ThreeViewNew />

</template>
