<template>
  <v-img 
    v-if="studio === 'Movement Nation Hurstville'"
    src="/public/movement_nation_hurstville.webp"
  />
  <v-img 
    v-if="studio === 'Movement Nation Parramatta'"
    src="/public/movement_nation_parramatta.webp"
  />
  <v-img
    v-if="studio === 'IMI'"
    class="imi pa-2"
    src="/public/imi.png"
  />
  </template>
  
<script lang="ts" setup>
  defineProps({
    studio: String
  })
</script>

<style>
  .v-img {
    width: 100px;
    height: 100px;
  }

  .imi {
    background-color: black;
  }
</style>