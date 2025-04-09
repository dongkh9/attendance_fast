<template>
  <div>
    {{ hello }}
  </div>
</template>

<script setup>
import {ref,onMounted} from  'vue';
import axios from 'axios';
const hello = ref("hello");

onMounted( async ()=>{
  hello.value = (await axios.get("http://localhost:8000/hello")).data.message;
})
</script>

<style scoped>

</style>